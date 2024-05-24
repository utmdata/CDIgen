# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2002 Ben Escotoben@emerose.org>
# Copyright 2007 Kenneth Loafman <kenneth@loafman.com>
# Copyright 2022 Thomas Kramer <code@tkramer.ch>
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
import fcntl
import re
import shlex
import subprocess
import time

from duplicity import util

import duplicity.backend
from duplicity import (
    path,
    progress,
)
from duplicity.errors import (
    FatalBackendException,
    BackendException,
    InvalidBackendURL,
)


class Xorriso:
    """
    Wrapper around a xorriso subprocess.
    """

    def __init__(self, device, xorriso_path="xorriso", xorriso_args=None):
        self.device = device

        # Xorriso process
        self.proc = None

        # Default arguments for xorriso.
        self.xorriso_args = [
            "-abort_on",
            "FAILURE",
            "-return_with",
            "SORRY",
            "0",
            "-osirrox",
            "on",  # Enable copying from ISO to disk.
            "-calm_drive",
            "off",  # Don't immediately turn off device. Increases access speed for next action.abs
            "-joliet",
            "on",
        ]

        if xorriso_args is not None:
            self.xorriso_args.extend(xorriso_args)

        self.__start_subprocess(
            [xorriso_path]
            + self.xorriso_args
            + [
                "-dev",
                self.device,
                "-dialog",
                "on",  # Enable interactive mode
            ]
        )

        stdout, stderr = self.__recv_stdout_stderr()
        self.__handle_xorriso_error(stderr)

        stdout, stderr = self.__send_cmd("-version")  # Test connectivity to subprocess.

    def __start_subprocess(self, commandline):
        def setNonBlocking(fd):
            flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            flags = flags | os.O_NONBLOCK
            fcntl.fcntl(fd, fcntl.F_SETFL, flags)

        try:
            p = subprocess.Popen(
                commandline,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.proc = p
        except FileNotFoundError as err:
            raise FatalBackendException(f"Xorriso binary not found: {self.xorriso_cmd}")

        setNonBlocking(self.proc.stdout)
        setNonBlocking(self.proc.stderr)

    def __send_cmd(self, *args):
        # Drain stdout and stderr

        while self.proc.stdout.readline():
            pass

        while self.proc.stderr.readline():
            pass

        try:
            for arg in args:
                self.proc.stdin.write(shlex.quote(arg).encode("utf-8"))
                self.proc.stdin.write(b" ")
            self.proc.stdin.write(b"\n")
            self.proc.stdin.flush()
        except BrokenPipeError as e:
            raise FatalBackendException("BrokenPipe: lost connection to xorriso subprocess")

        stdout, stderr = self.__recv_stdout_stderr()

        self.__handle_xorriso_error(stderr)

        return stdout, stderr

    def __recv_stdout_stderr(self):
        stdout = []
        stderr = []
        while True:
            if self.proc.poll() is not None:
                # Process terminated
                break

            no_input = True

            while True:
                line = self.proc.stdout.readline().decode("utf-8").strip()
                if line:
                    stdout.append(line)
                else:
                    no_input = False
                    break

            while True:
                line = self.proc.stderr.readline().decode("utf-8").strip()
                if line:
                    stderr.append(line)
                else:
                    no_input = False
                    break

            if stderr and stderr[-1] == "enter option and arguments :":
                break

            if no_input:
                time.sleep(0.1)

        return stdout, stderr

    def __handle_xorriso_error(self, stderr):
        """
        Detect errors from stderr of xorriso.
        Convert the errors into exceptions.
        """

        lines = stderr

        stderr = "\n".join(lines)

        is_fatal = "FATAL" in stderr
        is_failure = "FAILURE" in stderr

        if is_fatal:
            msg = "\n".join(l for l in lines if ": FATAL" in l)
            raise BackendException(msg)
        elif is_failure:
            msg = "\n".join(l for l in lines if ": FAILURE" in l)
            raise BackendException(stderr)

    def ls(self, pattern="."):
        """
        List files on optical disc.
        """

        files = [f for f, _ in self.lsl(pattern)]

        return files

    def lsl(self, pattern="."):
        """
        List files on optical disc.
        """

        stdout, stderr = self.__send_cmd("-lsl", pattern)

        # Parse output of `xorriso -lsl`
        lines = stdout

        files = []

        for line in lines:
            line = line.strip()

            if not line:  # Skip empty lines
                continue

            parts = re.split("\\s+", line, maxsplit=8)

            if len(parts) != 9:
                continue

            mode, _, _uid, _gid, size, _month, _day, _time, filename = parts

            if not filename.startswith("'") or not filename.endswith("'"):
                raise BackendException("Got unexpected format from xorriso -lsl.")

            # Parse size into an integer.
            try:
                size = int(size)
            except Exception as e:
                raise BackendException("Could not parse file size.")

            filename = filename[1:-1]  # strip leading and trailing `'`s
            files.append((filename, {"size": size}))

        return files

    def commit(self):
        """
        Commit changes and write them to the image.
        """

        stdout, stderr = self.__send_cmd("-commit")

        if "exceeds free space on media" in "\n".join(stderr):
            raise BackendException("Not enough free space on media.")

    def end(self):
        """
        Terminate the xorriso subprocess
        """

        stdout, stderr = self.__send_cmd("-end")

    def cp(self, files, dest):
        """
        Copy file to the ISO image. Does not commit the changes yet.
        """
        assert isinstance(files, list)

        stdout, stderr = self.__send_cmd(
            "-cpr",
            *files,
            dest,
            "--",
        )

        if "exceeds free space on media" in "\n".join(stderr):
            raise BackendException("Not enough free space on media.")

    def rm(self, files):
        """
        Remove a list of files from the image. Does not commit the changes yet.
        """
        assert isinstance(files, list)

        if not files:
            return

        stdout, stderr = self.__send_cmd(
            "-rm",
            *files,
            # Don't commit yet.
        )

    def extract(self, files, dest):
        """
        Extract files from the ISO image.
        """
        assert isinstance(files, list)

        assert not os.path.exists(dest) or os.path.isfile(dest)

        if len(files) == 0:
            return

        stdout, stderr = self.__send_cmd("-cpx", *files, dest)


class XorrisoBackend(duplicity.backend.Backend):
    """Backend for writing to optical discs or ISO images using xorriso.

    Simple URLs look like `xorriso:///dev/sr0` if the backup location is at the root of the filesystem.
    or if `xorriso://dev/sr0:/path/to/a/directory/on/iso` if the backup location is in a directory.

    Especially for testing also an ISO file can be used: xorriso://path/to/image.iso

    The path to the `xorriso` executable can be specified with teh `XORRISO_PATH` environment variable.
    Environment variables:

    * XORRISO_PATH: Alternative path to the `xorriso` executable
    * XORRISO_WRITE_SPEED: Specify the speed for writing to the optical disc. One of ["min", "max"].
    * XORRISO_ASSERT_VOLID: Abort when the volume ID of the ISO image does not match the given value.
    * XORRISO_ARGS: Arbitrary arguments to xorriso, inserted before the filesystem operations. For experts only.
    """

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        # Path to xorriso executable.
        xorriso_cmd = os.environ.get("XORRISO_PATH", default="xorriso")

        # Check if xorriso is installed.
        if xorriso_cmd == "xorriso":
            if not util.which("xorriso"):
                raise FatalBackendException("xorriso not installed")

        # Default arguments for xorriso.
        self.xorriso_args = []

        args_pre = os.environ.get("XORRISO_ARGS")
        if args_pre is not None:
            arg_list = shlex.split(args_pre)
            self.xorriso_args.extend(arg_list)

        assert_volid = os.environ.get("XORRISO_ASSERT_VOLID")
        if assert_volid is not None:
            self.xorriso_args += ["-assert_volid", assert_volid, "FAILURE"]

        speed = os.environ.get("XORRISO_WRITE_SPEED", default="min")
        if speed in ["min", "max"]:
            self.xorriso_args += ["-speed", speed]
        else:
            self.xorriso_args += ["-speed", "min"]

        # The URL form "file:MyFile" is not a valid duplicity target.
        if not parsed_url.path.startswith("//"):
            raise InvalidBackendURl("Bad xorriso:// path syntax.")

        path = parsed_url.path[2:]  # Strip '//'

        parts = path.split(":", maxsplit=1)
        if len(parts) == 2:
            self.device = parts[0]
            self.iso_path = parts[1]
        else:
            self.device = parts[0]
            self.iso_path = "/"

        if not self.iso_path.endswith("/"):
            self.iso_path += "/"

        if not os.path.exists(self.device):
            raise InvalidBackendURL(f"Optical disc device does not exist: {self.device}")

        # Start xorriso subprocess.
        self.xorriso = Xorriso(device=self.device, xorriso_path=xorriso_cmd, xorriso_args=self.xorriso_args)

    def _put(self, source_path, remote_filename):
        assert not os.path.isdir(source_path.name.decode("utf8"))
        source_path.setdata()
        source_size = source_path.getsize()
        progress.report_transfer(0, source_size)

        self.xorriso.cp(
            [source_path.name.decode("utf8")],
            self.iso_path + remote_filename.decode("utf8"),
        )
        self.xorriso.commit()

        progress.report_transfer(source_size, source_size)

    def _get(self, filename, local_path):
        self.xorriso.extract([self.iso_path + filename.decode("utf8")], local_path.name.decode("utf8"))

    def _list(self):
        files = self.xorriso.ls(pattern=self.iso_path)
        return [f.encode() for f in files]

    def _delete(self, filename):
        self.xorriso.rm([self.iso_path + filename.decode("utf8")])

    def _delete_list(self, filenames):
        filenames = [self.iso_path + f.decode("utf8") for f in filenames]
        self.xorriso.rm(filenames)

    def _query(self, filename):
        filename = self.iso_path + filename.decode("utf8")
        files = self.xorriso.lsl(filename)

        if len(files) == 0 or files[0][0] != filename:
            size = -1
        else:
            size = files[0][1]["size"]

        return {"size": size}

    def _close(self):
        self.xorriso.commit()
        self.xorriso.end()


duplicity.backend.register_backend("xorriso", XorrisoBackend)
