# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2022 Kenneth Loafman <kenneth@loafman.com>
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

"""
Data for parse command line, check for consistency, and set config
"""

from dataclasses import dataclass

from duplicity import __reldate__
from duplicity import __version__
from duplicity.cli_util import *


@dataclass(order=True)
class DuplicityCommands:
    """
    duplicity commands and positional args expected

    NOTE: cli_util must contain a function named check_* for each positional arg,
          for example check_source_path() to check for source path validity.
    """

    backup = ["source_path", "target_url"]
    cleanup = ["target_url"]
    collection_status = ["target_url"]
    full = ["source_path", "target_url"]
    incremental = ["source_path", "target_url"]
    list_current_files = ["target_url"]
    remove_older_than = ["remove_time", "target_url"]
    remove_all_but_n_full = ["count", "target_url"]
    remove_all_inc_of_but_n_full = ["count", "target_url"]
    restore = ["source_url", "target_dir"]
    verify = ["source_url", "target_dir"]


@dataclass(order=True)
class CommandAliases:
    """
    commands and aliases
    """

    backup = ["bu"]
    cleanup = ["cl"]
    collection_status = ["st"]
    full = ["fb"]
    incremental = ["incr", "inc", "ib"]
    list_current_files = ["ls"]
    remove_older_than = ["ro"]
    remove_all_but_n_full = ["ra"]
    remove_all_inc_of_but_n_full = ["ri"]
    restore = ["rb"]
    verify = ["vb"]


all_commands = set()
for var, aliases in CommandAliases.__dict__.items():
    if var.startswith("__"):
        continue
    all_commands.add(var2cmd(var))
    for alias in aliases:
        all_commands.add(alias)


command_args_expected = dict()
for var, aliases in CommandAliases.__dict__.items():
    if var.startswith("__"):
        continue
    cmd = var2cmd(var)
    expect = len(DuplicityCommands.__dict__[var])
    command_args_expected[cmd] = expect
    for alias in aliases:
        command_args_expected[alias] = expect


"""
Option kwargs for add_argument
"""
OptionKwargs = dict(
    allow_source_mismatch=dict(
        action="store_true",
        help="Allow different source directories",
        default=dflt(config.allow_source_mismatch),
    ),
    archive_dir=dict(
        metavar=_("path"),
        type=check_file,
        help="Path to store metadata archives",
        default=dflt(config.archive_dir),
    ),
    asynchronous_upload=dict(
        action=WarnAsyncStoreConstAction,
        const=1,
        dest="async_concurrency",
        help="Number of async upload tasks, max of 1",
        default=dflt(config.async_concurrency),
    ),
    azure_blob_tier=dict(
        metavar=_("Hot|Cool|Archive"),
        help="Standard storage tier used for storing backup files (Hot|Cool|Archive)",
        default=dflt(config.azure_blob_tier),
    ),
    azure_max_connections=dict(
        metavar=_("number"),
        type=int,
        help="Number of maximum parallel connections to use when the blob size exceeds 64MB",
        default=dflt(config.azure_max_connections),
    ),
    azure_max_block_size=dict(
        metavar=_("number"),
        type=int,
        help="Number for the block size to upload a blob if the length is unknown\n"
        "or is larger than the value set by --azure-max-single-put-size\n"
        "The maximum block size the service supports is 100MiB.",
        default=dflt(config.azure_max_block_size),
    ),
    azure_max_single_put_size=dict(
        metavar=_("number"),
        type=int,
        help="Largest supported upload size where the Azure library makes only one put call.\n"
        "Used to upload a single block if the content length is known and is less than this",
        default=dflt(config.azure_max_single_put_size),
    ),
    b2_hide_files=dict(
        action="store_true",
        help="Whether the B2 backend hides files instead of deleting them",
        default=dflt(config.b2_hide_files),
    ),
    backend_retry_delay=dict(
        metavar=_("seconds"),
        type=int,
        help="Delay time before next try after a failure of a backend operation",
        default=dflt(config.backend_retry_delay),
    ),
    cf_backend=dict(
        metavar="pyrax|cloudfiles",
        help="Allow the user to switch cloudfiles backend",
        default=dflt(config.cf_backend),
    ),
    compare_data=dict(
        action="store_true",
        help="Compare data on verify not only signatures",
        default=dflt(config.compare_data),
    ),
    config_dir=dict(
        metavar=_("path"),
        type=check_file,
        help="Path to store configuration files",
        default=dflt(config.config_dir),
    ),
    copy_blocksize=dict(
        metavar=_("number"),
        type=set_kilos,
        help="Blocksize to use in copy operations in kilobytes.",
        default=dflt(config.copy_blocksize),
    ),
    copy_links=dict(
        action="store_true",
        help="Copy contents of symlinks instead of linking",
        default=dflt(config.copy_links),
    ),
    dry_run=dict(
        action="store_true",
        help="Perform dry-run with no writes",
        default=dflt(config.dry_run),
    ),
    encrypt_key=dict(
        metavar=_("gpg-key-id"),
        type=set_encrypt_key,
        help="GNUpg key for encryption/decryption",
        default=dflt(None),
    ),
    encrypt_sign_key=dict(
        metavar=_("gpg-key-id"),
        type=set_encrypt_sign_key,
        help="GNUpg key for encryption/decryption and signing",
        default=dflt(None),
    ),
    encrypt_secret_keyring=dict(
        metavar=_("path"),
        help="Path to secret GNUpg keyring",
        default=dflt(None),
    ),
    exclude=dict(
        metavar=_("shell_pattern"),
        action=AddSelectionAction,
        help="Exclude globbing pattern",
        default=dflt(None),
    ),
    exclude_device_files=dict(
        nargs=0,
        action=AddSelectionAction,
        help="Exclude device files",
        default=dflt(False),
    ),
    exclude_filelist=dict(
        metavar=_("filename"),
        action=AddFilelistAction,
        help="File with list of file patterns to exclude",
        default=dflt(None),
    ),
    exclude_if_present=dict(
        metavar=_("filename"),
        action=AddSelectionAction,
        help="Exclude directory if this file is present",
        default=dflt(None),
    ),
    exclude_older_than=dict(
        metavar=_("time"),
        action=AddSelectionAction,
        help="Exclude files older than time",
        default=dflt(None),
    ),
    exclude_other_filesystems=dict(
        nargs=0,
        action=AddSelectionAction,
        help="Exclude other filesystems from backup",
        default=dflt(False),
    ),
    exclude_regexp=dict(
        metavar=_("regex"),
        action=AddSelectionAction,
        help="Exclude based on regex pattern",
        default=dflt(None),
    ),
    file_changed=dict(
        metavar=_("path"),
        type=check_file,
        help="Whether to collect only the file status, not the whole root",
        default=dflt(None),
    ),
    file_prefix=dict(
        metavar="string",
        type=make_bytes,
        help="String prefix for all duplicity files",
        default=dflt(config.file_prefix),
    ),
    file_prefix_archive=dict(
        metavar="string",
        type=make_bytes,
        help="String prefix for duplicity difftar files",
        default=dflt(config.file_prefix_archive),
    ),
    file_prefix_manifest=dict(
        metavar="string",
        type=make_bytes,
        help="String prefix for duplicity manifest files",
        default=dflt(config.file_prefix_manifest),
    ),
    file_prefix_signature=dict(
        metavar="string",
        type=make_bytes,
        help="String prefix for duplicity signature files",
        default=dflt(config.file_prefix_signature),
    ),
    file_prefix_jsonstat=dict(
        metavar="string",
        type=make_bytes,
        help="String prefix for duplicity jsonstat files",
        default=dflt(config.file_prefix_jsonstat),
    ),
    files_from=dict(
        metavar=_("filename"),
        type=check_file,
        action=AddFilelistAction,
        help="Defines the backup source as a sub-set of the source folder",
        default=dflt(None),
    ),
    filter_globbing=dict(
        nargs=0,
        action=AddSelectionAction,
        help="File selection mode switch, changes the interpretation of any subsequent\n"
        "--exclude* or --include* options to shell globbing.",
        default=dflt(None),
    ),
    filter_ignorecase=dict(
        nargs=0,
        action=AddSelectionAction,
        help="File selection mode switch, changes the interpretation of any subsequent\n"
        "--exclude* or --include* options to case-insensitive matching.",
        default=dflt(None),
    ),
    filter_literal=dict(
        nargs=0,
        action=AddSelectionAction,
        help="File selection mode switch, changes the interpretation of any subsequent\n"
        "--exclude* or --include* options to literal strings.",
        default=dflt(None),
    ),
    filter_regexp=dict(
        nargs=0,
        action=AddSelectionAction,
        help="File selection mode switch, changes the interpretation of any subsequent\n"
        "--exclude* or --include* options to regular expressions.",
        default=dflt(None),
    ),
    filter_strictcase=dict(
        nargs=0,
        action=AddSelectionAction,
        help="File selection mode switch, changes the interpretation of any subsequent\n"
        "--exclude* or --include* options to case-sensitive matching.",
        default=dflt(None),
    ),
    force=dict(
        action="store_true",
        help="Force duplicity to actually delete during cleanup",
        default=dflt(config.force),
    ),
    ftp_passive=dict(
        action="store_const",
        const="passive",
        dest="ftp_connection",
        help="Tell FTP to use passive mode",
        default=dflt(config.ftp_connection),
    ),
    ftp_regular=dict(
        action="store_const",
        const="regular",
        dest="ftp_connection",
        help="Tell FTP to use regular mode",
        default=dflt(config.ftp_connection),
    ),
    full_if_older_than=dict(
        metavar=_("interval"),
        type=check_interval,
        help="Perform full backup if last full is older than 'time'",
        default=dflt(config.full_if_older_than),
    ),
    gpg_binary=dict(
        metavar=_("path"),
        type=check_file,
        help="Path to GNUpg executable file",
        default=dflt(config.gpg_binary),
    ),
    gpg_options=dict(
        metavar=_("options"),
        action=SplitOptionsAction,
        help="Verbatim gpg options.  May be supplied multiple times.",
        default=dflt(config.gpg_options),
    ),
    hidden_encrypt_key=dict(
        metavar=_("gpg-key-id"),
        type=set_hidden_encrypt_key,
        help="Hidden GNUpg encryption key",
        default=dflt(None),
    ),
    idr_fakeroot=dict(
        metavar=_("path"),
        type=check_file,
        help="Fake root for idrive backend",
        default=dflt(config.idr_fakeroot),
    ),
    ignore_errors=dict(
        nargs=0,
        action=IgnoreErrorsAction,
        help="Ignore most errors during processing",
        default=dflt(config.ignore_errors),
    ),
    imap_full_address=dict(
        action="store_true",
        help="Whether to use the full email address as the user name",
        default=dflt(config.imap_full_address),
    ),
    imap_mailbox=dict(
        metavar=_("imap_mailbox"),
        help="Name of the imap folder to store backups",
        default=dflt(config.imap_mailbox),
    ),
    include=dict(
        metavar=_("shell_pattern"),
        action=AddSelectionAction,
        help="Include globbing pattern",
        default=dflt(None),
    ),
    include_filelist=dict(
        metavar=_("filename"),
        action=AddFilelistAction,
        help="File with list of file patterns to include",
        default=dflt(None),
    ),
    include_regexp=dict(
        metavar=_("regex"),
        action=AddSelectionAction,
        help="Include based on regex pattern",
        default=dflt(None),
    ),
    jsonstat=dict(
        action="store_true",
        help=_(
            "If set, an extra file with statistics in json format will be stored with each backup. "
            "It includes the statistics printed out on stdout by default. "
            "With 'collection-status' it returs these stats."
        ),
        default=dflt(config.jsonstat),
    ),
    # log_fd is directly applied in set_log_fd(), not saved in config
    log_fd=dict(
        metavar=_("file_descriptor"),
        dest="",
        type=set_log_fd,
        help="File descriptor to be used for logging",
    ),
    # log_file is directly applied in set_log_file(), not saved in config
    log_file=dict(
        metavar=_("log_filename"),
        dest="",
        type=set_log_file,
        help="Logging filename to use",
    ),
    log_timestamp=dict(
        action="store_true",
        help="Whether to include timestamp and level in log",
        default=dflt(False),
    ),
    max_blocksize=dict(
        metavar=_("number"),
        type=int,
        help="Maximum block size for large files in MB",
        default=dflt(config.max_blocksize),
    ),
    metadata_sync_mode=dict(
        choices=("full", "partial"),
        help="Only sync required metadata not all",
        default=dflt(config.metadata_sync_mode),
    ),
    mf_purge=dict(
        action="store_true",
        help="Option for mediafire to purge files on delete instead of sending to trash",
        default=dflt(config.mf_purge),
    ),
    mp_segment_size=dict(
        metavar=_("number"),
        type=set_megs,
        help="Swift backend segment size in megabytes",
        default=dflt(config.mp_segment_size),
    ),
    name=dict(
        metavar=_("backup name"),
        dest="backup_name",
        help="Custom backup name instead of hash",
        default=dflt(config.backup_name),
    ),
    no_compression=dict(
        action="store_false",
        dest="compression",
        help="If supplied do not perform compression",
        default=dflt(config.compression),
    ),
    no_encryption=dict(
        action="store_false",
        dest="encryption",
        help="If supplied do not perform encryption",
        default=dflt(config.encryption),
    ),
    no_files_changed=dict(
        action="store_false",
        dest="files_changed",
        help="If supplied do not collect the files_changed list",
        default=dflt(config.files_changed),
    ),
    no_restore_ownership=dict(
        action="store_false",
        dest="restore_ownership",
        help="If supplied do not restore uid/gid when finished",
        default=dflt(config.restore_ownership),
    ),
    no_print_statistics=dict(
        action="store_false",
        dest="print_statistics",
        help="If supplied do not print statistics",
        default=dflt(config.print_statistics),
    ),
    null_separator=dict(
        action="store_true",
        help="Whether to split on null instead of newline",
        default=dflt(config.null_separator),
    ),
    num_retries=dict(
        metavar=_("number"),
        type=int,
        help="Number of retries on network operations",
        default=dflt(config.num_retries),
    ),
    numeric_owner=dict(
        action="store_true",
        help="Keeps number from tar file. Like same option in GNU tar.",
        default=dflt(config.numeric_owner),
    ),
    par2_options=dict(
        metavar=_("options"),
        action=SplitOptionsAction,
        help="Verbatim par2 options.  May be supplied multiple times.",
        default=dflt(config.par2_options),
    ),
    par2_redundancy=dict(
        metavar=_("number"),
        type=int,
        help="Level of Redundancy in percent for Par2 files",
        default=dflt(config.par2_redundancy),
    ),
    par2_volumes=dict(
        metavar=_("number"),
        type=int,
        help="Number of par2 volumes",
        default=dflt(config.par2_volumes),
    ),
    path_to_restore=dict(
        metavar=_("path"),
        type=check_file,
        dest="restore_path",
        help="File or directory path to restore",
        default=dflt(config.restore_path),
    ),
    progress=dict(
        action="store_true",
        help="Display progress for the full and incremental backup operations",
        default=dflt(config.progress),
    ),
    progress_rate=dict(
        metavar=_("number"),
        type=int,
        help="Used to control the progress option update rate in seconds",
        default=dflt(config.progress_rate),
    ),
    rename=dict(
        metavar="from to",
        action=AddRenameAction,
        nargs=2,
        help="Rename files during restore",
        default=dflt(config.rename),
    ),
    restore_time=dict(
        metavar=_("time"),
        type=check_time,
        help="Restores will try to bring back the state as of the following time",
        default=dflt(config.restore_time),
    ),
    rsync_options=dict(
        metavar=_("options"),
        action=SplitOptionsAction,
        help="Verbatim rsync options.  May be supplied multiple times.",
        default=dflt(config.rsync_options),
    ),
    s3_endpoint_url=dict(
        metavar=_("s3_endpoint_url"),
        action="store",
        help="Specity S3 endpoint",
        default=dflt(config.s3_endpoint_url),
    ),
    s3_unencrypted_connection=dict(
        action="store_true",
        help="Whether to use plain HTTP (without SSL) to send data to S3",
        default=dflt(config.s3_unencrypted_connection),
    ),
    s3_use_deep_archive=dict(
        action="store_true",
        help="Whether to use S3 Glacier Deep Archive Storage",
        default=dflt(config.s3_use_deep_archive),
    ),
    s3_use_glacier=dict(
        action="store_true",
        help="Whether to use S3 Glacier Storage",
        default=dflt(config.s3_use_glacier),
    ),
    s3_use_glacier_ir=dict(
        action="store_true",
        help="Whether to use S3 Glacier IR Storage",
        default=dflt(config.s3_use_glacier_ir),
    ),
    s3_use_ia=dict(
        action="store_true",
        help="Whether to use S3 Infrequent Access Storage",
        default=dflt(config.s3_use_ia),
    ),
    s3_use_onezone_ia=dict(
        action="store_true",
        help="Whether to use S3 One Zone Infrequent Access Storage",
        default=dflt(config.s3_use_onezone_ia),
    ),
    s3_use_rrs=dict(
        action="store_true",
        help="Whether to use S3 Reduced Redundancy Storage",
        default=dflt(config.s3_use_rrs),
    ),
    s3_multipart_chunk_size=dict(
        metavar=_("number"),
        type=set_megs,
        help="Chunk size used for S3 multipart uploads.The number of parallel uploads to\n"
        "S3 be given by chunk size / volume size. Use this to maximize the use of\n"
        "your bandwidth",
        default=dflt(config.s3_multipart_chunk_size),
    ),
    s3_multipart_max_procs=dict(
        metavar=_("number"),
        type=int,
        help="Number of processes to set the Processor Pool to when uploading multipart\n"
        "uploads to S3. Use this to control the maximum simultaneous uploads to S3",
        default=dflt(config.s3_multipart_max_procs),
    ),
    s3_use_server_side_encryption=dict(
        action="store_true",
        dest="s3_use_sse",
        help="Allow use of server side encryption",
        default=dflt(config.s3_use_sse),
    ),
    s3_use_server_side_kms_encryption=dict(
        action="store_true",
        dest="s3_use_sse_kms",
        help="Allow use of server side KMS encryption",
        default=dflt(config.s3_use_sse_kms),
    ),
    s3_kms_key_id=dict(
        metavar=_("s3_kms_key_id"),
        action="store",
        help="S3 KMS encryption key id",
        default=dflt(config.s3_kms_key_id),
    ),
    s3_kms_grant=dict(
        metavar=_("s3_kms_grant"),
        action="store",
        help="S3 KMS grant value",
        default=dflt(config.s3_kms_grant),
    ),
    s3_region_name=dict(
        metavar=_("s3_region_name"),
        action="store",
        help="Specity S3 region name",
        default=dflt(config.s3_region_name),
    ),
    swift_storage_policy=dict(
        metavar=_("policy"),
        help="Option to specify a Swift container storage policy.",
        default=dflt(config.swift_storage_policy),
    ),
    scp_command=dict(
        metavar=_("command"),
        help="SCP command to use (ssh pexpect backend)",
        default=dflt(config.scp_command),
    ),
    sftp_command=dict(
        metavar=_("command"),
        help="SFTP command to use (ssh pexpect backend)",
        default=dflt(config.sftp_command),
    ),
    show_changes_in_set=dict(
        metavar=_("number"),
        type=int,
        help="Show file changes (new, deleted, changed) in the specified backup\n"
        "set (0 specifies latest, 1 specifies next latest, etc.)",
        default=dflt(config.show_changes_in_set),
    ),
    sign_key=dict(
        metavar=_("gpg-key-id"),
        type=set_sign_key,
        help="Sign key for encryption/decryption",
        default=dflt(None),
    ),
    skip_if_no_change=dict(
        action="store_true",
        help="Skip incremental backup if nothing changed.",
        default=dflt(config.skip_if_no_change),
    ),
    ssh_askpass=dict(
        action="store_true",
        help="Ask the user for the SSH password. Not for batch usage",
        default=dflt(config.ssh_askpass),
    ),
    ssh_options=dict(
        metavar=_("options"),
        action=SplitOptionsAction,
        help="Verbatim ssh options.  May be supplied multiple times.",
        default=dflt(config.ssh_options),
    ),
    ssl_cacert_file=dict(
        metavar="file",
        help=_("pem formatted bundle of certificate authorities"),
        default=dflt(config.ssl_cacert_file),
    ),
    ssl_cacert_path=dict(
        metavar="path",
        help=_("path to a folder with certificate authority files"),
        default=dflt(config.ssl_cacert_path),
    ),
    ssl_no_check_certificate=dict(
        action="store_true",
        help="Set to not validate SSL certificates",
        default=dflt(config.ssl_no_check_certificate),
    ),
    tempdir=dict(
        metavar=_("path"),
        type=check_file,
        dest="temproot",
        help="Working directory for temp files",
        default=dflt(config.temproot),
    ),
    timeout=dict(
        metavar=_("seconds"),
        type=check_timeout,
        help="Network timeout in seconds",
        default=dflt(config.timeout),
    ),
    time_separator=dict(
        metavar=_("char"),
        type=check_char,
        help="Character used like the ':' in time strings like=2002-08-06T04:22:00-07:00\n"
        "Note=Not valid for backup commands full and inc, only to read older backups",
        default=dflt(config.time_separator),
    ),
    use_agent=dict(
        action="store_true",
        help="Whether to specify --use-agent in GnuPG options",
        default=dflt(config.use_agent),
    ),
    # verbosity is set directly via check_verbosity(), not saved in config
    verbosity=dict(
        metavar=_("verb"),
        dest="",
        type=check_verbosity,
        help="Logging verbosity=[0-9] or [e, w, n, i, d] or [error, warning, notice, info, debug]",
    ),
    version=dict(
        action="version",
        version=f"duplicity {__version__} {__reldate__}",
        help="Display version and exit",
    ),
    volsize=dict(
        metavar=_("number"),
        type=set_megs,
        help="Volume size to use in MiB",
        default=dflt(config.volsize),
    ),
    webdav_headers=dict(
        metavar="string",
        help=_("extra headers for Webdav, like 'Cookie,name=value'"),
        default=dflt(config.webdav_headers),
    ),
    # TESTING ONLY - do not use in production
    current_time=dict(
        metavar="time",
        type=int,
        help=argparse.SUPPRESS,
    ),
    fail_on_volume=dict(
        metavar="volume",
        type=int,
        help=argparse.SUPPRESS,
    ),
    pydevd=dict(
        action="store_true",
        help=argparse.SUPPRESS,
    ),
    skip_volume=dict(
        metavar="volume",
        type=int,
        help=argparse.SUPPRESS,
    ),
)


@dataclass(order=True)
class OptionAliases:
    path_to_restore = ["-r"]
    restore_time = ["-t", "--time"]
    verbosity = ["-v"]
    version = ["-V"]


logging_options = {
    "--log-fd",
    "--log-file",
    "--log-timestamp",
    "--verbosity",
    "--version",
}

backup_only_options = {
    "--allow-source-mismatch",
    "--asynchronous-upload",
    "--dry-run",
    "--volsize",
}

selection_only_options = {
    "--exclude",
    "--exclude-device-files",
    "--exclude-filelist",
    "--exclude-if-present",
    "--exclude-older-than",
    "--exclude-other-filesystems",
    "--exclude-regexp",
    "--include",
    "--include-filelist",
    "--include-regexp",
    "--files-from",
    "--filter-globbing",
    "--filter-ignorecase",
    "--filter-literal",
    "--filter-regexp",
    "--filter-strictcase",
}

changed_options = {
    "--file-to-restore",
    "--do-not-restore-ownership",
}

removed_options = {
    "--gio",
    "--old-filenames",
    "--short-filenames",
    "--exclude-globbing-filelist",
    "--include-globbing-filelist",
    "--exclude-filelist-stdin",
    "--include-filelist-stdin",
    "--s3-multipart-max-timeout",
    "--s3-european-buckets",
    "--s3-use-multiprocessing",
    "--s3-use-new-style",
}

removed_backup_options = {
    "--time-separator",
}

# make list of all options available
all_options = {var2opt(var) for var in OptionKwargs.keys()}


@dataclass(order=True)
class CommandOptions:
    """
    legal options by command
    """

    backup = list(
        all_options,
    )
    cleanup = list(
        all_options - backup_only_options - selection_only_options,
    )
    collection_status = list(
        all_options - backup_only_options - selection_only_options,
    )
    full = list(
        all_options,
    )
    incremental = list(
        all_options,
    )
    list_current_files = list(
        all_options - backup_only_options - selection_only_options,
    )
    remove_older_than = list(
        all_options - backup_only_options - selection_only_options,
    )
    remove_all_but_n_full = list(
        all_options - backup_only_options - selection_only_options,
    )
    remove_all_inc_of_but_n_full = list(
        all_options - backup_only_options - selection_only_options,
    )
    restore = list(
        all_options - backup_only_options - selection_only_options,
    )
    verify = list(
        all_options - backup_only_options,
    )


trans = {
    # TRANSL: Used in usage help to represent a Unix-style path name. Example:
    # rsync://user[:password]@other_host[:port]//absolute_path
    "absolute_path": _("absolute_path"),
    # TRANSL: Used in usage help. Example:
    # tahoe://alias/some_dir
    "alias": _("alias"),
    # TRANSL: Used in help to represent a "bucket name" for Amazon Web
    # Services' Simple Storage Service (S3). Example:
    # s3://other.host/bucket_name[/prefix]
    "bucket_name": _("bucket_name"),
    # TRANSL: abbreviation for "character" (noun)
    "char": _("char"),
    # TRANSL: noun
    "command": _("command"),
    # TRANSL: Used in usage help to represent the name of a container in
    # Amazon Web Services' Cloudfront. Example:
    # cf+http://container_name
    "container_name": _("container_name"),
    # TRANSL: noun
    "count": _("count"),
    # TRANSL: Used in usage help to represent the name of a file directory
    "directory": _("directory"),
    # TRANSL: Used in usage help to represent the name of a file. Example:
    # --log-file <filename>
    "filename": _("filename"),
    # TRANSL: Used in usage help to represent an ID for a GnuPG key. Example:
    # --encrypt-key <gpg_key_id>
    "gpg_key_id": _("gpg-key-id"),
    # TRANSL: Used in usage help, e.g. to represent the name of a code
    # module. Example:
    # rsync://user[:password]@other.host[:port]::/module/some_dir
    "module": _("module"),
    # TRANSL: Used in usage help to represent a desired number of
    # something. Example:
    # --num-retries <number>
    "number": _("number"),
    # TRANSL: Used in usage help. (Should be consistent with the "Options:"
    # header.) Example:
    # duplicity [full|incremental] [options] source_path target_url
    "options": _("options"),
    # TRANSL: Used in usage help to represent an internet hostname. Example:
    # ftp://user[:password]@other.host[:port]/some_dir
    "other_host": _("other.host"),
    # TRANSL: Used in usage help. Example:
    # ftp://user[:password]@other.host[:port]/some_dir
    "password": _("password"),
    # TRANSL: Used in usage help to represent a Unix-style path name. Example:
    # --archive-dir <path>
    "path": _("path"),
    # TRANSL: Used in usage help to represent a TCP port number. Example:
    # ftp://user[:password]@other.host[:port]/some_dir
    "port": _("port"),
    # TRANSL: Used in usage help. This represents a string to be used as a
    # prefix to names for backup files created by Duplicity. Example:
    # s3://other.host/bucket_name[/prefix]
    "prefix": _("prefix"),
    # TRANSL: Used in usage help to represent a Unix-style path name. Example:
    # rsync://user[:password]@other.host[:port]/relative_path
    "relative_path": _("relative_path"),
    # TRANSL: Used in usage help. Example:
    # --timeout <seconds>
    "seconds": _("seconds"),
    # TRANSL: Used in usage help to represent a "glob" style pattern for
    # matching one or more files, as described in the documentation.
    # Example:
    # --exclude <shell_pattern>
    "shell_pattern": _("shell_pattern"),
    # TRANSL: Used in usage help to represent the name of a single file
    # directory or a Unix-style path to a directory. Example:
    # file:///some_dir
    "some_dir": _("some_dir"),
    # TRANSL: Used in usage help to represent the name of a single file
    # directory or a Unix-style path to a directory where files will be
    # coming FROM. Example:
    # duplicity [full|incremental] [options] source_path target_url
    "source_path": _("source_path"),
    # TRANSL: Used in usage help to represent a URL files will be coming
    # FROM. Example:
    # duplicity [restore] [options] source_url target_dir
    "source_url": _("source_url"),
    # TRANSL: Used in usage help to represent the name of a single file
    # directory or a Unix-style path to a directory. where files will be
    # going TO. Example:
    # duplicity [restore] [options] source_url target_dir
    "target_dir": _("target_dir"),
    # TRANSL: Used in usage help to represent a URL files will be going TO.
    # Example:
    # duplicity [full|incremental] [options] source_path target_url
    "target_url": _("target_url"),
    # TRANSL: Used in usage help to represent a time spec for a previous
    # point in time, as described in the documentation. Example:
    # duplicity remove-older-than time [options] target_url
    "time": _("time"),
    # TRANSL: Used in usage help to represent a user name (i.e. login).
    # Example:
    # ftp://user[:password]@other.host[:port]/some_dir
    "user": _("user"),
    # TRANSL: account id for b2. Example: b2://account_id@bucket/
    "account_id": _("account_id"),
    # TRANSL: application_key for b2.
    # Example: b2://account_id:application_key@bucket/
    "application_key": _("application_key"),
    # TRANSL: remote name for rclone.
    # Example: rclone://remote:/some_dir
    "remote": _("remote"),
}

help_url_formats = (
    _("Backends and their URL formats:")
    + f"""
  azure://{trans['container_name']}
  b2://{trans['account_id']}[:{trans['application_key']}]@{trans['bucket_name']}/[{trans['some_dir']}/]
  boto3+s3://{trans['bucket_name']}[/{trans['prefix']}]
  cf+http://{trans['container_name']}
  dpbx:///{trans['some_dir']}
  file:///{trans['some_dir']}
  ftp://{trans['user']}[:{trans['password']}]@{trans['other_host']}[:{trans['port']}]/{trans['some_dir']}
  ftps://{trans['user']}[:{trans['password']}]@{trans['other_host']}[:{trans['port']}]/{trans['some_dir']}
  gdocs://{trans['user']}[:{trans['password']}]@{trans['other_host']}/{trans['some_dir']}
  for gdrive:// a <service-account-url> like the following is required
        <serviceaccount-name>@<serviceaccount-name>.iam.gserviceaccount.com
  gdrive://<service-account-url>/target-folder/?driveID=<SHARED DRIVE ID> (for GOOGLE Shared Drive)
  gdrive://<service-account-url>/target-folder/?myDriveFolderID=<google-myDrive-folder-id> (for GOOGLE MyDrive)
  hsi://{trans['user']}[:{trans['password']}]@{trans['other_host']}[:{trans['port']}]/{trans['some_dir']}
  imap://{trans['user']}[:{trans['password']}]@{trans['other_host']}[:{trans['port']}]/{trans['some_dir']}
  mega://{trans['user']}[:{trans['password']}]@{trans['other_host']}/{trans['some_dir']}
  megav2://{trans['user']}[:{trans['password']}]@{trans['other_host']}/{trans['some_dir']}
  mf://{trans['user']}[:{trans['password']}]@{trans['other_host']}/{trans['some_dir']}
  onedrive://{trans['some_dir']}
  pca://{trans['container_name']}
  pydrive://{trans['user']}@{trans['other_host']}/{trans['some_dir']}
  rclone://{trans['remote']}:/{trans['some_dir']}
  rsync://{trans['user']}[:{trans['password']}]@{trans['other_host']}[:{trans['port']}]/{trans['relative_path']}
  rsync://{trans['user']}[:{trans['password']}]@{trans['other_host']}[:{trans['port']}]//{trans['absolute_path']}
  rsync://{trans['user']}[:{trans['password']}]@{trans['other_host']}[:{trans['port']}]::/{trans['module']}/{trans['some_dir']}
  s3+http://{trans['bucket_name']}[/{trans['prefix']}]
  s3://{trans['other_host']}[:{trans['port']}]/{trans['bucket_name']}[/{trans['prefix']}]
  scp://{trans['user']}[:{trans['password']}]@{trans['other_host']}[:{trans['port']}]/{trans['some_dir']}
  ssh://{trans['user']}[:{trans['password']}]@{trans['other_host']}[:{trans['port']}]/{trans['some_dir']}
  swift://{trans['container_name']}
  tahoe://{trans['alias']}/{trans['directory']}
  webdav://{trans['user']}[:{trans['password']}]@{trans['other_host']}/{trans['some_dir']}
  webdavs://{trans['user']}[:{trans['password']}]@{trans['other_host']}/{trans['some_dir']}
"""
)
