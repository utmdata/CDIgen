# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2002 Ben Escoto <ben@emerose.org>
# Copyright 2007 Kenneth Loafman <kenneth@loafman.com>
# Copyright 2011 Alexander Zangerl <az@snafu.priv.at>
# Copyright 2012 edso (ssh_config added)
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
import getpass
import logging
import os
import re
import sys
import warnings
from textwrap import dedent

import duplicity.backend
from duplicity import config
from duplicity import progress
from duplicity import util
from duplicity.errors import BackendException

global paramiko

read_blocksize = 65635  # for doing scp retrievals, where we need to read ourselves


class SSHParamikoBackend(duplicity.backend.Backend):
    """This backend accesses files using the sftp or scp protocols.
    It does not need any local client programs, but an ssh server and the sftp
    program must be installed on the remote side (or with scp, the programs
    scp, ls, mkdir, rm and a POSIX-compliant shell).

    Authentication keys are requested from an ssh agent if present, then
    ~/.ssh/id_rsa/dsa are tried. If -oIdentityFile=path is present in
    --ssh-options, then that file is also tried. The passphrase for any of
    these keys is taken from the URI or FTP_PASSWORD. If none of the above are
    available, password authentication is attempted (using the URI or
    FTP_PASSWORD).

    Missing directories on the remote side will be created.

    If scp is active then all operations on the remote side require passing
    arguments through a shell, which introduces unavoidable quoting issues:
    directory and file names that contain single quotes will not work.
    This problem does not exist with sftp.
    """

    def __init__(self, parsed_url):
        global paramiko

        duplicity.backend.Backend.__init__(self, parsed_url)

        self.retry_delay = 10

        if parsed_url.path:
            # remove first leading '/'
            self.remote_dir = re.sub(r"^/", r"", parsed_url.path, 1)
        else:
            self.remote_dir = "."

        # lazily import paramiko when we need it
        # debian squeeze's paramiko is a bit old, so we silence randompool
        # depreciation warning note also: passphrased private keys work with
        # squeeze's paramiko only if done with DES, not AES
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                import paramiko
            except ImportError:
                raise

        class AgreedAddPolicy(paramiko.AutoAddPolicy):
            """
            Policy for showing a yes/no prompt and adding the hostname and new
            host key to the known host file accordingly.

            This class simply extends the AutoAddPolicy class with a yes/no
            prompt.
            """

            def missing_host_key(self, client, hostname, key):
                md5 = key.get_fingerprint().hex()
                # format md5 as ssh does
                fingerprints = f"  MD5:{':'.join(str(a + b) for a, b in list(zip(md5[::2], md5[1::2])))}"
                # sha256 fingerprint available since paramiko 3.2 only
                if hasattr(key, "fingerprint"):
                    fingerprints += f"\n  {key.fingerprint}"
                keyname = key.get_name().upper()
                question = dedent(
                    """
                    The authenticity of host '{hostname}' can't be established.
                    {keyname} fingerprint is
                    {fingerprints}.
                    Are you sure you want to continue connecting (yes/no)? """
                ).format(**locals())
                while True:
                    sys.stdout.write(question)
                    choice = input().lower()
                    if choice in ["yes", "y"]:
                        paramiko.AutoAddPolicy.missing_host_key(self, client, hostname, key)
                        return
                    elif choice in ["no", "n"]:
                        raise AuthenticityException(hostname)
                    else:
                        question = "Please type 'yes' or 'no': "

        class AuthenticityException(paramiko.SSHException):
            def __init__(self, hostname):
                paramiko.SSHException.__init__(self, f"Host key verification for server {hostname} failed.")

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(AgreedAddPolicy())

        # paramiko uses logging with the normal python severity levels,
        # but duplicity uses both custom levels and inverted logic...*sigh*
        self.client.set_log_channel("sshbackend")
        ours = paramiko.util.get_logger("sshbackend")
        dest = logging.StreamHandler(sys.stderr)
        dest.setFormatter(logging.Formatter("ssh: %(message)s"))
        ours.addHandler(dest)

        # ..and the duplicity levels are neither linear,
        # nor are the names compatible with python logging,
        # eg. 'NOTICE'...WAAAAAH!
        plevel = logging.getLogger("duplicity").getEffectiveLevel()
        if plevel <= 1:
            wanted = logging.DEBUG
        elif plevel <= 5:
            wanted = logging.INFO
        elif plevel <= 7:
            wanted = logging.WARNING
        elif plevel <= 9:
            wanted = logging.ERROR
        else:
            wanted = logging.CRITICAL
        ours.setLevel(wanted)

        # load user/local known_hosts files
        # paramiko is very picky wrt format and bails out on any problem...
        global_known_hosts = "/etc/ssh/ssh_known_hosts"
        m = re.search(
            r"""
                      ^(?:.+\s+)?
                      (?:-oGlobalKnownHostsFile=)
                      (
                          ([\"'])
                          ([^\\2]+)
                          \\2
                          |
                          [\S]+
                      )
                      """,
            config.ssh_options,
            re.VERBOSE,
        )
        if m is not None:
            global_known_hosts = m.group(3) if m.group(3) else m.group(1)
        try:
            if os.path.isfile(global_known_hosts):
                self.client.load_system_host_keys(global_known_hosts)
        except Exception as e:
            raise BackendException(f"could not load {global_known_hosts}, maybe corrupt?")

        user_known_hosts = os.path.expanduser("~/.ssh/known_hosts")
        m = re.search(
            r"""
                      ^(?:.+\s+)?
                      (?:-oUserKnownHostsFile=)
                      (
                          ([\"'])
                          ([^\\2]+)
                          \\2
                          |
                          [\S]+
                      )
                      """,
            config.ssh_options,
            re.VERBOSE,
        )
        if m is not None:
            user_known_hosts = m.group(3) if m.group(3) else m.group(1)
        try:
            # use load_host_keys() to signal it's writable to paramiko
            # load if file exists or add filename to create it if needed
            if os.path.isfile(user_known_hosts):
                self.client.load_host_keys(user_known_hosts)
            else:
                self.client._host_keys_filename = user_known_hosts
        except Exception as e:
            raise BackendException(f"could not load {user_known_hosts}, maybe corrupt?")

        """ the next block reorganizes all host parameters into a
        dictionary like SSHConfig does. this dictionary 'self.config'
        becomes the authorative source for these values from here on.
        rationale is that it is easiest to deal wrt overwriting multiple
        values from ssh_config file. (ede 03/2012)
        """
        self.config = {"hostname": parsed_url.hostname}
        # get system host config entries
        self.config.update(self.gethostconfig("/etc/ssh/ssh_config", parsed_url.hostname))
        # update with user's config file
        self.config.update(self.gethostconfig("~/.ssh/config", parsed_url.hostname))
        # update with url values
        # username from url
        if parsed_url.username:
            self.config.update({"user": parsed_url.username})
        # username from input
        if "user" not in self.config:
            self.config.update({"user": getpass.getuser()})
        # port from url
        if parsed_url.port:
            self.config.update({"port": parsed_url.port})
        # ensure there is deafult 22 or an int value
        if "port" in self.config:
            self.config.update({"port": int(self.config["port"])})
        else:
            self.config.update({"port": 22})
        # parse ssh options for alternative ssh private key, identity file
        m = re.search(
            r"""
                      ^(?:.+\s+)?
                      (?:-oIdentityFile=|-i\s+)
                      (([\"'])
                      (
                          [^\\2]+)\\2
                          |
                          [\S]+
                      )
                      """,
            config.ssh_options,
            re.VERBOSE,
        )
        if m is not None:
            keyfilename = m.group(3) if m.group(3) else m.group(1)
            self.config["identityfile"] = keyfilename.strip("'\"")
        # ensure ~ is expanded and identity exists in dictionary
        if "identityfile" in self.config:
            if not isinstance(self.config["identityfile"], list):
                # Paramiko 1.9.0 and earlier do not support multiple
                # identity files when parsing config files and always
                # return a string; later versions always return a list,
                # even if there is only one file given.
                #
                # All recent versions seem to support *using* multiple
                # identity files, though, so to make things easier, we
                # simply always use a list.
                self.config["identityfile"] = [self.config["identityfile"]]

            self.config["identityfile"] = [os.path.expanduser(i) for i in self.config["identityfile"]]
        else:
            self.config["identityfile"] = None

        # get password, enable prompt if askpass is set
        self.use_getpass = config.ssh_askpass
        # set url values for beautiful login prompt
        parsed_url.username = self.config["user"]
        parsed_url.hostname = self.config["hostname"]

        self.scheme = duplicity.backend.strip_prefix(parsed_url.scheme, "paramiko")
        self.use_scp = self.scheme == "scp"

        self.connect()

    def connect(self):
        password = self.get_password()

        try:
            self.client.connect(
                hostname=self.config["hostname"],
                port=self.config["port"],
                username=self.config["user"],
                password=password,
                allow_agent=True,
                look_for_keys=True,
                key_filename=self.config["identityfile"],
            )
        except Exception as e:
            raise BackendException(
                f"ssh connection to "
                f"{self.config['user']}@{self.config['hostname']}:{int(self.config['port'])} "
                f"failed: {e}"
            )
        self.client.get_transport().set_keepalive(int(config.timeout / 2))

        # scp or sftp?
        if self.use_scp:
            # sanity-check the directory name
            if re.search("'", self.remote_dir):
                raise BackendException("cannot handle directory names with single quotes with scp")

            # make directory if needed
            self.runremote(f"mkdir -p '{self.remote_dir}'", False, "scp mkdir ")
        else:
            try:
                self.sftp = self.client.open_sftp()
            except Exception as e:
                raise BackendException(f"sftp negotiation failed: {e}")

            # move to the appropriate directory, possibly after creating it and its parents
            dirs = self.remote_dir.split(os.sep)
            if len(dirs) > 0:
                if dirs[0] == "":
                    dirs[0] = "/"
                for d in dirs:
                    if d == "":
                        continue
                    try:
                        attrs = self.sftp.stat(d)
                    except IOError as e:
                        if e.errno == errno.ENOENT:
                            try:
                                self.sftp.mkdir(d)
                            except Exception as e:
                                raise BackendException(f"sftp mkdir {self.sftp.normalize('.')}/{d} failed: {e}")
                        else:
                            raise BackendException(f"sftp stat {self.sftp.normalize('.')}/{d} failed: {e}")
                    try:
                        self.sftp.chdir(d)
                    except Exception as e:
                        raise BackendException(f"sftp chdir to {self.sftp.normalize('.')}/{d} failed: {e}")

    def _put(self, source_path, remote_filename):
        # remote_filename is a byte object, not str or unicode
        remote_filename = os.fsdecode(remote_filename)
        if self.use_scp:
            f = open(source_path.name, "rb")
            try:
                chan = self.client.get_transport().open_session()
                chan.settimeout(config.timeout)
                # scp in sink mode uses the arg as base directory
                chan.exec_command(f"scp -t '{self.remote_dir}'")
            except Exception as e:
                raise BackendException(f"scp execution failed: {e}")
            # scp protocol: one 0x0 after startup, one after the Create meta,
            # one after saving if there's a problem: 0x1 or 0x02 and some error
            # text
            response = chan.recv(1)
            if response != b"\0":
                raise BackendException(b"scp remote error: %b" % chan.recv(-1))
            fstat = os.stat(source_path.name)
            chan.send(f"C{oct(fstat.st_mode)[-4:]} {int(fstat.st_size)} {remote_filename}\n")
            response = chan.recv(1)
            if response != b"\0":
                raise BackendException(b"scp remote error: %b" % chan.recv(-1))
            file_pos = 0
            file_size = fstat.st_size
            while file_pos < file_size:
                chan.sendall(f.read(16384))
                file_pos = f.tell()
                progress.report_transfer(file_pos, file_size)
            chan.sendall(b"\0")
            f.close()
            response = chan.recv(1)
            if response != b"\0":
                raise BackendException(f"scp remote error: {chan.recv(-1)}")
            chan.close()
        else:
            self.sftp.put(source_path.name, remote_filename, callback=progress.report_transfer)

    def _get(self, remote_filename, local_path):
        # remote_filename is a byte object, not str or unicode
        remote_filename = os.fsdecode(remote_filename)
        if self.use_scp:
            try:
                chan = self.client.get_transport().open_session()
                chan.settimeout(config.timeout)
                chan.exec_command(f"scp -f '{self.remote_dir}/{remote_filename}'")
            except Exception as e:
                raise BackendException(f"scp execution failed: {e}")

            chan.send("\0")  # overall ready indicator
            msg = chan.recv(-1)
            if isinstance(msg, bytes):  # make msg into str
                msg = msg.decode()
            m = re.match(r"C([0-7]{4})\s+(\d+)\s+(\S.*)$", msg)
            if m is None or m.group(3) != remote_filename:
                raise BackendException(f"scp get {remote_filename} failed: incorrect response '{msg}'")
            chan.recv(1)  # dispose of the newline trailing the C message

            size = int(m.group(2))
            togo = size
            f = open(local_path.name, "wb")
            chan.send("\0")  # ready for data
            try:
                while togo > 0:
                    if togo > read_blocksize:
                        blocksize = read_blocksize
                    else:
                        blocksize = togo
                    buff = chan.recv(blocksize)
                    f.write(buff)
                    togo -= len(buff)
            except Exception as e:
                raise BackendException(f"scp get {remote_filename} failed: {e}")

            msg = chan.recv(1)  # check the final status
            if msg != b"\0":
                raise BackendException(f"scp get {remote_filename} failed: {chan.recv(-1)}")
            f.close()
            chan.send("\0")  # send final done indicator
            chan.close()
        else:
            self.sftp.get(remote_filename, local_path.name)

    def _list(self):
        # In scp mode unavoidable quoting issues will make this fail if the
        # directory name contains single quotes.
        if self.use_scp:
            output = self.runremote(f"ls -1 '{self.remote_dir}'", False, "scp dir listing ")
            return output.splitlines()
        else:
            return self.sftp.listdir()

    def _delete(self, filename):
        # filename is a byte object, not str or unicode
        filename = os.fsdecode(filename)
        # In scp mode unavoidable quoting issues will cause failures if
        # filenames containing single quotes are encountered.
        if self.use_scp:
            self.runremote(f"rm '{self.remote_dir}/{filename}'", False, "scp rm ")
        else:
            self.sftp.remove(filename)

    def runremote(self, cmd, ignoreexitcode=False, errorprefix=""):
        """small convenience function that opens a shell channel, runs remote
        command and returns stdout of command. throws an exception if exit
        code!=0 and not ignored"""
        try:
            ch_in, ch_out, ch_err = self.client.exec_command(cmd, -1, config.timeout)
            output = ch_out.read(-1)
            return output
        except Exception as e:
            if not ignoreexitcode:
                raise BackendException(f"{errorprefix}failed: {cmd} \n {util.uexc(e)}")

    def gethostconfig(self, file, host):
        file = os.path.expanduser(file)
        if not os.path.isfile(file):
            return {}

        sshconfig = paramiko.SSHConfig()
        try:
            sshconfig.parse(open(file))
        except Exception as e:
            raise BackendException(f"could not load '{file}', maybe corrupt?")

        return sshconfig.lookup(host)

    def _retry_cleanup(self):
        self.client.close()
        self.connect()


duplicity.backend.register_backend("sftp", SSHParamikoBackend)
duplicity.backend.register_backend("scp", SSHParamikoBackend)
duplicity.backend.register_backend("paramiko+sftp", SSHParamikoBackend)
duplicity.backend.register_backend("paramiko+scp", SSHParamikoBackend)
duplicity.backend.uses_netloc.extend(["sftp", "scp", "paramiko+sftp", "paramiko+scp"])
