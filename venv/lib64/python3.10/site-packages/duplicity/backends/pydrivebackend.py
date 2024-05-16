# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2015 Yigal Asnis
#
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# It is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with duplicity; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


import os

import duplicity.backend
from duplicity import log
from duplicity.errors import BackendException


class PyDriveBackend(duplicity.backend.Backend):
    """Connect to remote store using PyDrive API"""

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        log.Warn(
            "\n\nThe PyDrive backend is now deprecated and will be removed in a future version.\n"
            "It has been replaced by the GDrive backend.  See the manpage for details.\n\n\n"
        )

        try:
            import httplib2
            from apiclient.discovery import build
        except ImportError as e:
            raise BackendException(
                "PyDrive backend requires PyDrive2 and Google API client installation.\n"
                "Please read the manpage for setup details.\n"
                f"Exception: {str(e)}"
            )

        # Shared Drive ID specified as a query parameter in the backend URL.
        # Example: pydrive://developer.gserviceaccount.com/target-folder/?driveID=<SHARED DRIVE ID>
        self.api_params = {}
        self.shared_drive_id = None
        if "driveID" in parsed_url.query_args:
            self.shared_drive_id = parsed_url.query_args["driveID"][0]
            self.api_params = {
                "corpora": "teamDrive",
                "teamDriveId": self.shared_drive_id,
                "includeTeamDriveItems": True,
                "supportsTeamDrives": True,
            }

        try:
            from pydrive2.auth import GoogleAuth
            from pydrive2.drive import GoogleDrive
            from pydrive2.files import (
                ApiRequestError,
                FileNotUploadedError,
            )
        except ImportError as e:
            raise BackendException(
                f"PyDrive backend requires PyDrive2 installation.\n"
                f"Please read the manpage for setup details.\n"
                f"Exception: {str(e)}"
            )

        # let user get by with old client while he can
        try:
            from oauth2client.client import SignedJwtAssertionCredentials

            self.oldClient = True
        except Exception as e:
            from oauth2client.service_account import ServiceAccountCredentials
            from oauth2client import crypt

            self.oldClient = False

        if "GOOGLE_DRIVE_ACCOUNT_KEY" in os.environ:
            account_key = os.environ["GOOGLE_DRIVE_ACCOUNT_KEY"]
            if self.oldClient:
                credentials = SignedJwtAssertionCredentials(
                    parsed_url.username + "@" + parsed_url.hostname,
                    account_key,
                    scopes="https://www.googleapis.com/auth/drive",
                )
            else:
                signer = crypt.Signer.from_string(account_key)  # pylint: disable=used-before-assignment
                credentials = ServiceAccountCredentials(  # pylint: disable=used-before-assignment
                    parsed_url.username + "@" + parsed_url.hostname,
                    signer,
                    scopes="https://www.googleapis.com/auth/drive",
                )
            credentials.authorize(httplib2.Http())
            gauth = GoogleAuth(http_timeout=60)
            gauth.credentials = credentials
        elif "GOOGLE_DRIVE_SETTINGS" in os.environ:
            gauth = GoogleAuth(settings_file=os.environ["GOOGLE_DRIVE_SETTINGS"], http_timeout=60)
            gauth.CommandLineAuth()
        elif "GOOGLE_SECRETS_FILE" in os.environ and "GOOGLE_CREDENTIALS_FILE" in os.environ:
            gauth = GoogleAuth(http_timeout=60)
            gauth.LoadClientConfigFile(os.environ["GOOGLE_SECRETS_FILE"])
            gauth.LoadCredentialsFile(os.environ["GOOGLE_CREDENTIALS_FILE"])
            if gauth.credentials is None:
                gauth.CommandLineAuth()
            elif gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()
            gauth.SaveCredentialsFile(os.environ["GOOGLE_CREDENTIALS_FILE"])
        else:
            raise BackendException(
                "GOOGLE_DRIVE_ACCOUNT_KEY or GOOGLE_DRIVE_SETTINGS environment "
                "variable not set. Please read the manpage to fix."
            )
        self.drive = GoogleDrive(gauth)

        if self.shared_drive_id:
            parent_folder_id = self.shared_drive_id
        else:
            # Dirty way to find root folder id
            file_list = self.drive.ListFile({"q": "'Root' in parents and trashed=false"}).GetList()
            if file_list:
                parent_folder_id = file_list[0]["parents"][0]["id"]
            else:
                file_in_root = self.drive.CreateFile({"title": "i_am_in_root"})
                file_in_root.Upload()
                parent_folder_id = file_in_root["parents"][0]["id"]
                file_in_root.Delete()

        # Fetch destination folder entry and create hierarchy if required.
        folder_names = parsed_url.path.split("/")
        for folder_name in folder_names:
            if not folder_name:
                continue
            list_file_args = {"q": f"'{parent_folder_id}' in parents and trashed=false"}
            list_file_args.update(self.api_params)
            file_list = self.drive.ListFile(list_file_args).GetList()
            folder = next(
                (
                    item
                    for item in file_list
                    if item["title"] == folder_name and item["mimeType"] == "application/vnd.google-apps.folder"
                ),
                None,
            )
            if folder is None:
                create_file_args = {
                    "title": folder_name,
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [{"id": parent_folder_id}],
                }
                create_file_args["parents"][0].update(self.api_params)
                create_file_args.update(self.api_params)
                folder = self.drive.CreateFile(create_file_args)
                if self.shared_drive_id:
                    folder.Upload(param={"supportsTeamDrives": True})
                else:
                    folder.Upload()
            parent_folder_id = folder["id"]
        self.folder = parent_folder_id
        self.id_cache = {}

    def file_by_name(self, filename):
        from pydrive2.files import ApiRequestError  # pylint: disable=import-error

        filename = os.fsdecode(filename)  # PyDrive deals with unicode filenames

        if filename in self.id_cache:
            # It might since have been locally moved, renamed or deleted, so we
            # need to validate the entry.
            file_id = self.id_cache[filename]
            drive_file = self.drive.CreateFile({"id": file_id})
            try:
                if drive_file["title"] == filename and not drive_file["labels"]["trashed"]:
                    for parent in drive_file["parents"]:
                        if parent["id"] == self.folder:
                            log.Info(f"PyDrive backend: found file '{filename}' with id {file_id} in ID cache")
                            return drive_file
            except ApiRequestError as error:
                # A 404 occurs if the ID is no longer valid
                if error.args[0].resp.status != 404:
                    raise
            # If we get here, the cache entry is invalid
            log.Info(f"PyDrive backend: invalidating '{filename}' (previously ID {file_id}) from ID cache")
            del self.id_cache[filename]

        # Not found in the cache, so use directory listing. This is less
        # reliable because there is no strong consistency.
        q = f"title='{filename}' and '{self.folder}' in parents and trashed=false"
        fields = "items(title,id,fileSize,downloadUrl,exportLinks),nextPageToken"
        list_file_args = {"q": q, "fields": fields}
        list_file_args.update(self.api_params)
        flist = self.drive.ListFile(list_file_args).GetList()
        if len(flist) > 1:
            log.FatalError(_("PyDrive backend: multiple files called '%s'.") % (filename,))
        elif flist:
            file_id = flist[0]["id"]
            self.id_cache[filename] = flist[0]["id"]
            log.Info(f"PyDrive backend: found file '{filename}' with id {file_id} on server, adding to cache")
            return flist[0]
        log.Info(f"PyDrive backend: file '{filename}' not found in cache or on server")
        return None

    def id_by_name(self, filename):
        drive_file = self.file_by_name(filename)
        if drive_file is None:
            return ""
        else:
            return drive_file["id"]

    def _put(self, source_path, remote_filename):
        remote_filename = os.fsdecode(remote_filename)
        drive_file = self.file_by_name(remote_filename)
        if drive_file is None:
            # No existing file, make a new one
            create_file_args = {
                "title": remote_filename,
                "parents": [{"kind": "drive#fileLink", "id": self.folder}],
            }
            create_file_args["parents"][0].update(self.api_params)
            drive_file = self.drive.CreateFile(create_file_args)
            log.Info(f"PyDrive backend: creating new file '{remote_filename}'")
        else:
            log.Info(f"PyDrive backend: replacing existing file '{remote_filename}' with id '{drive_file['id']}'")
        drive_file.SetContentFile(os.fsdecode(source_path.name))
        if self.shared_drive_id:
            drive_file.Upload(param={"supportsTeamDrives": True})
        else:
            drive_file.Upload()
        self.id_cache[remote_filename] = drive_file["id"]

    def _get(self, remote_filename, local_path):
        drive_file = self.file_by_name(remote_filename)
        drive_file.GetContentFile(os.fsdecode(local_path.name))

    def _list(self):
        list_file_args = {
            "q": f"'{self.folder}' in parents and trashed=false",
            "fields": "items(title,id),nextPageToken",
        }
        list_file_args.update(self.api_params)
        drive_files = self.drive.ListFile(list_file_args).GetList()
        filenames = set(item["title"] for item in drive_files)
        # Check the cache as well. A file might have just been uploaded but
        # not yet appear in the listing.
        # Note: do not use iterkeys() here, because file_by_name will modify
        # the cache if it finds invalid entries.
        for filename in list(self.id_cache.keys()):
            if (filename not in filenames) and (self.file_by_name(filename) is not None):
                filenames.add(filename)
        return list(filenames)

    def _delete(self, filename):
        file_id = self.id_by_name(filename)
        if file_id == "":
            log.Warn(f"File '{os.fsdecode(filename)}' does not exist while trying to delete it")
        elif self.shared_drive_id:
            self.drive.auth.service.files().delete(fileId=file_id, param={"supportsTeamDrives": True}).execute()
        else:
            self.drive.auth.service.files().delete(fileId=file_id).execute()

    def _query(self, filename):
        drive_file = self.file_by_name(filename)
        if drive_file is None:
            size = -1
        else:
            size = int(drive_file["fileSize"])
        return {"size": size}

    def _error_code(self, operation, error):  # pylint: disable=unused-argument
        from pydrive2.files import (
            ApiRequestError,
            FileNotUploadedError,  # pylint: disable=import-error
        )

        if isinstance(error, FileNotUploadedError):
            return log.ErrorCode.backend_not_found
        elif isinstance(error, ApiRequestError):
            return log.ErrorCode.backend_permission_denied
        return log.ErrorCode.backend_error


duplicity.backend.register_backend("pydrive", PyDriveBackend)
""" pydrive is an alternate way to access gdocs """
duplicity.backend.register_backend("pydrive+gdocs", PyDriveBackend)
""" register pydrive as the default way to access gdocs """
duplicity.backend.register_backend("gdocs", PyDriveBackend)

duplicity.backend.uses_netloc.extend(["pydrive", "pydrive+gdocs", "gdocs"])
