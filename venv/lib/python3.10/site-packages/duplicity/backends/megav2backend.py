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
import re
import subprocess

import duplicity.backend
from duplicity.errors import BackendException


class Megav2Backend(duplicity.backend.Backend):
    """Backend for MEGA.nz cloud storage, only one that works for accounts created since Nov. 2018
    See https://github.com/megous/megatools/issues/411 for more details

    This MEGA backend resorts to official tools (MEGAcmd) as available at https://mega.nz/cmd
    MEGAcmd works through a single binary called "mega-cmd", which talks to a backend server
    "mega-cmd-server", which keeps state (for example, persisting a session). Multiple "mega-*"
    shell wrappers (ie. "mega-ls") exist as the user interface to "mega-cmd" and MEGA API
    The full MEGAcmd User Guide can be found in the software's GitHub page below :
    https://github.com/meganz/MEGAcmd/blob/master/UserGuide.md"""

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        # Sanity check : ensure all the necessary "MEGAcmd" binaries exist
        self._check_binary_exists("mega-login")
        self._check_binary_exists("mega-logout")
        self._check_binary_exists("mega-cmd")
        self._check_binary_exists("mega-cmd-server")
        self._check_binary_exists("mega-ls")
        self._check_binary_exists("mega-mkdir")
        self._check_binary_exists("mega-get")
        self._check_binary_exists("mega-put")
        self._check_binary_exists("mega-rm")

        # "MEGAcmd" does not use a config file, however it is handy to keep one (with the old ".megarc" format) to
        # securely store the username and password
        self._hostname = parsed_url.hostname
        if parsed_url.password is None:
            self._megarc = f"{os.getenv('HOME')}/.megav2rc"
            try:
                conf_file = open(self._megarc, "r")
            except Exception as e:
                raise BackendException(
                    f"No password provided in URL and MEGA configuration file for "
                    f"duplicity does not exist as '{self._megarc}'"
                )

            myvars = {}
            for line in conf_file:
                name, var = line.partition("=")[::2]
                myvars[name.strip()] = str(var.strip())
            conf_file.close()
            self._username = myvars["Username"]
            self._password = myvars["Password"]

        else:
            self._username = parsed_url.username
            self._password = self.get_password()

        # Remote folder ("MEGAcmd" no longer shows "Root/" at the top of the hierarchy)
        self._folder = f"/{parsed_url.path[1:]}"

        # Only create the remote folder if it doesn't exist yet
        self.mega_login()
        cmd = ["mega-ls", self._folder]
        try:
            self.subprocess_popen(cmd)
        except Exception as e:
            self._makedir(self._folder)

    def _check_binary_exists(self, cmd):
        """Checks that a specified command exists in the running user command path"""

        try:
            # Ignore the output, as we only need the return code
            subprocess.check_output(["which", cmd])
        except Exception as e:
            raise BackendException(
                f"Command '{cmd}' not found, make sure 'MEGAcmd' tools (https://mega.nz/cmd) "
                f"is properly installed and in the running user command path"
            )

    def _makedir(self, path):
        """Creates a remote directory (recursively if necessary)"""

        self.mega_login()
        cmd = ["mega-mkdir", "-p", path]
        try:
            self.subprocess_popen(cmd)
        except Exception as e:
            error_str = str(e)
            if "Folder already exists" in error_str:
                raise BackendException(
                    f"Folder '{path}' could not be created on MEGA because it already exists. "
                    f"Use another path or remove the folder in MEGA manually"
                )
            else:
                raise BackendException(f"Folder '{path}' could not be created, reason : '{e}'")

    def _put(self, source_path, remote_filename):
        """Uploads file to the specified remote folder (tries to delete it first to make
        sure the new one can be uploaded)"""

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

        self.download(remote_file=remote_filename.decode(), local_file=local_path.name.decode())

    def _list(self):
        """Lists files in the specified remote path"""

        return self.folder_contents(files_only=True)

    def _delete(self, filename):
        """Deletes file from the specified remote path"""

        self.delete(remote_file=filename.decode())

    def _close(self):
        """Function called when backend is done being used"""

        cmd = ["mega-logout"]
        self.subprocess_popen(cmd)

    def mega_login(self):
        """Helper function to call from each method interacting with MEGA to make
        sure a session already exists or one is created to start with"""

        # Abort if command doesn't return in a reasonable time (somehow "mega-session" sometimes
        # doesn't return), and create session if one doesn't exist yet
        try:
            subprocess.check_output("mega-session", timeout=30)
        except subprocess.TimeoutExpired:
            raise BackendException("Timed out while trying to determine if a MEGA session exists")
        except Exception as e:
            cmd = ["mega-login", self._username, self._password]
            try:
                subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
            except Exception as e:
                raise BackendException(f"Could not log in to MEGA, error : '{e}'")

    def folder_contents(self, files_only=False):
        """Lists contents of a remote MEGA path, optionally ignoring subdirectories"""

        cmd = ["mega-ls", "-l", self._folder]

        self.mega_login()
        files = subprocess.check_output(cmd)
        files = files.decode().split("\n")

        # Optionally ignore directories
        if files_only:
            files = [f.split()[5] for f in files if re.search("^-", f)]

        return files

    def download(self, remote_file, local_file):
        """Downloads a file from a remote MEGA path"""

        cmd = ["mega-get", f"{self._folder}/{remote_file}", local_file]
        self.mega_login()
        self.subprocess_popen(cmd)

    def upload(self, local_file, remote_file):
        """Uploads a file to a remote MEGA path"""

        cmd = ["mega-put", local_file, f"{self._folder}/{remote_file}"]
        self.mega_login()
        try:
            self.subprocess_popen(cmd)
        except Exception as e:
            error_str = str(e)
            if "Reached storage quota" in error_str:
                raise BackendException(
                    f"MEGA account over quota, could not write file : '{remote_file}'. "
                    f"Upgrade your storage at https://mega.nz/pro or remove some data."
                )
            else:
                raise BackendException(f"Failed writing file '{remote_file}' to MEGA, reason : '{e}'")

    def delete(self, remote_file):
        """Deletes a file from a remote MEGA path"""

        cmd = ["mega-rm", "-f", f"{self._folder}/{remote_file}"]
        self.mega_login()
        self.subprocess_popen(cmd)


duplicity.backend.register_backend("megav2", Megav2Backend)
duplicity.backend.uses_netloc.extend(["megav2"])
