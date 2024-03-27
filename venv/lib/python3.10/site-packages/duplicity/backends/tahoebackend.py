# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2008 Francois Deppierraz
#
# This file is part of duplicity.
#
# Duplicity is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
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
from duplicity import log


class TAHOEBackend(duplicity.backend.Backend):
    """
    Backend for the Tahoe file system
    """

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        url = parsed_url.path.strip("/").split("/")

        self.alias = url[0]

        if len(url) > 1:
            self.directory = "/".join(url[1:])
        else:
            self.directory = ""

        log.Debug(f"tahoe: {url} -> {self.alias}:{self.directory}")

    def get_remote_path(self, filename=None):
        if filename is None:
            if self.directory != "":
                return f"{self.alias}:{self.directory}"
            else:
                return f"{self.alias}:"

        if isinstance(filename, bytes):
            filename = os.fsdecode(filename)
        if self.directory != "":
            return f"{self.alias}:{self.directory}/{filename}"
        else:
            return f"{self.alias}:{filename}"

    def run(self, *args):
        cmd = " ".join(args)
        _, output, _ = self.subprocess_popen(cmd)
        return output

    def _put(self, source_path, remote_filename):
        self.run("tahoe", "cp", source_path.uc_name, self.get_remote_path(remote_filename))

    def _get(self, remote_filename, local_path):
        self.run("tahoe", "cp", self.get_remote_path(remote_filename), local_path.uc_name)

    def _list(self):
        output = self.run("tahoe", "ls", self.get_remote_path())
        return [os.fsencode(x) for x in output.split("\n") if x]

    def _delete(self, filename):
        self.run("tahoe", "rm", self.get_remote_path(filename))


duplicity.backend.register_backend("tahoe", TAHOEBackend)
