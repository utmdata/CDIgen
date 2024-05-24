# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright (c) 2015 Matthew Bentley
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
from urllib.parse import quote_plus

import duplicity.backend
from duplicity import config
from duplicity import log
from duplicity import progress
from duplicity import util
from duplicity import config
from duplicity.errors import (
    BackendException,
    FatalBackendException,
)


class B2ProgressListener(object):
    def __enter__(self):
        pass

    def set_total_bytes(self, total_byte_count):
        self.total_byte_count = total_byte_count

    def bytes_completed(self, byte_count):
        progress.report_transfer(byte_count, self.total_byte_count)

    def close(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class B2Backend(duplicity.backend.Backend):
    """
    Backend for BackBlaze's B2 storage service
    """

    def __init__(self, parsed_url):
        """
        Authorize to B2 api and set up needed variables
        """
        duplicity.backend.Backend.__init__(self, parsed_url)

        global DownloadDestLocalFile, FileVersionInfoFactory

        try:  # figure out what version of b2sdk we have
            from b2sdk import __version__ as VERSION  # pylint: disable=import-error

            v_split = VERSION.split(".")
            self.v_num = [int(x) for x in v_split]
        except Exception as e:
            self.v_num = [0, 0, 0]

        try:  # public API v2 is recommended, if available
            from b2sdk.v2 import B2Api  # pylint: disable=import-error
            from b2sdk.v2 import InMemoryAccountInfo  # pylint: disable=import-error
            from b2sdk.v2.exception import (
                NonExistentBucket,
            )  # pylint: disable=import-error
        except ImportError:
            try:  # if public API v2 not found, try to use public API v1
                from b2sdk.v1 import B2Api  # pylint: disable=import-error
                from b2sdk.v1 import InMemoryAccountInfo  # pylint: disable=import-error
                from b2sdk.v1 import (
                    DownloadDestLocalFile,
                )  # pylint: disable=import-error
                from b2sdk.v1.exception import (
                    NonExistentBucket,
                )  # pylint: disable=import-error

                if self.v_num < [1, 9, 0]:
                    from b2sdk.v1.file_version import FileVersionInfoFactory
            except ImportError:
                try:  # try to import the new b2sdk internal API if available (and public API isn't)
                    from b2sdk.api import B2Api  # pylint: disable=import-error
                    from b2sdk.account_info import (
                        InMemoryAccountInfo,
                    )  # pylint: disable=import-error
                    from b2sdk.download_dest import (
                        DownloadDestLocalFile,
                    )  # pylint: disable=import-error
                    from b2sdk.exception import (
                        NonExistentBucket,
                    )  # pylint: disable=import-error
                    from b2sdk.file_version import (
                        FileVersionInfoFactory,
                    )  # pylint: disable=import-error
                except ImportError as e:
                    raise BackendException("B2 backend requires B2 Python SDK (pip install b2sdk)")

        self.service = B2Api(InMemoryAccountInfo())
        self.parsed_url.hostname = "B2"

        account_id = parsed_url.username
        account_key = self.get_password()

        self.url_parts = [x for x in parsed_url.path.replace("@", "/").split("/") if x != ""]
        if self.url_parts:
            self.username = self.url_parts.pop(0)
            bucket_name = self.url_parts.pop(0)
        else:
            raise BackendException("B2 requires a bucket name")
        self.path = "".join([f"{url_part}/" for url_part in self.url_parts])
        self.service.authorize_account("production", account_id, account_key)

        try:
            log.Log(
                f"B2 Backend (path= {self.path}, bucket= {bucket_name}, "
                f"recommended_part_size= {self.service.account_info.get_recommended_part_size()})",
                log.INFO,
            )
        except AttributeError:
            log.Log(
                f"B2 Backend (path= {self.path}, bucket= {bucket_name}, "
                f"minimum_part_size= {self.service.account_info.get_minimum_part_size()})",
                log.INFO,
            )

        try:
            self.bucket = self.service.get_bucket_by_name(bucket_name)
            log.Log("Bucket found", log.INFO)
        except NonExistentBucket:
            try:
                log.Log("Bucket not found, creating one", log.INFO)
                self.bucket = self.service.create_bucket(bucket_name, "allPrivate")
            except Exception as e:
                raise FatalBackendException("Bucket cannot be created")

    def _get(self, remote_filename, local_path):
        """
        Download remote_filename to local_path
        """
        log.Log(
            f"Get: {self.path + os.fsdecode(remote_filename)} -> {os.fsdecode(local_path.name)}",
            log.INFO,
        )
        if self.v_num < [1, 11, 0]:
            self.bucket.download_file_by_name(
                quote_plus(self.path + os.fsdecode(remote_filename), "/"),
                DownloadDestLocalFile(local_path.name),
            )
        else:
            df = self.bucket.download_file_by_name(quote_plus(self.path + os.fsdecode(remote_filename), "/"))
            try:
                # b2sdk >= 1.19.0
                df.save_to(local_path.uc_name)
            except Exception as e:
                # b2sdk < 1.19.0
                df.save_to(local_path.name)

    def _put(self, source_path, remote_filename):
        """
        Copy source_path to remote_filename
        """
        log.Log(
            f"Put: {os.fsdecode(source_path.name)} -> {self.path + os.fsdecode(remote_filename)}",
            log.INFO,
        )
        self.bucket.upload_local_file(
            os.fsdecode(source_path.name),
            quote_plus(self.path + os.fsdecode(remote_filename), "/"),
            content_type="application/pgp-encrypted",
            progress_listener=B2ProgressListener(),
        )

    def _list(self):
        """
        List files on remote server
        """
        return [
            file_version_info.file_name[len(self.path) :]
            for (file_version_info, folder_name) in self.bucket.ls(self.path)
        ]

    def _delete(self, filename):
        """
        Delete filename from remote server
        """
        full_filename = self.path + os.fsdecode(filename)
        log.Log(f"Delete: {full_filename}", log.INFO)

        if config.b2_hide_files:
            self.bucket.hide_file(full_filename)
        else:
            file_version_info = self.file_info(quote_plus(full_filename, "/"))
            self.bucket.delete_file_version(file_version_info.id_, file_version_info.file_name)

    def _query(self, filename):
        """
        Get size info of filename
        """
        log.Log(f"Query: {self.path}{os.fsdecode(filename)}", log.INFO)
        file_version_info = self.file_info(quote_plus(self.path + os.fsdecode(filename), "/"))
        return {
            "size": int(file_version_info.size)
            if file_version_info is not None and file_version_info.size is not None
            else -1
        }

    def file_info(self, filename):
        if self.v_num >= [1, 9, 0]:
            return self.bucket.get_file_info_by_name(filename)
        else:
            response = self.bucket.api.session.list_file_names(self.bucket.id_, filename, 1, self.path)
            for entry in response["files"]:
                file_version_info = FileVersionInfoFactory.from_api_response(entry)
                if file_version_info.file_name == filename:
                    return file_version_info
            raise BackendException("File not found")


duplicity.backend.register_backend("b2", B2Backend)
