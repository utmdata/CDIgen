# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
# vim:tabstop=4:shiftwidth=4:expandtab
#
# Copyright 2014 Google Inc.
# Contact Michael Stapelberg <stapelberg+duplicity@google.com>
# This is NOT a Google product.
# Revised for Microsoft Graph API 2019 by David Martin
#
# This file is part of duplicity.
#
# Duplicity is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# Duplicity is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with duplicity; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


import json
import os
import sys
import time

import duplicity.backend
from duplicity import config
from duplicity import log
from duplicity import util
from duplicity.errors import BackendException


# For documentation on the API, see
# The previous Live SDK API required the use of opaque folder IDs to navigate paths, but the Microsoft Graph
# API allows the use of parent/child/grandchild pathnames.
# Old Live SDK API: https://docs.microsoft.com/en-us/previous-versions/office/developer/onedrive-live-sdk/dn659731(v%3doffice.15)  # noqa
# Files API: https://docs.microsoft.com/en-us/graph/api/resources/onedrive?view=graph-rest-1.0
# Large file upload API: https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_createuploadsession?view=odsp-graph-online  # noqa


class OneDriveBackend(duplicity.backend.Backend):
    """Uses Microsoft OneDrive (formerly SkyDrive) for backups."""

    API_URI = "https://graph.microsoft.com/v1.0/"
    # The large file upload API says that uploaded chunks (except the last) must be multiples of 327680 bytes.
    REQUIRED_FRAGMENT_SIZE_MULTIPLE = 327680

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        self.directory = parsed_url.path.lstrip("/")

        # this drive_root works for personal and business onedrive
        # to use a sharepoint 365 default drive this needs to be set to
        # 'sites/<xxxx.sharepoint.com>,<site id>/drive'
        self.drive_root = os.environ.get("DUPLICITY_ONEDRIVE_ROOT", "me/drive")

        self.directory_onedrive_path = f"{self.drive_root + '/root'}:/{self.directory}/"
        if self.directory == "":
            raise BackendException(
                "You did not specify a path. " "Please specify a path, e.g. onedrive://duplicity_backups"
            )

        if config.volsize > (10 * 1024 * 1024 * 1024):
            raise BackendException("Your --volsize is bigger than 10 GiB, which is the maximum file size on OneDrive.")

        self.initialize_oauth2_session()

    def initialize_oauth2_session(self):
        client_id = os.environ.get("OAUTH2_CLIENT_ID")
        refresh_token = os.environ.get("OAUTH2_REFRESH_TOKEN")
        for n in range(1, config.num_retries + 1):
            try:
                if client_id and refresh_token:
                    self.http_client = ExternalOAuth2Session(client_id, refresh_token)
                else:
                    self.http_client = DefaultOAuth2Session(self.API_URI)
                break
            except Exception as e:
                if n >= config.num_retries:
                    raise e
                log.Warn(
                    _("Attempt of initialize_oauth2_session Nr. %s failed. %s: %s")
                    % (n, e.__class__.__name__, util.uexc(e))
                )
                time.sleep(config.backend_retry_delay)

    def _list(self):
        accum = []
        # Strip last slash, because graph can give a 404 in some cases with it
        next_url = self.API_URI + self.directory_onedrive_path.rstrip("/") + ":/children"
        while True:
            response = self.http_client.get(next_url, timeout=config.timeout)
            if response.status_code == 404:
                # No further files here
                break
            response.raise_for_status()
            responseJson = response.json()
            if "value" not in responseJson:
                raise BackendException(f'Malformed JSON: expected "value" member in {responseJson}')
            accum += responseJson["value"]
            if "@odata.nextLink" in responseJson:
                next_url = responseJson["@odata.nextLink"]
            else:
                break

        return [x["name"] for x in accum]

    def _get(self, remote_filename, local_path):
        remote_filename = remote_filename.decode("UTF-8")
        with local_path.open("wb") as f:
            response = self.http_client.get(
                self.API_URI + self.directory_onedrive_path + remote_filename + ":/content",
                stream=True,
                timeout=config.timeout,
            )
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
            f.flush()

    def _put(self, source_path, remote_filename):
        # Happily, the OneDrive API will lazily create the folder hierarchy required to contain a pathname

        # Check if the user has enough space available on OneDrive before even
        # attempting to upload the file.
        remote_filename = remote_filename.decode("UTF-8")
        source_size = os.path.getsize(source_path.name)
        start = time.time()
        response = self.http_client.get(self.API_URI + self.drive_root + "?$select=quota", timeout=config.timeout)
        response.raise_for_status()
        if "quota" in response.json():
            available = response.json()["quota"].get("remaining", None)
            if available:
                log.Debug(f"Bytes available: {int(available)}")
                if source_size > available:
                    raise BackendException(
                        (
                            f'Out of space: trying to store "{source_path.name}" ({int(source_size)} bytes), '
                            f"but only {int(available)} bytes available on OneDrive."
                        )
                    )
        log.Debug(f"Checked quota in {time.time() - start:f}s")

        with source_path.open() as source_file:
            start = time.time()
            url = self.API_URI + self.directory_onedrive_path + remote_filename + ":/createUploadSession"

            response = self.http_client.post(url, timeout=config.timeout)
            response.raise_for_status()
            response_json = json.loads(response.content.decode("UTF-8"))
            if "uploadUrl" not in response_json:
                raise BackendException(
                    (
                        f'File "{remote_filename}" cannot be uploaded: '
                        f"could not create upload session: {response.content}"
                    )
                )
            uploadUrl = response_json["uploadUrl"]

            # https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_createuploadsession?
            # indicates 10 MiB is optimal for stable high speed connections.
            offset = 0
            desired_num_fragments = 10 * 1024 * 1024 // self.REQUIRED_FRAGMENT_SIZE_MULTIPLE
            while True:
                chunk = source_file.read(desired_num_fragments * self.REQUIRED_FRAGMENT_SIZE_MULTIPLE)
                if len(chunk) == 0:
                    break
                headers = {
                    "Content-Length": f"{len(chunk)}",
                    "Content-Range": f"bytes {int(offset)}-{int(offset + len(chunk) - 1)}/{int(source_size)}",
                }
                log.Debug(f"PUT {remote_filename} {headers['Content-Range']}")
                response = self.http_client.put(uploadUrl, headers=headers, data=chunk, timeout=config.timeout)
                response.raise_for_status()
                offset += len(chunk)

            log.Debug(f"PUT file in {time.time() - start:f}s")

    def _delete(self, remote_filename):
        remote_filename = remote_filename.decode("UTF-8")
        response = self.http_client.delete(
            self.API_URI + self.directory_onedrive_path + remote_filename,
            timeout=config.timeout,
        )
        if response.status_code == 404:
            raise BackendException(f'File "{remote_filename}" cannot be deleted: it does not exist')
        response.raise_for_status()

    def _query(self, remote_filename):
        remote_filename = remote_filename.decode("UTF-8")
        response = self.http_client.get(
            self.API_URI + self.directory_onedrive_path + remote_filename,
            timeout=config.timeout,
        )
        if response.status_code != 200:
            return {"size": -1}
        if "size" not in response.json():
            raise BackendException(f'Malformed JSON: expected "size" member in {response.json()}')
        return {"size": response.json()["size"]}

    def _retry_cleanup(self):
        self.initialize_oauth2_session()


class OneDriveOAuth2Session(object):
    """A tiny wrapper for OAuth2Session that handles some OneDrive details."""

    OAUTH_TOKEN_URI = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    def __init__(self):
        # OAUTHLIB_RELAX_TOKEN_SCOPE prevents the oauthlib from complaining
        # about a mismatch between the requested scope and the delivered scope.
        # We need this because we don't get a refresh token without asking for
        # offline_access, but Microsoft Graph doesn't include offline_access
        # in its response (even though it does send a refresh_token).
        os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "TRUE"

        # Import requests-oauthlib
        try:
            # On debian (and derivatives), get these dependencies using:
            # apt-get install python-requests-oauthlib
            # On fedora (and derivatives), get these dependencies using:
            # yum install python-requests-oauthlib
            from requests_oauthlib import OAuth2Session

            self.session_class = OAuth2Session
        except ImportError as e:
            raise BackendException(
                f"OneDrive backend requires python-requests-oauthlib to be "
                f"installed. Please install it and try again.\n{str(e)}"
            )

        # Should be filled by a subclass
        self.session = None

    def get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.session.put(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.session.delete(*args, **kwargs)


class DefaultOAuth2Session(OneDriveOAuth2Session):
    """A possibly-interactive console session using a built-in API key"""

    OAUTH_TOKEN_PATH = os.path.expanduser(
        os.environ.get("DUPLICITY_ONEDRIVE_TOKEN", "~/.duplicity_onedrive_oauthtoken.json")
    )

    CLIENT_ID = os.getenv("DUPLICITY_ONEDRIVE_CLIENT_ID", "1612f841-ae01-46ab-9535-43ba6ec04029")
    OAUTH_AUTHORIZE_URI = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    OAUTH_REDIRECT_URI = "https://login.microsoftonline.com/common/oauth2/nativeclient"
    # Files.Read is for reading files,
    # Files.ReadWrite  is for creating/writing files,
    # Files.Read.All and Files.Read.All are used if a sharepoint drive is provided by ONEDRIVE_ROOT in env
    # User.Read is needed for the /me request to see if the token works.
    # offline_access is necessary for duplicity to access onedrive without
    # the user being logged in right now.
    OAUTH_SCOPE = [
        "Files.Read",
        "Files.ReadWrite",
        "Files.Read.All",
        "Files.ReadWrite.All",
        "User.Read",
        "offline_access",
    ]

    def __init__(self, api_uri):
        super().__init__()

        token = None
        try:
            with open(self.OAUTH_TOKEN_PATH) as f:
                token = json.load(f)
        except IOError as e:
            log.Error(f"Could not load OAuth2 token. Trying to create a new one. (original error: {e})")

        self.session = self.session_class(
            self.CLIENT_ID,
            scope=self.OAUTH_SCOPE,
            redirect_uri=self.OAUTH_REDIRECT_URI,
            token=token,
            auto_refresh_kwargs={
                "client_id": self.CLIENT_ID,
            },
            auto_refresh_url=self.OAUTH_TOKEN_URI,
            token_updater=self.token_updater,
        )

        # We have to refresh token manually because it's not working "under the covers"
        if token is not None:
            self.session.refresh_token(self.OAUTH_TOKEN_URI, timeout=config.timeout)

        # Send a request to make sure the token is valid (or could at least be
        # refreshed successfully, which will happen under the covers). In case
        # this request fails, the provided token was too old (i.e. expired),
        # and we need to get a new token.
        user_info_response = self.session.get(api_uri + "me", timeout=config.timeout)
        if user_info_response.status_code != 200:
            token = None

        if token is None:
            if not sys.stdout.isatty() or not sys.stdin.isatty():
                log.FatalError(
                    f"The OAuth2 token could not be loaded from {self.OAUTH_TOKEN_PATH} and you are not "
                    f"running duplicity interactively, so duplicity cannot possibly access OneDrive."
                )
            authorization_url, state = self.session.authorization_url(self.OAUTH_AUTHORIZE_URI, display="touch")

            print(
                f"\nIn order to authorize duplicity to access your OneDrive, please open {authorization_url} "
                f"in a browser and copy the URL of the blank page the dialog leads to.\n"
            )

            redirected_to = input("URL of the blank page: ").strip()

            token = self.session.fetch_token(
                self.OAUTH_TOKEN_URI,
                authorization_response=redirected_to,
                include_client_id=True,
                timeout=config.timeout,
            )

            user_info_response = self.session.get(api_uri + "me", timeout=config.timeout)
            user_info_response.raise_for_status()

            try:
                with open(self.OAUTH_TOKEN_PATH, "w") as f:
                    json.dump(token, f)
            except Exception as e:
                log.Error(
                    f"Could not save the OAuth2 token to {self.OAUTH_TOKEN_PATH}. This means you need to do the "
                    f"OAuth2 authorization process on every start of duplicity. Original error: {e}"
                )

    def token_updater(self, token):
        try:
            with open(self.OAUTH_TOKEN_PATH, "w") as f:
                json.dump(token, f)
        except Exception as e:
            log.Error(
                f"Could not save the OAuth2 token to {self.OAUTH_TOKEN_PATH}. This means you may need to do the "
                f"OAuth2 authorization process again soon. Original error: {e}"
            )


class ExternalOAuth2Session(OneDriveOAuth2Session):
    """Caller is managing tokens and provides an active refresh token."""

    def __init__(self, client_id, refresh_token):
        super().__init__()

        token = {
            "refresh_token": refresh_token,
        }

        self.session = self.session_class(
            client_id,
            token=token,
            auto_refresh_kwargs={
                "client_id": client_id,
            },
            auto_refresh_url=self.OAUTH_TOKEN_URI,
        )

        # Get an initial refresh under our belts, since we don't have an access
        # token to start with.
        self.session.refresh_token(self.OAUTH_TOKEN_URI, timeout=config.timeout)


duplicity.backend.register_backend("onedrive", OneDriveBackend)
