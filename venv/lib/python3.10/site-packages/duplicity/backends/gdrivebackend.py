# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2015 Yigal Asnis
# Copyright 2021 Jindrich Makovicka
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
import pickle

import duplicity.backend
from duplicity import log
from duplicity.errors import BackendException


class GDriveBackend(duplicity.backend.Backend):
    """Connect to remote store using Google Drive API V3"""

    PAGE_SIZE = 100
    MIN_RESUMABLE_UPLOAD = 5 * 1024 * 1024

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)
        try:
            from googleapiclient.discovery import build
            from google.oauth2.service_account import Credentials
        except ImportError as e:
            raise BackendException(
                f"""GDrive backend requires Google API client installation.
Please read the manpage for setup details.
Exception: {str(e)}"""
            )

        # Note Google has 2 drive methods, `Shared(previously Team) Drives` and `My Drive`
        #   both can be shared but require different addressing
        # For a Google Shared Drives folder
        # ---------------------------------
        # Share Drive ID specified as a query parameter in the backend URL.
        # Example:
        #  gdrive://developer.gserviceaccount.com/target-folder/?driveID=<SHARED DRIVE ID>
        #
        # For a Google My Drive based shared folder
        # -----------------------------------------
        # MyDrive folder ID specified as a query parameter in the backend URL
        #
        # Example
        #  export GOOGLE_SERVICE_ACCOUNT_URL=<serviceaccount-name>@<serviceaccount-name>.iam.gserviceaccount.com
        #  gdrive://${GOOGLE_SERVICE_ACCOUNT_URL}/<target-folder-name/>?myDriveFolderID=<google-myDrive-folder-id>
        #
        # both methods use a Google Services Account
        # export GOOGLE_SERVICE_JSON_FILE=<serviceaccount-credentials.json>
        # export GOOGLE_SERVICE_ACCOUNT_URL=<serviceaccount-name>@<serviceaccount-name>.iam.gserviceaccount.com
        #
        # Note that a local http server will be created on port 8080 to receive the redirect from the Google
        # OAuth service. If you are running on a remote server, you will need to port forward 8080 from the machine
        # which will do the web based authentication.

        self.shared_drive_corpora = {}
        self.shared_drive_id = {}
        self.shared_drive_flags_include = {}
        self.shared_drive_flags_support = {}
        self.shared_root_folder_id = None
        if "driveID" in parsed_url.query_args:
            self.shared_drive_corpora = {"corpora": "drive"}
            self.shared_drive_id = {"driveId": parsed_url.query_args["driveID"][0]}
            self.shared_drive_flags_include = {"includeItemsFromAllDrives": True}
            self.shared_drive_flags_support = {"supportsAllDrives": True}
        elif "myDriveFolderID" in parsed_url.query_args:
            self.shared_drive_corpora = {"corpora": "user"}
            self.shared_drive_flags_include = {"includeItemsFromAllDrives": True}
            self.shared_drive_flags_support = {"supportsAllDrives": True}
            self.shared_root_folder_id = parsed_url.query_args["myDriveFolderID"][0]
        else:
            raise BackendException(
                "gdrive: backend requires a query paramater should either be driveID or myDriveFolderID"
            )
        if parsed_url.username is not None:
            client_id = f"{parsed_url.username}@{parsed_url.hostname}"
        else:
            client_id = parsed_url.hostname

        if "GOOGLE_SERVICE_JSON_FILE" in os.environ:
            credentials = Credentials.from_service_account_file(os.environ["GOOGLE_SERVICE_JSON_FILE"])
            if credentials.service_account_email != client_id:
                raise BackendException(
                    f"Service account email in the JSON file ({credentials.service_account_email}) "
                    f"does not match the URL ({client_id})"
                )

        elif "GOOGLE_CLIENT_SECRET_JSON_FILE" in os.environ and "GOOGLE_CREDENTIALS_FILE" in os.environ:
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request

            credentials = None
            if os.path.exists(os.environ["GOOGLE_CREDENTIALS_FILE"]):
                with open(os.environ["GOOGLE_CREDENTIALS_FILE"], "rb") as token:
                    credentials = pickle.load(token)

            # If there are no (valid) credentials available, let the user log in.
            if not credentials or not credentials.valid:
                if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        os.environ["GOOGLE_CLIENT_SECRET_JSON_FILE"],
                        ["https://www.googleapis.com/auth/drive.file"],
                    )

                    if flow.client_config["client_id"] != client_id:
                        raise BackendException(
                            f"Client ID in the JSON file ({flow.client_config['client_id']}) "
                            f"does not match the URL ({client_id})"
                        )

                    flow_args = {"open_browser": False}
                    if "GOOGLE_OAUTH_LOCAL_SERVER_PORT" in os.environ:
                        flow_args["port"] = int(os.environ["GOOGLE_OAUTH_LOCAL_SERVER_PORT"])
                    if "GOOGLE_OAUTH_LOCAL_SERVER_HOST" in os.environ:
                        flow_args["host"] = os.environ["GOOGLE_OAUTH_LOCAL_SERVER_HOST"]
                    credentials = flow.run_local_server(**flow_args)
                # Save the credentials for the next run
                with open(os.environ["GOOGLE_CREDENTIALS_FILE"], "wb") as token:
                    pickle.dump(credentials, token)

            if credentials.client_id != client_id:
                raise BackendException(
                    f"Client ID in the credentials file ({credentials.client_id}) does not match the URL ({client_id})"
                )

        else:
            raise BackendException(
                "GOOGLE_SERVICE_JSON_FILE or GOOGLE_CLIENT_SECRET_JSON_FILE environment "
                "variable not set. Please read the manpage to fix."
            )

        self.drive = build("drive", "v3", credentials=credentials)

        if self.shared_drive_id:
            parent_folder_id = self.shared_drive_id["driveId"]
        elif self.shared_root_folder_id:
            parent_folder_id = self.shared_root_folder_id
        else:
            parent_folder_id = "root"

        # Fetch destination folder entry and create hierarchy if required.
        folder_names = parsed_url.path.split("/")
        for folder_name in folder_names:
            if not folder_name:
                continue
            q = (
                "name = '"
                + folder_name
                + "' and '"
                + parent_folder_id
                + "' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed=false"
            )
            results = (
                self.drive.files()
                .list(
                    q=q,
                    pageSize=1,
                    fields="files(name,id),nextPageToken",
                    **self.shared_drive_corpora,
                    **self.shared_drive_id,
                    **self.shared_drive_flags_include,
                    **self.shared_drive_flags_support,
                )
                .execute()
            )
            file_list = results.get("files", [])
            if len(file_list) == 0:
                file_metadata = {
                    "name": folder_name,
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [parent_folder_id],
                }
                file_metadata.update(self.shared_drive_id)
                folder = (
                    self.drive.files()
                    .create(
                        body=file_metadata,
                        fields="id",
                        **self.shared_drive_flags_support,
                    )
                    .execute()
                )
            else:
                folder = file_list[0]

            parent_folder_id = folder["id"]

        self.folder = parent_folder_id
        self.id_cache = {}

    def file_by_name(self, filename):
        from googleapiclient.errors import HttpError

        filename = os.fsdecode(filename)

        if filename in self.id_cache:
            # It might since have been locally moved, renamed or deleted, so we
            # need to validate the entry.
            file_id = self.id_cache[filename]
            try:
                drive_file = (
                    self.drive.files()
                    .get(
                        fileId=file_id,
                        fields="id,size,name,parents,trashed",
                        **self.shared_drive_flags_support,
                    )
                    .execute()
                )
                if drive_file["name"] == filename and not drive_file["trashed"]:
                    for parent in drive_file["parents"]:
                        if parent == self.folder:
                            log.Info(f"GDrive backend: found file '{filename}' with id {file_id} in ID cache")
                            return drive_file
            except HttpError as error:
                # A 404 occurs if the ID is no longer valid
                if error.resp.status != 404:
                    raise
            # If we get here, the cache entry is invalid
            log.Info(f"GDrive backend: invalidating '{filename}' (previously ID {file_id}) from ID cache")
            del self.id_cache[filename]

        # Not found in the cache, so use directory listing. This is less
        # reliable because there is no strong consistency.
        q = f"name = '{filename}' and '{self.folder}' in parents and trashed = false"
        results = (
            self.drive.files()
            .list(
                q=q,
                fields="files(name,id,size),nextPageToken",
                pageSize=2,
                **self.shared_drive_corpora,
                **self.shared_drive_id,
                **self.shared_drive_flags_include,
                **self.shared_drive_flags_support,
            )
            .execute()
        )
        file_list = results.get("files", [])
        if len(file_list) > 1:
            log.FatalError(f"GDrive backend: multiple files called '{filename}'.")
        elif len(file_list) > 0:
            file_id = file_list[0]["id"]
            self.id_cache[filename] = file_list[0]["id"]
            log.Info(f"GDrive backend: found file '{filename}' with id {file_id} on server, adding to cache")
            return file_list[0]

        log.Info(f"GDrive backend: file '{filename}' not found in cache or on server")
        return None

    def id_by_name(self, filename):
        drive_file = self.file_by_name(filename)
        if drive_file is None:
            return ""
        else:
            return drive_file["id"]

    def _put(self, source_path, remote_filename):
        from googleapiclient.http import MediaFileUpload

        remote_filename = os.fsdecode(remote_filename)
        drive_file = self.file_by_name(remote_filename)
        if remote_filename.endswith(".gpg"):
            mime_type = "application/pgp-encrypted"
        else:
            mime_type = "text/plain"

        file_size = os.path.getsize(source_path.name)
        if file_size >= self.MIN_RESUMABLE_UPLOAD:
            resumable = True
            num_retries = 5
        else:
            resumable = False
            num_retries = 0

        media = MediaFileUpload(source_path.name, mimetype=mime_type, resumable=resumable)
        if drive_file is None:
            # No existing file, make a new one
            file_metadata = {"name": remote_filename, "parents": [self.folder]}
            file_metadata.update(self.shared_drive_id)
            log.Info(f"GDrive backend: creating new file '{remote_filename}'")
            drive_file = (
                self.drive.files()
                .create(
                    body=file_metadata,
                    media_body=media,
                    **self.shared_drive_flags_support,
                )
                .execute(num_retries=num_retries)
            )
        else:
            log.Info(f"GDrive backend: replacing existing file '{remote_filename}' with id '{drive_file['id']}'")
            drive_file = (
                self.drive.files()
                .update(
                    media_body=media,
                    fileId=drive_file["id"],
                    **self.shared_drive_flags_support,
                )
                .execute(num_retries=num_retries)
            )

        self.id_cache[remote_filename] = drive_file["id"]

    def _get(self, remote_filename, local_path):
        from googleapiclient.http import MediaIoBaseDownload

        drive_file = self.file_by_name(remote_filename)
        request = self.drive.files().get_media(fileId=drive_file["id"], **self.shared_drive_flags_support)
        with open(os.fsdecode(local_path.name), "wb") as fh:
            done = False
            downloader = MediaIoBaseDownload(fh, request)
            while done is False:
                status, done = downloader.next_chunk()

    def _list(self):
        page_token = None
        drive_files = []
        while True:
            response = (
                self.drive.files()
                .list(
                    q=f"'{self.folder}' in parents and trashed=false",
                    pageSize=self.PAGE_SIZE,
                    fields="files(name,id),nextPageToken",
                    pageToken=page_token,
                    **self.shared_drive_corpora,
                    **self.shared_drive_id,
                    **self.shared_drive_flags_include,
                    **self.shared_drive_flags_support,
                )
                .execute()
            )

            drive_files += response.get("files", [])

            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

        filenames = set(item["name"] for item in drive_files)
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
        else:
            self.drive.files().delete(fileId=file_id, **self.shared_drive_flags_support).execute()

    def _query(self, filename):
        drive_file = self.file_by_name(filename)
        if drive_file is None:
            size = -1
        else:
            size = int(drive_file["size"])
        return {"size": size}

    def _error_code(self, operation, error):  # pylint: disable=unused-argument
        from google.auth.exceptions import RefreshError
        from googleapiclient.errors import HttpError

        if isinstance(error, HttpError):
            return log.ErrorCode.backend_not_found
        elif isinstance(error, RefreshError):
            return log.ErrorCode.backend_permission_denied
        return log.ErrorCode.backend_error


duplicity.backend.register_backend("gdrive", GDriveBackend)

duplicity.backend.uses_netloc.extend(["gdrive"])
