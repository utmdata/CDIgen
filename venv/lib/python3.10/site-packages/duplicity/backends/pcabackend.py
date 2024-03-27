# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2013 Matthieu Huin <mhu@enovance.com>
# Copyright 2017 Xavier Lucas <xavier.lucas@corp.ovh.com>
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
import time

import duplicity.backend
from duplicity import log
from duplicity.errors import BackendException


class PCABackend(duplicity.backend.Backend):
    """
    Backend for OVH PCA
    """

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)

        try:
            from swiftclient import Connection
            from swiftclient import ClientException
        except ImportError as e:
            raise BackendException(
                f"""PCA backend requires the python-swiftclient library.
Exception: {str(e)}"""
            )

        self.resp_exc = ClientException
        self.conn_cls = Connection
        conn_kwargs = {}

        # if the user has already authenticated
        if "PCA_PREAUTHURL" in os.environ and "PCA_PREAUTHTOKEN" in os.environ:
            conn_kwargs["preauthurl"] = os.environ["PCA_PREAUTHURL"]
            conn_kwargs["preauthtoken"] = os.environ["PCA_PREAUTHTOKEN"]

        else:
            if "PCA_USERNAME" not in os.environ:
                raise BackendException("PCA_USERNAME environment variable " "not set.")

            if "PCA_PASSWORD" not in os.environ:
                raise BackendException("PCA_PASSWORD environment variable " "not set.")

            if "PCA_AUTHURL" not in os.environ:
                raise BackendException("PCA_AUTHURL environment variable " "not set.")

            conn_kwargs["user"] = os.environ["PCA_USERNAME"]
            conn_kwargs["key"] = os.environ["PCA_PASSWORD"]
            conn_kwargs["authurl"] = os.environ["PCA_AUTHURL"]

        os_options = {}

        if "PCA_AUTHVERSION" in os.environ:
            conn_kwargs["auth_version"] = os.environ["PCA_AUTHVERSION"]
            if os.environ["PCA_AUTHVERSION"] == "3":
                if "PCA_USER_DOMAIN_NAME" in os.environ:
                    os_options.update({"user_domain_name": os.environ["PCA_USER_DOMAIN_NAME"]})
                if "PCA_USER_DOMAIN_ID" in os.environ:
                    os_options.update({"user_domain_id": os.environ["PCA_USER_DOMAIN_ID"]})
                if "PCA_PROJECT_DOMAIN_NAME" in os.environ:
                    os_options.update({"project_domain_name": os.environ["PCA_PROJECT_DOMAIN_NAME"]})
                if "PCA_PROJECT_DOMAIN_ID" in os.environ:
                    os_options.update({"project_domain_id": os.environ["PCA_PROJECT_DOMAIN_ID"]})
                if "PCA_TENANTNAME" in os.environ:
                    os_options.update({"tenant_name": os.environ["PCA_TENANTNAME"]})
                if "PCA_ENDPOINT_TYPE" in os.environ:
                    os_options.update({"endpoint_type": os.environ["PCA_ENDPOINT_TYPE"]})
                if "PCA_USERID" in os.environ:
                    os_options.update({"user_id": os.environ["PCA_USERID"]})
                if "PCA_TENANTID" in os.environ:
                    os_options.update({"tenant_id": os.environ["PCA_TENANTID"]})
                if "PCA_REGIONNAME" in os.environ:
                    os_options.update({"region_name": os.environ["PCA_REGIONNAME"]})

        else:
            conn_kwargs["auth_version"] = "2"
        if "PCA_TENANTNAME" in os.environ:
            conn_kwargs["tenant_name"] = os.environ["PCA_TENANTNAME"]
        if "PCA_REGIONNAME" in os.environ:
            os_options.update({"region_name": os.environ["PCA_REGIONNAME"]})

        conn_kwargs["os_options"] = os_options
        conn_kwargs["retries"] = 0

        self.conn_kwargs = conn_kwargs

        # This folds the null prefix and all null parts, which means that:
        #  //MyContainer/ and //MyContainer are equivalent.
        #  //MyContainer//My/Prefix/ and //MyContainer/My/Prefix are equivalent.
        url_parts = [x for x in parsed_url.path.split("/") if x != ""]

        self.container = url_parts.pop(0)
        if url_parts:
            self.prefix = f"{'/'.join(url_parts)}/"
        else:
            self.prefix = ""

        policy = "PCA"
        policy_header = "X-Storage-Policy"

        container_metadata = None
        try:
            self.conn = Connection(**self.conn_kwargs)
            container_metadata = self.conn.head_container(self.container)
        except ClientException:
            pass
        except Exception as e:
            log.FatalError(
                f"Connection failed: {e.__class__.__name__} {str(e)}",
                log.ErrorCode.connection_failed,
            )

        if container_metadata is None:
            log.Info(f"Creating container {self.container}")
            try:
                headers = dict([[policy_header, policy]])
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

    def _error_code(self, operation, e):  # pylint: disable= unused-argument
        if isinstance(e, self.resp_exc):
            if e.http_status == 404:
                return log.ErrorCode.backend_not_found

    def _put(self, source_path, remote_filename):
        self.conn.put_object(
            self.container,
            self.prefix + os.fsdecode(remote_filename),
            open(os.fsdecode(source_path.name), "rb"),
        )

    def _get(self, remote_filename, local_path):
        body = self.unseal(os.fsdecode(remote_filename))
        if body:
            with open(os.fsdecode(local_path.name), "wb") as f:
                for chunk in body:
                    f.write(chunk)

    def __list_objs(self, ffilter=None):
        # full_listing should be set to True but a bug in python-swiftclient
        # doesn't forward query_string in this case...
        # bypass here using a patched copy (with query_string) from swiftclient code
        rv = self.conn.get_container(
            self.container,
            full_listing=False,
            path=self.prefix,
            query_string="policy_extra=true",
        )
        listing = rv[1]
        while listing:
            marker = listing[-1]["name"]
            version_marker = listing[-1].get("version_id")
            listing = self.conn.get_container(
                self.container,
                marker=marker,
                version_marker=version_marker,
                full_listing=False,
                path=self.prefix,
                query_string="policy_extra=true",
            )[1]
            if listing:
                rv[1].extend(listing)
        if ffilter is not None:
            return list(filter(ffilter, rv[1]))
        return rv[1]

    def _list(self):
        return [os.fsencode(o["name"][len(self.prefix) :]) for o in self.__list_objs()]

    def _delete(self, filename):
        self.conn.delete_object(self.container, self.prefix + os.fsdecode(filename))

    def _query(self, filename):
        sobject = self.conn.head_object(self.container, self.prefix + os.fsdecode(filename))
        return {"size": int(sobject["content-length"])}

    def unseal(self, remote_filename):
        try:
            _, body = self.conn.get_object(self.container, remote_filename, resp_chunk_size=1024)
            log.Info(f"File {remote_filename} was successfully unsealed.")
            return body
        except self.resp_exc as e:
            # The object is sealed but being released.
            if e.http_status == 429:
                # The retry-after header contains the remaining duration before
                # the unsealing operation completes.
                duration = int(e.http_response_headers["Retry-After"])
                m, s = divmod(duration, 60)
                h, m = divmod(m, 60)
                eta = f"{int(h)}h{int(m):02}m{int(s):02}s"
                log.Info(f"File {remote_filename} is being unsealed, operation ETA is {eta}.")
            else:
                log.FatalError(
                    f"Connection failed: {e.__class__.__name__} {str(e)}",
                    log.ErrorCode.connection_failed,
                )
        return None

    def pre_process_download_batch(self, remote_filenames):
        """
        This is called before downloading volumes from this backend
        by main engine. For PCA, volumes passed as argument need to be unsealed.
        This method is blocking, showing a status at regular interval
        """
        retry_interval = 60  # status will be shown every 60s
        # remote_filenames are bytes string
        u_remote_filenames = list(map(os.fsdecode, remote_filenames))
        objs = self.__list_objs(
            ffilter=lambda x: os.fsdecode(x["name"]) in [self.prefix + s for s in u_remote_filenames]
        )
        # first step: retrieve pca seal status for all required volumes
        # and launch unseal for all sealed files
        one_object_not_unsealed = False
        for o in objs:
            filename = os.fsdecode(o["name"])
            # see ovh documentation for policy_retrieval_state definition
            policy_retrieval_state = o["policy_retrieval_state"]
            log.Info(f"Volume {filename}. State : {policy_retrieval_state}. ")
            if policy_retrieval_state == "sealed":
                log.Notice(f"Launching unseal of volume {filename}.")
                self.unseal(o["name"])
                one_object_not_unsealed = True
            elif policy_retrieval_state == "unsealing":
                one_object_not_unsealed = True
        # second step: display estimated time for last volume unseal
        # and loop until all volumes are unsealed
        while one_object_not_unsealed:
            one_object_not_unsealed = self.unseal_status(u_remote_filenames)
            time.sleep(retry_interval)
            # might be a good idea to show a progress bar here...
        else:
            log.Notice("All volumes to download are unsealed.")

    def unseal_status(self, u_remote_filenames):
        """
        Shows unsealing status for input volumes
        """
        one_object_not_unsealed = False
        objs = self.__list_objs(
            ffilter=lambda x: os.fsdecode(x["name"]) in [self.prefix + s for s in u_remote_filenames]
        )
        max_duration = 0
        for o in objs:
            policy_retrieval_state = o["policy_retrieval_state"]
            filename = os.fsdecode(o["name"])
            if policy_retrieval_state == "sealed":
                log.Notice(f"Error: volume is still in sealed state : {filename}.")
                log.Notice(f"Launching unseal of volume {filename}.")
                self.unseal(o["name"])
                one_object_not_unsealed = True
            elif policy_retrieval_state == "unsealing":
                duration = int(o["policy_retrieval_delay"])
                log.Info(f"{filename} available in {int(duration)} seconds.")
                if duration > max_duration:
                    max_duration = duration
                one_object_not_unsealed = True

        m, s = divmod(max_duration, 60)
        h, m = divmod(m, 60)
        max_duration_eta = f"{int(h)}h{int(m):02}m{int(s):02}s"
        log.Notice(f"Need to wait {max_duration_eta} before all volumes are unsealed.")
        return one_object_not_unsealed


duplicity.backend.register_backend("pca", PCABackend)
