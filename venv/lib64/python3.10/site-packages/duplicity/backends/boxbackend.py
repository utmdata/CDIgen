# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2020 Jose L. Domingo Lopez <github@24x7linux.com>
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


import os

import duplicity.backend
from duplicity.errors import BackendException


class BoxBackend(duplicity.backend.Backend):
    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        global Client, JWTAuth
        from boxsdk import (
            Client,
            JWTAuth,
        )

        self._client = self.get_box_client(parsed_url)
        self._folder = parsed_url.path[1:] if parsed_url.path[0] == "/" else parsed_url.path

        self._file_to_metadata_map = {}
        self._folder_id = self.get_id_from_path(self._folder)
        if self._folder_id is None:
            self._folder_id = self.makedirs(self._folder)

    def get_box_client(self, parsed_url):
        try:
            config_path = os.path.expanduser(parsed_url.query_args["config"][0])
            return Client(JWTAuth.from_settings_file(config_path))
        except Exception as e:
            config_path = os.environ.get("BOX_CONFIG_PATH")
            if config_path is not None:
                try:
                    return Client(JWTAuth.from_settings_file(config_path))
                except Exception as e:
                    raise BackendException("box config file is not found.")

            raise BackendException("box config file is not specified or not found.")

    def _put(self, source_path, remote_filename):
        """Uploads file to the specified remote folder
        (tries to delete it first to make sure the new one can be uploaded)"""

        try:
            self.delete(remote_filename.decode())
        except Exception:
            pass
        self.upload(
            local_file=source_path.get_canonical().decode(),
            remote_file=remote_filename.decode(),
        )

    def _get(self, remote_filename, local_path):
        """Downloads file from the specified remote path"""

        self.download(
            remote_file=remote_filename.decode(),
            local_file=local_path.name.decode(),
        )

    def _list(self):
        """Lists files in the specified remote path"""

        return self.folder_contents()

    def _delete(self, filename):
        """Deletes file from the specified remote path"""

        self.delete(remote_file=filename.decode())

    def _query_list(self, filename_list):
        """Query metadata for a list of file"""
        return {filename: self._file_to_metadata_map.get(filename.decode(), {"size": -1}) for filename in filename_list}

    def get_id_from_path(self, remote_path, parent_id="0"):
        """Get the folder or file id from its path"""
        path_items = [x.strip() for x in remote_path.split("/") if x.strip() != ""]
        head = path_items[0]
        tail = path_items[1:]

        while True:
            selected_item_id = None
            for item in self._client.folder(folder_id=parent_id).get_items():
                if item.name == head:
                    selected_item_id = item.id
                    break

            if selected_item_id is None:
                return None
            elif len(tail) == 0:
                return selected_item_id

            parent_id = selected_item_id
            head = tail[0]
            tail = tail[1:]

        return None

    def get_file_id_from_filename(self, remote_filename):
        """Get the fild id by its file name"""
        file = self._file_to_metadata_map.get(remote_filename)

        if file is not None:
            return file["id"]

        file_id = self.get_id_from_path(remote_filename, parent_id=self._folder_id)
        file = self._client.file(file_id).get()
        self._file_to_metadata_map[file.name] = {
            "id": file.id,
            "size": file.size,
        }
        return file_id

    def makedirs(self, remote_path):
        """Create folder(s) in a path if necessary"""
        path_items = [x.strip() for x in remote_path.split("/") if x.strip() != ""]
        parent_id = "0"

        start_folder_id = None
        while len(path_items) > 0:
            selected_item_id = None
            for item in self._client.folder(folder_id=parent_id).get_items():
                if item.name == path_items[0]:
                    selected_item_id = item.id
                    break

            if selected_item_id is None:
                start_folder_id = parent_id
                break

            parent_id = selected_item_id
            path_items = path_items[1:]

        if start_folder_id is not None:
            parent_id = start_folder_id
            for item in path_items:
                subfolder = self._client.folder(parent_id).create_subfolder(item)
                parent_id = subfolder.id

        return parent_id

    def folder_contents(self):
        """Lists files of a remote box path"""

        items = [
            x
            for x in self._client.folder(folder_id=self._folder_id).get_items(fields=["id", "name", "size"])
            if x.type == "file"
        ]

        self._file_to_metadata_map.update({x.name: {"id": x.id, "size": x.size} for x in items})

        return [x.name for x in items]

    def upload(self, remote_file, local_file):
        """Upload local file to the box folder"""
        new_file = self._client.folder(self._folder_id).upload(file_path=local_file, file_name=remote_file)

        self._file_to_metadata_map[new_file.name] = {
            "id": new_file.id,
            "size": new_file.size,
        }

    def download(self, remote_file, local_file):
        """Download file in box folder"""
        file_id = self.get_file_id_from_filename(remote_file)
        with open(local_file, "wb") as fp:
            self._client.file(file_id).download_to(fp)

    def delete(self, remote_file):
        """Delete file in box folder"""
        file_id = self.get_file_id_from_filename(remote_file)
        self._client.file(file_id).delete()


duplicity.backend.register_backend("box", BoxBackend)
