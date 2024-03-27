# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2021 Syeam Bin Abdullah <syeamtechdemon@gmail.com>
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
import shutil
import urllib.request
from pathlib import Path

import requests

import duplicity.backend
from duplicity import log
from duplicity.errors import BackendException


class SlateBackend(duplicity.backend.Backend):
    """
    Backend for Slate
    """

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)
        log.Debug("loading slate backend...")
        if "SLATE_API_KEY" not in os.environ.keys():
            raise BackendException(
                """You must set an environment variable SLATE_API_KEY
                as the value of your slate API key"""
            )
        else:
            self.key = os.environ["SLATE_API_KEY"]

        if "SLATE_SSL_VERIFY" not in os.environ.keys():
            self.verify = True
        else:
            if "SLATE_SSL_VERIFY" == "0":
                self.verify = False
            else:
                self.verify = True

        data = json.dumps({"data": {"private": "true"}})
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.key}",
        }

        response = requests.post(
            "https://slate.host/api/v1/get",
            data=data,
            headers=headers,
            verify=self.verify,
        )
        if not response.ok:
            raise BackendException("Slate backend requires a valid API key")

        self.slate_id = parsed_url.geturl().split("/")[-1]

    def _put(self, source_path, remote_filename):
        data = json.dumps({"data": {"private": "true"}})
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.key}",
        }

        log.Debug(f"source_path.name: {str(source_path.name)}")
        log.Debug(f"remote_filename: {remote_filename.decode('utf8')}")
        rem_filename = str(os.fsdecode(remote_filename))

        src = Path(os.fsdecode(source_path.name))
        if str(src.name).startswith("mktemp"):
            log.Debug("copying temp file for upload")
            src = shutil.move(str(src), str(src.with_name(rem_filename)))

        log.Debug("response")
        headers = {"Authorization": f"Basic {self.key}"}
        files = {rem_filename: open(str(src), "rb")}
        log.Debug(f"-------------------FILECHECK: {str(files.keys())}")
        response = requests.post(
            url=f"https://uploads.slate.host/api/public/{self.slate_id}",
            files=files,
            headers=headers,
        )
        log.Debug("response handled")

        if not response.ok:
            raise BackendException(f"An error occurred whilst attempting to upload a file: {response}")
        else:
            log.Debug(f"File successfully uploaded to slate with id:{self.slate_id}")

        if str(src).endswith("difftar.gpg"):
            os.remove(str(src))

    def _list(self):
        # Checks if a specific slate has been selected, otherwise lists all slates
        log.Debug(f"Slate ID: {self.slate_id}")
        data = json.dumps({"data": {"private": "true"}})
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.key}",
        }
        response = requests.post(
            "https://slate.host/api/v1/get",
            data=data,
            headers=headers,
            verify=self.verify,
        )

        if not response.ok:
            raise BackendException("Slate backend requires a valid API key")

        slates = response.json()["slates"]
        # log.Debug("SLATES:\n%s"%(slates))
        file_list = []
        for slate in slates:
            if slate["id"] == self.slate_id:
                files = slate["data"]["objects"]
                for f in files:
                    file_list.append(f["name"])
            else:
                log.Debug(f"Could not find slate with id: {self.slate_id}")

        return file_list

    def _get(self, remote_filename, local_path):
        # Downloads chosen file from IPFS by parsing its cid
        found = False
        data = json.dumps({"data": {"private": "true"}})
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.key}",
        }

        response = requests.post(
            "https://slate.host/api/v1/get",
            data=data,
            headers=headers,
            verify=self.verify,
        )

        slates = response.json()["slates"]
        # file_list = self._list()

        # if remote_filename not in file_list:
        #     raise BackendException(u"The chosen file does not exist in the chosen slate")

        for slate in slates:
            if slate["id"] == self.slate_id:
                found = True
                for obj in slate["data"]["objects"]:
                    if obj["name"] == remote_filename.decode("utf8"):
                        cid = obj["url"].split("/")[-1]
                        break
                    else:
                        raise BackendException(
                            "The file '"
                            + remote_filename.decode("utf8")
                            + "' could not be found in the specified slate"
                        )

        if not found:
            raise BackendException(f"A slate with id {self.slate_id} does not exist")

        try:
            urllib.request.urlretrieve(f"http://ipfs.io/ipfs/{cid}", os.fsdecode(local_path.name))
            log.Debug(f"Downloaded file with cid: {cid}")
        except NameError as e:
            raise BackendException("Couldn't download file")


duplicity.backend.register_backend("slate", SlateBackend)
