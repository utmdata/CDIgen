# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2002 Ben Escoto <ben@emerose.org>
# Copyright 2007 Kenneth Loafman <kenneth@loafman.com>
# Copyright 2008 Ian Barton <ian@manor-farm.org>
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


import email
import email.encoders
import email.mime.multipart
import getpass
import imaplib
import os
import re
import socket
import time

from email.parser import Parser

try:
    from email.policy import default
except Exception as e:
    pass

# TODO: should probably change use of socket.sslerror instead of doing this
import ssl

socket.sslerror = ssl.SSLError

from duplicity import config
from duplicity.errors import *  # pylint: disable=unused-wildcard-import
import duplicity.backend


class ImapBackend(duplicity.backend.Backend):
    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        log.Debug(
            f"I'm {self.__class__.__name__} (scheme {parsed_url.scheme}) connecting to "
            f"{parsed_url.hostname} as {parsed_url.username}"
        )

        #  Store url for reconnection on error
        self.url = parsed_url

        #  Set the username
        if parsed_url.username is None:
            username = eval(input("Enter account userid: "))
        else:
            username = parsed_url.username

        #  Set the password
        if not parsed_url.password:
            if "IMAP_PASSWORD" in os.environ:
                password = os.environ.get("IMAP_PASSWORD")
            else:
                password = getpass.getpass("Enter account password: ")
        else:
            password = parsed_url.password

        self.username = username
        self.password = password
        self.resetConnection()

    def resetConnection(self):
        parsed_url = self.url
        try:
            imap_server = os.environ["IMAP_SERVER"]
        except KeyError:
            imap_server = parsed_url.hostname

        #  Try to close the connection cleanly
        try:
            self.conn.close()  # pylint:disable=access-member-before-definition
        except Exception:
            pass

        if parsed_url.scheme == "imap":
            cl = imaplib.IMAP4
            self.conn = cl(imap_server, 143)
        elif parsed_url.scheme == "imaps":
            cl = imaplib.IMAP4_SSL
            self.conn = cl(imap_server, 993)

        log.Debug(f"Type of imap class: {cl.__name__}")
        self.remote_dir = re.sub(r"^/", r"", parsed_url.path, 1)

        #  Login
        if not config.imap_full_address:
            self.conn.login(self.username, self.password)
            self.conn.select(config.imap_mailbox)
            log.Info("IMAP connected")
        else:
            self.conn.login(f"{self.username}@{parsed_url.hostname}", self.password)
            self.conn.select(config.imap_mailbox)
            log.Info("IMAP connected")

    def prepareBody(self, f, rname):
        mp = email.mime.multipart.MIMEMultipart()

        # I am going to use the remote_dir as the From address so that
        # multiple archives can be stored in an IMAP account and can be
        # accessed separately
        mp["From"] = self.remote_dir
        mp["Subject"] = rname.decode()

        a = email.mime.multipart.MIMEBase("application", "binary")
        a.set_payload(f.read())

        email.encoders.encode_base64(a)

        mp.attach(a)

        return mp.as_string()

    def _put(self, source_path, remote_filename):
        f = source_path.open("rb")
        allowedTimeout = config.timeout
        if allowedTimeout == 0:
            # Allow a total timeout of 1 day
            allowedTimeout = 2880
        while allowedTimeout > 0:
            try:
                self.conn.select(remote_filename)
                body = self.prepareBody(f, remote_filename)
                # If we don't select the IMAP folder before
                # append, the message goes into the INBOX.
                self.conn.select(config.imap_mailbox)
                self.conn.append(config.imap_mailbox, None, None, body.encode())
                break
            except (imaplib.IMAP4.abort, socket.error, socket.sslerror):
                allowedTimeout -= 1
                log.Info(f"Error saving '{remote_filename}', retrying in 30s ")
                time.sleep(30)
                while allowedTimeout > 0:
                    try:
                        self.resetConnection()
                        break
                    except (imaplib.IMAP4.abort, socket.error, socket.sslerror):
                        allowedTimeout -= 1
                        log.Info("Error reconnecting, retrying in 30s ")
                        time.sleep(30)

        log.Info(f"IMAP mail with '{remote_filename}' subject stored")

    def _get(self, remote_filename, local_path):
        allowedTimeout = config.timeout
        if allowedTimeout == 0:
            # Allow a total timeout of 1 day
            allowedTimeout = 2880
        while allowedTimeout > 0:
            try:
                self.conn.select(config.imap_mailbox)
                (result, flist) = self.conn.search(None, "Subject", remote_filename)
                if result != "OK":
                    raise Exception(flist[0])

                # check if there is any result
                if flist[0] == "":
                    raise Exception("no mail with subject %s")

                (result, flist) = self.conn.fetch(flist[0], "(RFC822)")

                if result != "OK":
                    raise Exception(flist[0])
                rawbody = flist[0][1]

                p = Parser()

                m = p.parsestr(rawbody.decode())

                mp = m.get_payload(0)

                body = mp.get_payload(decode=True)
                break
            except (imaplib.IMAP4.abort, socket.error, socket.sslerror):
                allowedTimeout -= 1
                log.Info(f"Error loading '{remote_filename}', retrying in 30s ")
                time.sleep(30)
                while allowedTimeout > 0:
                    try:
                        self.resetConnection()
                        break
                    except (imaplib.IMAP4.abort, socket.error, socket.sslerror):
                        allowedTimeout -= 1
                        log.Info("Error reconnecting, retrying in 30s ")
                        time.sleep(30)

        tfile = local_path.open("wb")
        tfile.write(body)
        tfile.close()
        local_path.setdata()
        log.Info(f"IMAP mail with '{remote_filename}' subject fetched")

    def _list(self):
        ret = []
        (result, flist) = self.conn.select(config.imap_mailbox)
        if result != "OK":
            raise BackendException(flist[0])

        # Going to find all the archives which have remote_dir in the From
        # address

        # Search returns an error if you haven't selected an IMAP folder.
        (result, flist) = self.conn.search(None, "FROM", self.remote_dir)
        if result != "OK":
            raise Exception(flist[0])
        if flist[0] == b"":
            return ret
        nums = flist[0].strip().split(b" ")
        set = b"%s:%s" % (nums[0], nums[-1])  # pylint: disable=redefined-builtin
        (result, flist) = self.conn.fetch(set, "(BODY[HEADER])")
        if result != "OK":
            raise Exception(flist[0])

        for msg in flist:
            if len(msg) == 1:
                continue
            headers = Parser(policy=default).parsestr(
                msg[1].decode("unicode-escape")  # noqa  # pylint: disable=unsubscriptable-object
            )
            subj = headers["subject"]
            header_from = headers["from"]

            # Catch messages with empty headers which cause an exception.
            if not (header_from is None):
                if re.compile(f"^{self.remote_dir}$").match(header_from):
                    ret.append(subj)
                    log.Info(f"IMAP flist: {subj} {header_from}")
        return ret

    def imapf(self, fun, *args):
        (ret, flist) = fun(*args)
        if ret != "OK":
            raise Exception(flist[0])
        return flist

    def delete_single_mail(self, i):
        self.imapf(self.conn.store, i, "+FLAGS", "\\DELETED")

    def expunge(self):
        flist = self.imapf(self.conn.expunge)

    def _delete_list(self, filename_list):
        for filename in filename_list:
            flist = self.imapf(self.conn.search, None, f"(SUBJECT {filename})")
            flist = flist[0].split()
            if len(flist) > 0 and flist[0] != "":
                self.delete_single_mail(flist[0])
                log.Notice(f"marked {filename} to be deleted")
        self.expunge()
        log.Notice(f"IMAP expunged {len(filename_list)} files")

    def _close(self):
        self.conn.select(config.imap_mailbox)
        self.conn.close()
        self.conn.logout()


duplicity.backend.register_backend("imap", ImapBackend)
duplicity.backend.register_backend("imaps", ImapBackend)
duplicity.backend.uses_netloc.extend(["imap", "imaps"])
