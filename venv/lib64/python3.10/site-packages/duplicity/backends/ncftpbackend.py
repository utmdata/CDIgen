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

import os.path
import re
import urllib.error
import urllib.parse
import urllib.request

import duplicity.backend
from duplicity import config
from duplicity import log
from duplicity import tempdir


class NCFTPBackend(duplicity.backend.Backend):
    """Connect to remote store using File Transfer Protocol"""

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        # we expect an error return, so go low-level and ignore it
        try:
            p = os.popen("ncftpls -v")
            fout = p.read()
            ret = p.close()
        except Exception:
            pass
        # the expected error is 8 in the high-byte and some output
        if ret != 0x0800 or not fout:
            log.FatalError(
                "NcFTP not found:  Please install NcFTP version 3.1.9 or later",
                log.ErrorCode.ftp_ncftp_missing,
            )

        # version is the second word of the first line
        version = fout.split("\n")[0].split()[1]
        if version < "3.1.9":
            log.FatalError(
                "NcFTP too old:  Duplicity requires NcFTP version 3.1.9,"
                "3.2.1 or later.  Version 3.2.0 will not work properly.",
                log.ErrorCode.ftp_ncftp_too_old,
            )
        elif version == "3.2.0":
            log.Warn(
                "NcFTP (ncftpput) version 3.2.0 may fail with duplicity.\n"
                "see: http://www.ncftpd.com/ncftp/doc/changelog.html\n"
                "If you have trouble, please upgrade to 3.2.1 or later",
                log.WarningCode.ftp_ncftp_v320,
            )
        log.Notice(f"NcFTP version is {version}")

        self.parsed_url = parsed_url

        self.url_string = duplicity.backend.strip_auth_from_url(self.parsed_url)

        # strip ncftp+ prefix
        self.url_string = duplicity.backend.strip_prefix(self.url_string, "ncftp")

        # This squelches the "file not found" result from ncftpls when
        # the ftp backend looks for a collection that does not exist.
        # version 3.2.2 has error code 5, 1280 is some legacy value
        self.popen_breaks["ncftpls"] = [5, 1280]

        # Use an explicit directory name.
        if self.url_string[-1] != "/":
            self.url_string += "/"

        self.password = self.get_password()

        if config.ftp_connection == "regular":
            self.conn_opt = "-E"
        else:
            self.conn_opt = "-F"

        self.tempfd, self.tempname = tempdir.default().mkstemp()
        self.tempfile = os.fdopen(self.tempfd, "w")
        self.tempfile.write(f"host {self.parsed_url.hostname}\n")
        self.tempfile.write(f"user {self.parsed_url.username}\n")
        self.tempfile.write(f"pass {self.password}\n")
        self.tempfile.close()
        self.flags = f"-f {self.tempname} {self.conn_opt} -t {config.timeout} -o useCLNT=0,useHELP_SITE=0 "
        if parsed_url.port is not None and parsed_url.port != 21:
            self.flags += f" -P '{parsed_url.port}'"

    def _put(self, source_path, remote_filename):
        remote_filename = os.fsdecode(remote_filename)
        remote_path = os.path.join(
            urllib.parse.unquote(re.sub("^/", "", self.parsed_url.path)),
            remote_filename,
        ).rstrip()
        commandline = f"ncftpput {self.flags} -m -V -C '{source_path.uc_name}' '{remote_path}'"
        self.subprocess_popen(commandline)

    def _get(self, remote_filename, local_path):
        remote_filename = os.fsdecode(remote_filename)
        remote_path = os.path.join(
            urllib.parse.unquote(re.sub("^/", "", self.parsed_url.path)),
            remote_filename,
        ).rstrip()
        commandline = (
            f"ncftpget {self.flags} -V -C '{self.parsed_url.hostname}' "
            f"'{remote_path.lstrip('/')}' '{local_path.uc_name}'"
        )
        self.subprocess_popen(commandline)

    def _list(self):
        # Do a long listing to avoid connection reset
        commandline = f"ncftpls {self.flags} -l '{self.url_string}'"
        _, l, _ = self.subprocess_popen(commandline)
        # Look for our files as the last element of a long list line
        return [os.fsencode(x.split()[-1]) for x in l.split("\n") if x and not x.startswith("total ")]

    def _delete(self, filename):
        commandline = f"ncftpls {self.flags} -l -X 'DELE {filename}' '{self.url_string}'"
        self.subprocess_popen(commandline)


duplicity.backend.register_backend("ncftp+ftp", NCFTPBackend)
duplicity.backend.uses_netloc.extend(["ncftp+ftp"])
