# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2013 Matthieu Huin <mhu@enovance.com>
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

import duplicity.backend
from duplicity import config
from duplicity import log
from duplicity.errors import BackendException


class SwiftBackend(duplicity.backend.Backend):
    """
    Backend for Swift
    """

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        try:
            from swiftclient.service import SwiftService
            from swiftclient import Connection
            from swiftclient import ClientException
        except ImportError as e:
            raise BackendException(
                f"""Swift backend requires the python-swiftclient library.
Exception: {str(e)}"""
            )

        self.resp_exc = ClientException
        conn_kwargs = {}
        os_options = {}
        svc_options = {}

        # if the user has already authenticated
        if "SWIFT_PREAUTHURL" in os.environ and "SWIFT_PREAUTHTOKEN" in os.environ:
            conn_kwargs["preauthurl"] = os.environ["SWIFT_PREAUTHURL"]
            conn_kwargs["preauthtoken"] = os.environ["SWIFT_PREAUTHTOKEN"]

        else:
            if "SWIFT_USERNAME" not in os.environ:
                raise BackendException("SWIFT_USERNAME environment variable " "not set.")

            if "SWIFT_PASSWORD" not in os.environ:
                raise BackendException("SWIFT_PASSWORD environment variable " "not set.")

            if "SWIFT_AUTHURL" not in os.environ:
                raise BackendException("SWIFT_AUTHURL environment variable " "not set.")

            svc_options["os_username"] = conn_kwargs["user"] = os.environ["SWIFT_USERNAME"]
            svc_options["os_password"] = conn_kwargs["key"] = os.environ["SWIFT_PASSWORD"]
            svc_options["os_auth_url"] = conn_kwargs["authurl"] = os.environ["SWIFT_AUTHURL"]

        if "SWIFT_AUTHVERSION" in os.environ:
            svc_options["auth_version"] = conn_kwargs["auth_version"] = os.environ["SWIFT_AUTHVERSION"]
            if os.environ["SWIFT_AUTHVERSION"] == "3":
                if "SWIFT_USER_DOMAIN_NAME" in os.environ:
                    os_options.update({"user_domain_name": os.environ["SWIFT_USER_DOMAIN_NAME"]})
                if "SWIFT_USER_DOMAIN_ID" in os.environ:
                    os_options.update({"user_domain_id": os.environ["SWIFT_USER_DOMAIN_ID"]})
                if "SWIFT_PROJECT_DOMAIN_NAME" in os.environ:
                    os_options.update({"project_domain_name": os.environ["SWIFT_PROJECT_DOMAIN_NAME"]})
                if "SWIFT_PROJECT_DOMAIN_ID" in os.environ:
                    os_options.update({"project_domain_id": os.environ["SWIFT_PROJECT_DOMAIN_ID"]})
                if "SWIFT_PROJECT_ID" in os.environ:
                    os_options.update({"project_id": os.environ["SWIFT_PROJECT_ID"]})
                if "SWIFT_PROJECT_NAME" in os.environ:
                    os_options.update({"project_name": os.environ["SWIFT_PROJECT_NAME"]})
                if "SWIFT_TENANTNAME" in os.environ:
                    os_options.update({"tenant_name": os.environ["SWIFT_TENANTNAME"]})
                if "SWIFT_ENDPOINT_TYPE" in os.environ:
                    os_options.update({"endpoint_type": os.environ["SWIFT_ENDPOINT_TYPE"]})
                if "SWIFT_USERID" in os.environ:
                    os_options.update({"user_id": os.environ["SWIFT_USERID"]})
                if "SWIFT_TENANTID" in os.environ:
                    os_options.update({"tenant_id": os.environ["SWIFT_TENANTID"]})
                if "SWIFT_REGIONNAME" in os.environ:
                    os_options.update({"region_name": os.environ["SWIFT_REGIONNAME"]})

        else:
            conn_kwargs["auth_version"] = "1"
        if "SWIFT_TENANTNAME" in os.environ:
            conn_kwargs["tenant_name"] = os.environ["SWIFT_TENANTNAME"]
        if "SWIFT_REGIONNAME" in os.environ:
            os_options.update({"region_name": os.environ["SWIFT_REGIONNAME"]})

        # formatting options for swiftclient.SwiftService
        for key in os_options.keys():
            svc_options[f"os_{key}"] = os_options[key]

        conn_kwargs["os_options"] = os_options

        # This folds the null prefix and all null parts, which means that:
        #  //MyContainer/ and //MyContainer are equivalent.
        #  //MyContainer//My/Prefix/ and //MyContainer/My/Prefix are equivalent.
        url_parts = [x for x in parsed_url.path.split("/") if x != ""]

        self.container = url_parts.pop(0)
        if url_parts:
            self.prefix = f"{'/'.join(url_parts)}/"
        else:
            self.prefix = ""

        policy = config.swift_storage_policy
        policy_header = "X-Storage-Policy"

        container_metadata = None
        try:
            log.Debug(f"Starting connection with arguments:'{conn_kwargs}'")
            self.conn = Connection(**conn_kwargs)
            container_metadata = self.conn.head_container(self.container)
        except ClientException as e:
            log.Debug(f"Connection failed: {e.__class__.__name__} {str(e)}")
            pass
        except Exception as e:
            log.FatalError(
                f"Connection failed: {e.__class__.__name__} {str(e)}",
                log.ErrorCode.connection_failed,
            )

        if container_metadata is None:
            log.Info(f"Creating container {self.container}")
            try:
                headers = dict([[policy_header, policy]]) if policy else None
                self.conn.put_container(self.container, headers=headers)
            except Exception as e:
                log.FatalError(
                    f"Container creation failed: {e.__class__.__name__} {str(e)}",
                    log.ErrorCode.connection_failed,
                )
        elif policy and container_metadata[policy_header.lower()] != policy:
            log.FatalError(
                f"Container '{self.container}' exists but its storage policy is "
                f"'{container_metadata[policy_header.lower()]}' not '{policy}'."
            )
        else:
            log.Debug(f"Container already created: {container_metadata}")

        # checking service connection
        try:
            log.Debug(f"Starting  Swiftservice: '{svc_options}'")
            self.svc = SwiftService(options=svc_options)
            container_stat = self.svc.stat(self.container)
        except ClientException as e:
            log.FatalError(
                f"Connection failed: {e.__class__.__name__} {str(e)}",
                log.ErrorCode.connection_failed,
            )
        log.Debug(f"Container stats: {container_stat}")

    def _error_code(self, operation, e):  # pylint: disable=unused-argument
        if isinstance(e, self.resp_exc):
            if e.http_status == 404:
                return log.ErrorCode.backend_not_found

    def _put(self, source_path, remote_filename):
        lp = os.fsdecode(source_path.name)
        if config.mp_segment_size > 0:
            from swiftclient.service import SwiftUploadObject

            st = os.stat(lp)
            # only upload using Dynamic Large Object if mpvolsize is triggered
            if st.st_size >= config.mp_segment_size:
                log.Debug("Uploading Dynamic Large Object")
                mp = self.svc.upload(
                    self.container,
                    [SwiftUploadObject(lp, object_name=self.prefix + os.fsdecode(remote_filename))],
                    options={"segment_size": config.mp_segment_size},
                )
                uploads = [a for a in mp if "container" not in a["action"]]
                for upload in uploads:
                    if not upload["success"]:
                        raise BackendException(upload["traceback"])
                return
        rp = self.prefix + os.fsdecode(remote_filename)
        log.Debug(f"Uploading '{lp}' to '{rp}' in remote container '{self.container}'")
        self.conn.put_object(
            container=self.container,
            obj=self.prefix + os.fsdecode(remote_filename),
            contents=open(lp, "rb"),
        )

    def _get(self, remote_filename, local_path):
        headers, body = self.conn.get_object(
            self.container,
            self.prefix + os.fsdecode(remote_filename),
            resp_chunk_size=1024,
        )
        with open(local_path.name, "wb") as f:
            for chunk in body:
                f.write(chunk)

    def _list(self):
        headers, objs = self.conn.get_container(self.container, full_listing=True, path=self.prefix)
        # removes prefix from return values. should check for the prefix ?
        return [o["name"][len(self.prefix) :] for o in objs]

    def _delete(self, filename):
        # use swiftservice to correctly delete all segments in case of multipart uploads
        deleted = [a for a in self.svc.delete(self.container, [self.prefix + os.fsdecode(filename)])]

    def _query(self, filename):
        # use swiftservice to correctly report filesize in case of multipart uploads
        sobject = [a for a in self.svc.stat(self.container, [self.prefix + os.fsdecode(filename)])][0]
        sobj = {"size": int(sobject["headers"]["content-length"])}
        log.Debug(f"Objectquery: '{os.fsdecode(filename)}' has size {sobj['size']}.")
        return sobj


duplicity.backend.register_backend("swift", SwiftBackend)
