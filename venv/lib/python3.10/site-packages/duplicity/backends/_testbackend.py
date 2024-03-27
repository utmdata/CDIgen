# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2002 Ben Escoto <ben@emerose.org>
# Copyright 2007 Kenneth Loafman <kenneth@loafman.com>
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

import glob
import inspect
import json
import logging
import os
import re
import time

import duplicity.backend
from duplicity import (
    log,
    path,
    progress,
)
from duplicity.errors import BackendException

ERROR_ON = {}


class BackendErrors:
    FAIL_WITH_EXCEPTION = "DUP_FAIL_WITH_EXCEPTION"  # set to substring mached by the filename.
    WAIT_FOR_OTHER_VOLUME = (
        "DUP_FAIL_WAIT_FOR_VOLUME"  # set to json string: ["file_to_delay", "file_wait_for"] (substing match)
    )
    LAST_BYTE_MISSING = "DUP_FAIL_LAST_BYTE_MISSING"  # set to substring mached by the filename.
    SKIP_PUT_SILENT = "DUP_FAIL_SKIP_PUT_SILENT"  # Don't put file contains string


class _TestBackend(duplicity.backend.Backend):
    """Use this backend to test/create certain error situations

    errors listed in global ERROR_ON get trigered.

    """

    def __init__(self, parsed_url):
        log._logger.addHandler(logging.FileHandler("/tmp/testbackend.log"))
        log.Warn("TestBackend is not made for produtcion use!")
        # The URL form "file:MyFile" is not a valid duplicity target.
        if not parsed_url.path.startswith("//"):
            raise BackendException("Bad file:// path syntax.")
        self.remote_pathdir = path.Path(parsed_url.path[2:])
        try:
            os.makedirs(self.remote_pathdir.base)
        except Exception:
            pass
        fail_env = [f"{k}={v}" for k, v in os.environ.items() if k.startswith("DUP_FAIL_")]
        log.Warn(f"ENV found: {fail_env}")

    @staticmethod
    def _fail_with_exception(filename):
        filename = os.fsdecode(filename)
        log.Debug(f"DUB_FAIL: Check if fail on exception for {filename}. Called by {inspect.stack()[2][3]}.")
        if os.getenv(BackendErrors.FAIL_WITH_EXCEPTION) and os.getenv(BackendErrors.FAIL_WITH_EXCEPTION) in filename:
            log.Warn(f"DUB_FAIL: Force exception on file {filename}.")
            raise FileNotFoundError(f"TEST: raised  exception on {filename} by intention")

    def _wait_for_other_volume(self, filename):
        filename = os.fsdecode(filename)
        log.Debug(f"DUB_FAIL: Check if action on {filename} shoud be delayed. Called by {inspect.stack()[2][3]}.")
        env = os.getenv(BackendErrors.WAIT_FOR_OTHER_VOLUME)
        if not env:
            return  # skip if env not set
        file_stop, file_waitfor = json.loads(env)
        timestamp = re.match(r".*\.(\d{8}T\d{6}[-+0-9:Z]*)\..*", filename).gorup(1)
        file_waitfor_glob = f"{os.fsdecode(self.remote_pathdir.get_canonical())}/*{timestamp}*{file_waitfor}*"
        if file_stop in filename:
            while not glob.glob(file_waitfor_glob):
                log.Warn(f"DUB_FAIL: Waiting for file matiching {file_waitfor_glob}.")
                time.sleep(1)
            log.Warn(f"DUB_FAIL: {filename} written after {glob.glob(file_waitfor_glob)}")

    def _remove_last_byte(self, filename):
        filename = os.fsdecode(filename)
        log.Debug(f"DUB_FAIL: Check if {filename} shoud be truncated. Called by {inspect.stack()[2][3]}.")
        if os.getenv(BackendErrors.LAST_BYTE_MISSING) and os.getenv(BackendErrors.LAST_BYTE_MISSING) in filename:
            log.Warn(f"DUB_FAIL: removing last byte from {filename}")
            with open(self.remote_pathdir.append(filename).get_canonical(), "ab") as remote_file:
                remote_file.seek(-1, os.SEEK_END)
                remote_file.truncate()

    @staticmethod
    def _skip_put_silent(filename):
        """
        retrun true if file should be skipped silently
        """
        filename = os.fsdecode(filename)
        log.Debug(f"DUB_FAIL: Check if {filename} should be skipped. Called by {inspect.stack()[2][3]}.")
        if os.getenv(BackendErrors.SKIP_PUT_SILENT) and os.getenv(BackendErrors.SKIP_PUT_SILENT) in filename:
            log.Warn(f"DUB_FAIL: {filename} skipped silent.")
            return True
        return False

    def _move(self, source_path, remote_filename):
        self._fail_with_exception(remote_filename)
        self._wait_for_other_volume(remote_filename)
        target_path = self.remote_pathdir.append(remote_filename)
        try:
            source_path.rename(target_path)
            return True
        except OSError:
            return False

    def _put(self, source_path, remote_filename):
        self._fail_with_exception(remote_filename)
        self._wait_for_other_volume(remote_filename)
        if self._skip_put_silent(remote_filename):
            return
        target_path = self.remote_pathdir.append(remote_filename)
        source_path.setdata()
        source_size = source_path.getsize()
        progress.report_transfer(0, source_size)
        target_path.writefileobj(source_path.open("rb"))

        self._remove_last_byte(remote_filename)

        progress.report_transfer(source_size, source_size)

    def _get(self, filename, local_path):
        self._fail_with_exception(filename)
        source_path = self.remote_pathdir.append(filename)
        local_path.writefileobj(source_path.open("rb"))

    def _list(self):
        return self.remote_pathdir.listdir()

    def _delete(self, filename):
        self._fail_with_exception(filename)
        self.remote_pathdir.append(filename).delete()

    def _delete_list(self, filenames):
        for filename in filenames:
            self._fail_with_exception(filename)
            self.remote_pathdir.append(filename).delete()

    def _query(self, filename):
        self._fail_with_exception(filename)
        target_file = self.remote_pathdir.append(filename)
        target_file.setdata()
        size = target_file.getsize() if target_file.exists() else -1
        return {"size": size}


duplicity.backend.register_backend("fortestsonly", _TestBackend)
