# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2021 Menno Smits <menno@smi-ling.nl>
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

import errno
import os
import re
import shutil
import tempfile
import urllib
import xml.etree.ElementTree as ET

import duplicity.backend
from duplicity import config
from duplicity import log
from duplicity.errors import BackendException


#
#   This backend works with the IDrive  "dedup implementation". V0.1
#               (for all new and recent accounts)
#
#   Credits: This code is loosely inspired by the work of <aappddeevv>
#
#
#   This backend uses an intermediate driver for IDrive: "idevsutil_dedup" that will be
#   installed automagically  when you perform the account setup on your system.
#   It can, however, also be downloaded directly from the following URL's
#
#   https://www.idrivedownloads.com/downloads/linux/download-options/IDrive_linux_64bit.zip
#   and
#   https://www.idrivedownloads.com/downloads/linux/download-options/IDrive_linux_32bit.zip
#
#   for 32 and 64 bit linux, respectively. Copy the file anywhere with exe permissions.
#   (no further setup of your IDrive account is needed for idrived to work)
#
#
#   For this backend to work, you need to create a number of environment variables:
#
#   - Put the absolute path to the driver-file (idevsutil_dedup) in IDEVSPATH
#   - Put the account-name (login name) in IDRIVEID
#
#   - Put the name of the desired bucket for this backup-session in IDBUCKET
#     If this bucket does not exist it will be created at runtime
#
#   - Create a file with the account password - put absolute path in IDPWDFILE
#
#   When using a custom encryption key:
#   - Create a file with the encryption key - put absolute path in IDKEYFILE
#
#   Note: setup proper security for these files!
#
#
#   The IDrive "root" issue ...
#
#   IDrive stores files according to 1) the selected bucket, 2) the supplied path
#   and 3)the absolute path of the directory used for uploads. So ... if we use
#       - bucket <MYBUCKET>
#       - duplicity commandline idrived://DUPLICITY
#   and
#       - system tempfile OR path set from --tempfile "\tmp"
#
#   the files end-up in the following path:
#       <MYBUCKET>/DUPLICITY/tmp/duplicity-??????-tempdir
#
#   Not only is this SO UGLY .... but - as tempdirs have unique names - this effectively
#   disables the idea of incremental backups.
#
#   To remedy this, idrived uses the concept of a "fakeroot" directory, defined via the
#   --idr-fakeroot=... switch. This can be an existing directory, or the directory is
#   created at runtime on the root of the (host) files system. (cave: you have to have
#   write access to the root!). Directories created at runtime are auto-removed on exit!
#
#   So, in the above scheme, we could do:
#       duplicity --idr-fakeroot=nicepath idrived://DUPLICITY
#
#   our files end-up at
#       <MYBUCKET>/DUPLICITY/nicepath
#
#
#   Have fun!
#


class IDriveBackend(duplicity.backend.Backend):
    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        # parsed_url will have leading slashes in it, 4 slashes typically.
        self.parsed_url = parsed_url
        self.url_string = duplicity.backend.strip_auth_from_url(self.parsed_url)
        log.Debug(f"parsed_url: {parsed_url}")

        self.connected = False

    def user_connected(self):
        return self.connected

    def request(self, commandline):
        # request for commands returning data in XML format
        log.Debug(f"Request command: {commandline}")
        try:
            _, reply, error = self.subprocess_popen(commandline)
        except KeyError:
            raise BackendException(f"Unknown protocol failure on request {commandline}")

        response = reply + error
        try:
            xml = f"<root>{''.join(re.findall('<[^>]+>', response))}</root>"
            el = ET.fromstring(xml)

        except Exception as e:
            el = None
        log.Debug(f"Request response: {response}")

        return el

    def connect(self):
        # get the path to the command executable
        path = os.environ.get("IDEVSPATH")
        if path is None:
            log.Warn("-" * 72)
            log.Warn("WARNING: No path to 'idevsutil_dedup' has been set. Download module from")
            log.Warn("   https://www.idrivedownloads.com/downloads/linux/download-options/IDrive_linux_64bit.zip")
            log.Warn("or")
            log.Warn("   https://www.idrivedownloads.com/downloads/linux/download-options/IDrive_linux_32bit.zip")
            log.Warn("and place anywhere with exe rights. Then creat env var 'IDEVSPATH' with path to file")
            log.Warn("-" * 72)
            raise BackendException("No IDEVSPATH env var set. Should contain folder to idevsutil_dedup")
        self.cmd = os.path.join(path, "idevsutil_dedup")
        log.Debug(f"IDrive command base: {self.cmd}")

        # get the account-id
        self.idriveid = os.environ.get("IDRIVEID")
        if self.idriveid is None:
            log.Warn("-" * 72)
            log.Warn("WARNING: IDrive logon ID missing")
            log.Warn("Create an environment variable IDriveID with your IDrive logon ID")
            log.Warn("-" * 72)
            raise BackendException("No IDRIVEID env var set. Should contain IDrive id")
        log.Debug(f"IDrive id: {self.idriveid}")

        # Get the full-path to the account password file
        filepath = os.environ.get("IDPWDFILE")
        if filepath is None:
            log.Warn("-" * 72)
            log.Warn("WARNING: IDrive password file missging")
            log.Warn("Please create a file with your IDrive logon password,")
            log.Warn("Then create an environment variable IDPWDFILE with path/filename of said file")
            log.Warn("-" * 72)
            raise BackendException("No IDPWDFILE env var set. Should contain file with password")
        log.Debug(f"IDrive pwdpath: {filepath}")
        self.auth_switch = f" --password-file={filepath}"

        # fakeroot set? Create directory and mark for cleanup
        if config.fakeroot is None:
            self.cleanup = False
            self.fakeroot = ""
        else:
            # Make sure fake root is created at root level!
            self.fakeroot = os.path.join("/", config.fakeroot)
            try:
                os.mkdir(self.fakeroot)
            except OSError as e:
                self.cleanup = False
                if e.errno == errno.EEXIST:
                    log.Debug(f"Using existing directory {self.fakeroot} as fake-root")
                else:
                    log.Warn("-" * 72)
                    log.Warn(
                        f"WARNING: Creation of FAKEROOT {self.fakeroot} failed; "
                        f"backup will use system temp directory"
                    )
                    log.Warn("This might interfere with incremental backups")
                    log.Warn("-" * 72)
                    raise BackendException(f"Creation of the directory {self.fakeroot} failed")
            else:
                log.Debug(f"Directory {self.fakeroot} created as fake-root (Will clean-up afterwards!)")
                self.cleanup = True

        # get the bucket
        self.bucket = os.environ.get("IDBUCKET")
        if self.bucket is None:
            log.Warn("-" * 72)
            log.Warn("WARNING: IDrive backup bucket missing")
            log.Warn("Create an environment variable IDBUCKET specifying the target bucket")
            log.Warn("-" * 72)
            raise BackendException("No IDBUCKET env var set. Should contain IDrive backup bucket")
        log.Debug(f"IDrive bucket: {self.bucket}")

        # check account / get config status and config type
        el = self.request(f"{self.cmd + self.auth_switch} --validate --user={self.idriveid}").find("tree")

        if el.attrib["message"] != "SUCCESS":
            raise BackendException(f"Protocol failure - {el.attrib['desc']}")
        if el.attrib["desc"] != "VALID ACCOUNT":
            raise BackendException("IDrive account invalid")
        if el.attrib["configstatus"] != "SET":
            raise BackendException("IDrive account not set")

        # When private encryption enabled: get the full-path to a encription key file
        if el.attrib["configtype"] == "PRIVATE":
            filepath = os.environ.get("IDKEYFILE")
            if filepath is None:
                log.Warn("-" * 72)
                log.Warn("WARNING: IDrive encryption key file missging")
                log.Warn("Please create a file with your IDrive encryption key,")
                log.Warn("Then create an environment variable IDKEYFILE with path/filename of said file")
                log.Warn("-" * 72)
                raise BackendException("No IDKEYFILE env var set. Should contain file with encription key")
            log.Debug(f"IDrive keypath: {filepath}")
            self.auth_switch += f" --pvt-key={filepath}"

        # get the server address
        el = self.request(f"{self.cmd + self.auth_switch} --getServerAddress {self.idriveid}").find("tree")
        self.idriveserver = el.attrib["cmdUtilityServer"]

        # get the device list - primarely used to get device-id string
        el = self.request(self.cmd + self.auth_switch + f" --list-device {self.idriveid}@{self.idriveserver}::home")
        # scan all returned devices for requested device (== bucket)
        self.idrivedevid = None
        for item in el.findall("item"):
            if item.attrib["nick_name"] == self.bucket:
                # prefix and suffix reverse-engineered from Common.pl!
                self.idrivedevid = f"5c0b{item.attrib['device_id']}4b5z"
        if self.idrivedevid is None:
            el = self.request(
                f"{self.cmd}{self.auth_switch} "
                f"--create-bucket --bucket-type=D --nick-name={self.bucket} "
                f"--os=Linux --uid=987654321 "
                f"{self.idriveid}@{self.idriveserver}::home/"
            ).find("item")
            # prefix and suffix reverse-engineered from Common.pl!
            self.idrivedevid = f"5c0b{el.attrib['device_id']}4b5z"

        # We're fully connected!
        self.connected = True
        log.Debug("User fully connected")

    def list_raw(self):
        # get raw list; used by _list, _query and _query_list
        remote_path = os.path.join(
            urllib.parse.unquote(self.parsed_url.path.lstrip("/")),
            self.fakeroot.lstrip("/"),
        ).rstrip()
        commandline = (
            self.cmd + self.auth_switch + f" --auth-list --device-id={self.idrivedevid} "
            f"{self.idriveid}@{self.idriveserver}::home/{remote_path}"
        )
        try:
            _, l, _ = self.subprocess_popen(commandline)
        except Exception as e:
            # error: treat as empty response
            log.Debug("list EMPTY response ")
            return []

        log.Debug(f"list response: {l}")

        # get a list of lists from data lines returned by idevsutil_dedup --auth-list
        filtered = list(
            map(
                (lambda line: re.split(r"\[|\]", line)),
                [x for x in l.splitlines() if x.startswith("[")],
            )
        )
        # remove whitespace from elements
        filtered = list(map((lambda line: list(map((lambda c: c.strip()), line))), filtered))
        # remove empty elements
        filtered = list(map((lambda cols: list(filter((lambda c: c != ""), cols))), filtered))

        return filtered

    def _put(self, source_path, remote_filename):
        # Put a file.
        log.Debug("_PUT")
        if not self.user_connected():
            self.connect()

        # decode from byte-stream to utf-8 string
        filename = remote_filename.decode("utf-8")

        intrim_file = os.path.join(self.fakeroot, filename)
        remote_dirpath = urllib.parse.unquote(self.parsed_url.path.lstrip("/"))

        os.rename(source_path.name, intrim_file)

        log.Debug(f"put_file: source_path={source_path.name}, remote_file={filename}")

        flist = tempfile.NamedTemporaryFile("w")
        flist.write(intrim_file)
        flist.seek(0)

        putrequest = (
            f"{self.cmd}{self.auth_switch} "
            f"--device-id={self.idrivedevid} "
            f"--files-from={flist.name} / "
            f"{self.idriveid}@{self.idriveserver}::home/{remote_dirpath}"
        )
        log.Debug(f"put_file put command: {putrequest}")
        _, putresponse, _ = self.subprocess_popen(putrequest)
        log.Debug(f"put_file put response: {putresponse}")

        flist.close()
        os.remove(intrim_file)

    def _get(self, remote_filename, local_path):
        # Get a file.
        log.Debug("_GET")
        if not self.user_connected():
            self.connect()

        # decode from byte-stream to utf-8 string
        filename = remote_filename.decode("utf-8")

        remote_path = os.path.join(
            urllib.parse.unquote(self.parsed_url.path.lstrip("/")),
            self.fakeroot.lstrip("/"),
            filename,
        ).rstrip()

        log.Debug(
            f"_get: remote_filename={filename}, local_path={local_path}, "
            f"remote_path={remote_path}, parsed_url.path={self.parsed_url.path}"
        )

        # Create tempdir to downlaod file into
        tmpdir = tempfile.mkdtemp()
        log.Debug(f"_get created temporary download folder: {tmpdir}")

        # The filelist file
        flist = tempfile.NamedTemporaryFile("w")
        flist.write(remote_path)
        flist.seek(0)

        getrequest = (
            f"{self.cmd}{self.auth_switch} "
            f"--device-id={self.idrivedevid} "
            f"--files-from={flist.name} "
            f"{self.idriveid}@{self.idriveserver}::home/ "
            f"{tmpdir}"
        )
        log.Debug(f"get command: {getrequest}")
        _, getresponse, _ = self.subprocess_popen(getrequest)
        log.Debug(f"_get response: {getresponse}")

        flist.close()

        # move to the final location
        downloadedSrcPath = os.path.join(tmpdir, remote_path.lstrip("/").rstrip("/"))
        log.Debug(f"_get moving file {downloadedSrcPath} to final location: {local_path.name}")

        os.rename(downloadedSrcPath, local_path.name)

        shutil.rmtree(tmpdir)

    def _list(self):
        # List files on remote folder
        log.Debug("_LIST")
        if not self.user_connected():
            self.connect()

        filtered = self.list_raw()
        filtered = [x[-1] for x in filtered]

        return filtered

    def _delete(self, remote_filename):
        # Delete single file
        log.Debug("_DELETE")
        if not self.user_connected():
            self.connect()

        # decode from byte-stream to utf-8 string
        filename = remote_filename.decode("utf-8")

        # create a file-list file
        flist = tempfile.NamedTemporaryFile("w")
        flist.write(filename.lstrip("/"))
        flist.seek(0)

        # target path (remote) on IDrive
        remote_path = os.path.join(
            urllib.parse.unquote(self.parsed_url.path.lstrip("/")),
            self.fakeroot.lstrip("/"),
        ).rstrip()
        log.Debug(f"delete: {filename} from remote file path {remote_path}")

        # delete files from file-list
        delrequest = (
            f"{self.cmd}{self.auth_switch} "
            f"--delete-items "
            f"--device-id={self.idrivedevid} "
            f"--files-from={flist.name} "
            f"{self.idriveid}@{self.idriveserver}::home/{remote_path}"
        )
        log.Debug(f"delete: {delrequest}")
        _, delresponse, _ = self.subprocess_popen(delrequest)
        log.Debug(f"delete response: {delresponse}")

        # close tempfile
        flist.close()

    def _delete_list(self, filename_list):
        # Delete multiple files
        log.Debug("_DELETE LIST")
        if not self.user_connected():
            self.connect()

        # create a file-list file
        flist = tempfile.NamedTemporaryFile("w")

        # create file-list
        for filename in filename_list:
            flist.write(f"{filename.decode('utf-8').lstrip('/')}\n")
        flist.seek(0)

        # target path (remote) on IDrive
        remote_path = os.path.join(
            urllib.parse.unquote(self.parsed_url.path.lstrip("/")),
            self.fakeroot.lstrip("/"),
        ).rstrip()
        log.Debug(f"delete multiple files from remote file path {remote_path}")

        # delete files from file-list
        delrequest = (
            f"{self.cmd}{self.auth_switch} "
            f"--delete-items "
            f"--device-id={self.idrivedevid} "
            f"--files-from={flist.name} "
            f"{self.idriveid}@{self.idriveserver}::home/{remote_path}"
        )
        log.Debug(f"delete: {delrequest}")
        _, delresponse, _ = self.subprocess_popen(delrequest)
        log.Debug(f"delete response: {delresponse}")

        # close tempfile
        flist.close()

    def _close(self):
        # Remove EVS_temp directory + contents
        log.Debug("Removing IDrive temp folder evs_temp")
        try:
            shutil.rmtree("evs_temp")
        except Exception as e:
            pass

    def _query(self, filename):
        log.Debug("_QUERY")
        if not self.user_connected():
            self.connect()

        # Get raw directory list; take-out size (index 1) for requested filename (index -1)
        filtered = self.list_raw()
        if filtered:
            filtered = [x[1] for x in filtered if x[-1] == filename.decode("utf-8")]
        if filtered:
            return {"size": int(filtered[0])}

        return {"size": -1}

    def _query_list(self, filename_list):
        log.Debug("_QUERY_LIST")
        if not self.user_connected():
            self.connect()

        # Get raw directory list
        filtered = self.list_raw()

        # For each filename in list: take-out size (index 1) for requested filename (index -1)
        info = {}
        for filename in filename_list:
            if filtered:
                result = [x[1] for x in filtered if x[-1] == filename.decode("utf-8")]
            if result:
                info[filename] = {"size": int(result[0])}
            else:
                info[filename] = {"size": -1}

        return info

    def __del__(self):
        # remove the self-created temp dir.
        # We do it here, AFTER the clean-up of Duplicity, so it will be empty!
        if self.cleanup:
            os.rmdir(self.fakeroot)


duplicity.backend.register_backend("idrived", IDriveBackend)
