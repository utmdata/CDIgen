# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2002 Ben Escoto <ben@emerose.org>
# Copyright 2007 Kenneth Loafman <kenneth@loafman.com>
# Copyright 2010 Marcel Pennewiss <opensource@pennewiss.de>
# Copyright 2014 Edgar Soldin
#                 - webdav, fish, sftp support
#                 - https cert verification switches
#                 - debug output
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
import re
import urllib.error
import urllib.parse
import urllib.request

try:
    from shlex import quote as cmd_quote
except ImportError:
    from pipes import quote as cmd_quote

import duplicity.backend
from duplicity import config
from duplicity import log
from duplicity import tempdir


class LFTPBackend(duplicity.backend.Backend):
    """Connect to remote store using File Transfer Protocol"""

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        # we expect an output
        try:
            p = os.popen("lftp --version")
            fout = p.read()
            ret = p.close()
        except Exception:
            pass
        # there is no output if lftp not found
        if not fout:
            log.FatalError("LFTP not found:  Please install LFTP.", log.ErrorCode.ftps_lftp_missing)

        # version is the second word of the second part of the first line
        version = fout.split("\n")[0].split(" | ")[1].split()[1]
        log.Notice(f"LFTP version is {version}")

        self.parsed_url = parsed_url

        self.scheme = duplicity.backend.strip_prefix(parsed_url.scheme, "lftp").lower()
        self.scheme = re.sub("^webdav", "http", self.scheme)
        self.url_string = f"{self.scheme}://{parsed_url.hostname}"
        if parsed_url.port:
            self.url_string += f":{parsed_url.port}"

        self.remote_path = re.sub("^/", "", parsed_url.path)

        # Fix up an empty remote path
        if len(self.remote_path) == 0:
            self.remote_path = "/"

        # Use an explicit directory name.
        if self.remote_path[-1] != "/":
            self.remote_path += "/"

        self.authflag = ""
        if self.parsed_url.username:
            self.username = self.parsed_url.username
            self.password = self.get_password()
            self.authflag = f"-u '{self.username},{self.password}'"

        if config.ftp_connection == "regular":
            self.conn_opt = "off"
        else:
            self.conn_opt = "on"

        # check for cacert file if https
        self.cacert_file = config.ssl_cacert_file
        if self.scheme == "https" and not config.ssl_no_check_certificate:
            cacert_candidates = ["~/.duplicity/cacert.pem", "~/duplicity_cacert.pem", "/etc/duplicity/cacert.pem"]
            # look for a default cacert file
            if not self.cacert_file:
                for path in cacert_candidates:
                    path = os.path.expanduser(path)
                    if os.path.isfile(path):
                        self.cacert_file = path
                        break

        # save config into a reusable temp file
        self.tempfd, self.tempname = tempdir.default().mkstemp()
        self.tempfile = os.fdopen(self.tempfd, "w")
        self.tempfile.write(
            "set ssl:verify-certificate " + ("false" if config.ssl_no_check_certificate else "true") + "\n"
        )
        if self.cacert_file:
            self.tempfile.write(f"set ssl:ca-file {cmd_quote(self.cacert_file)}\n")
        if config.ssl_cacert_path:
            self.tempfile.write(f"set ssl:ca-path {cmd_quote(config.ssl_cacert_path)}\n")
        if self.parsed_url.scheme == "ftps":
            self.tempfile.write("set ftp:ssl-allow true\n")
            self.tempfile.write("set ftp:ssl-protect-data true\n")
            self.tempfile.write("set ftp:ssl-protect-list true\n")
        elif self.parsed_url.scheme == "ftpes":
            self.tempfile.write("set ftp:ssl-force on\n")
            self.tempfile.write("set ftp:ssl-protect-data on\n")
            self.tempfile.write("set ftp:ssl-protect-list on\n")
        else:
            self.tempfile.write("set ftp:ssl-allow false\n")
        self.tempfile.write("set http:use-propfind true\n")
        self.tempfile.write(f"set net:timeout {config.timeout}\n")
        self.tempfile.write(f"set net:max-retries {config.num_retries}\n")
        self.tempfile.write(f"set ftp:passive-mode {self.conn_opt}\n")
        if log.getverbosity() >= log.DEBUG:
            self.tempfile.write("debug\n")
        if self.parsed_url.scheme == "ftpes":
            self.tempfile.write(f"open {self.authflag} {self.url_string.replace('ftpes', 'ftp')}\n")
        else:
            self.tempfile.write(f"open {self.authflag} {self.url_string}\n")
        self.tempfile.close()
        # print settings in debug mode
        if log.getverbosity() >= log.DEBUG:
            f = open(self.tempname, "r")
            log.Debug(f"SETTINGS: \n{f.read()}")

    def _put(self, source_path, remote_filename):
        if isinstance(remote_filename, bytes):
            remote_filename = os.fsdecode(remote_filename)
        commandline = (
            f'lftp -c "source {self.tempname}; mkdir -p -f {cmd_quote(self.remote_path)}; '
            f"put {cmd_quote(source_path.uc_name)} "
            f'-o {cmd_quote(self.remote_path) + os.fsdecode(remote_filename)}"'
        )
        log.Debug(f"CMD: {commandline}")
        s, l, e = self.subprocess_popen(commandline)
        log.Debug(f"STATUS: {s}")
        log.Debug(f"STDERR:\n{e}")
        log.Debug(f"STDOUT:\n{l}")

    def _get(self, remote_filename, local_path):
        if isinstance(remote_filename, bytes):
            remote_filename = os.fsdecode(remote_filename)
        commandline = (
            f'lftp -c "source {cmd_quote(self.tempname)}; '
            f"get {cmd_quote(self.remote_path) + remote_filename} "
            f'-o {cmd_quote(local_path.uc_name)}"'
        )
        log.Debug(f"CMD: {commandline}")
        _, l, e = self.subprocess_popen(commandline)
        log.Debug(f"STDERR:\n{e}")
        log.Debug(f"STDOUT:\n{l}")

    def _list(self):
        # Do a long listing to avoid connection reset
        # remote_dir = urllib.unquote(self.parsed_url.path.lstrip('/')).rstrip()
        remote_dir = urllib.parse.unquote(self.parsed_url.path)
        # print remote_dir
        quoted_path = cmd_quote(self.remote_path)
        # failing to cd into the folder might be because it was not created already
        commandline = (
            f'lftp -c "source {cmd_quote(self.tempname)}; ( cd {quoted_path} && ls ) || '
            f'( mkdir -p -f {quoted_path} && cd {quoted_path} && ls )"'
        )
        log.Debug(f"CMD: {commandline}")
        _, l, e = self.subprocess_popen(commandline)
        log.Debug(f"STDERR:\n{e}")
        log.Debug(f"STDOUT:\n{l}")

        # Look for our files as the last element of a long list line
        return [os.fsencode(x.split()[-1]) for x in l.split("\n") if x]

    def _delete(self, filename):
        commandline = (
            f'lftp -c "source {cmd_quote(self.tempname)}; cd {cmd_quote(self.remote_path)}; '
            f'rm {cmd_quote(os.fsdecode(filename))}"'
        )
        log.Debug(f"CMD: {commandline}")
        _, l, e = self.subprocess_popen(commandline)
        log.Debug(f"STDERR:\n{e}")
        log.Debug(f"STDOUT:\n{l}")


duplicity.backend.register_backend("ftp", LFTPBackend)
duplicity.backend.register_backend("ftps", LFTPBackend)
duplicity.backend.register_backend("fish", LFTPBackend)
duplicity.backend.register_backend("ftpes", LFTPBackend)

duplicity.backend.register_backend("lftp+ftp", LFTPBackend)
duplicity.backend.register_backend("lftp+ftps", LFTPBackend)
duplicity.backend.register_backend("lftp+fish", LFTPBackend)
duplicity.backend.register_backend("lftp+ftpes", LFTPBackend)
duplicity.backend.register_backend("lftp+sftp", LFTPBackend)
duplicity.backend.register_backend("lftp+webdav", LFTPBackend)
duplicity.backend.register_backend("lftp+webdavs", LFTPBackend)
duplicity.backend.register_backend("lftp+http", LFTPBackend)
duplicity.backend.register_backend("lftp+https", LFTPBackend)

duplicity.backend.uses_netloc.extend(
    [
        "ftp",
        "ftps",
        "fish",
        "ftpes",
        "lftp+ftp",
        "lftp+ftps",
        "lftp+fish",
        "lftp+ftpes",
        "lftp+sftp",
        "lftp+webdav",
        "lftp+webdavs",
        "lftp+http",
        "lftp+https",
    ]
)
