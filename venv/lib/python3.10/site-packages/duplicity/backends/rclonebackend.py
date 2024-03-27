# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2019 Francesco Magno
# Copyright 2019 Kenneth Loafman <kenneth@loafman.com>
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
import os.path

import duplicity.backend
from duplicity import log
from duplicity.errors import BackendException


class RcloneBackend(duplicity.backend.Backend):
    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)
        self.parsed_url = parsed_url
        self.remote_path = self.parsed_url.path
        self.rclone_cmd = "rclone"

        try:
            rc, o, e = self._subprocess_safe_popen(f"{self.rclone_cmd} version")
        except Exception:
            log.FatalError("rclone not found: please install rclone", log.ErrorCode.backend_error)

        verb = log.getverbosity()
        if verb >= log.DEBUG:
            os.environ["RCLONE_LOG_LEVEL"] = "DEBUG"
        elif verb >= log.INFO:
            os.environ["RCLONE_LOG_LEVEL"] = "INFO"
        elif verb >= log.NOTICE:
            os.environ["RCLONE_LOG_LEVEL"] = "NOTICE"
        elif verb >= log.ERROR:
            os.environ["RCLONE_LOG_LEVEL"] = "ERROR"

        if parsed_url.path.startswith("//"):
            self.remote_path = self.remote_path[2:].replace(":/", ":", 1)

        self.remote_path = os.fsdecode(self.remote_path)

    def _get(self, remote_filename, local_path):
        remote_filename = os.fsdecode(remote_filename)
        local_pathname = os.fsdecode(local_path.name)
        commandline = f"{self.rclone_cmd} copyto '{self.remote_path}/{remote_filename}' '{local_pathname}'"
        rc, o, e = self._subprocess_safe_popen(commandline)
        if rc != 0:
            if os.path.isfile(local_pathname):
                os.remove(local_pathname)
            raise BackendException(f"rclone returned rc = {int(rc)}: {e}")

    def _put(self, source_path, remote_filename):
        source_pathname = os.fsdecode(source_path.name)
        remote_filename = os.fsdecode(remote_filename)
        commandline = f"{self.rclone_cmd} copyto '{source_pathname}' '{self.remote_path}/{remote_filename}'"
        rc, o, e = self._subprocess_safe_popen(commandline)
        if rc != 0:
            raise BackendException(f"rclone returned rc = {int(rc)}: {e}")

    def _list(self):
        filelist = []
        commandline = f"{self.rclone_cmd} lsf '{self.remote_path}'"
        rc, o, e = self._subprocess_safe_popen(commandline)
        if rc == 3:
            return filelist
        if rc != 0:
            raise BackendException(f"rclone returned rc = {int(rc)}: {e}")
        if not o:
            return filelist
        return [os.fsencode(x) for x in o.split("\n") if x]

    def _delete(self, remote_filename):
        remote_filename = os.fsdecode(remote_filename)
        commandline = f"{self.rclone_cmd} deletefile --drive-use-trash=false '{self.remote_path}/{remote_filename}'"
        rc, o, e = self._subprocess_safe_popen(commandline)
        if rc != 0:
            raise BackendException(f"rclone returned rc = {int(rc)}: {e}")

    def _subprocess_safe_popen(self, commandline):
        import shlex
        from subprocess import (
            Popen,
            PIPE,
        )

        args = shlex.split(commandline)
        p = Popen(args, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        for l in stderr.split("\n"):
            if len(l) > 1:
                print(l)
        return p.returncode, stdout, stderr


duplicity.backend.register_backend("rclone", RcloneBackend)
