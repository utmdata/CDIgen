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
Utils for parse command line, check for consistency, and set config
"""

import io
import os
import re
import socket
import sys
from hashlib import md5

# TODO: Remove duplicity.argparse311 when py38 goes EOL
if sys.version_info[:2] == (3, 8):
    from duplicity import argparse311 as argparse
else:
    import argparse

from duplicity import config
from duplicity import dup_time
from duplicity import errors
from duplicity import log
from duplicity import path
from duplicity import selection

gpg_key_patt = re.compile(r"^(0x)?([0-9A-Fa-f]{8}|[0-9A-Fa-f]{16}|[0-9A-Fa-f]{40})$")
url_regexp = re.compile(r"^[\w\+]+://")

help_footer = _("Enter 'duplicity --help' for help screen.")


class CommandLineError(errors.UserError):
    sys.tracebacklimit = 4
    pass


def command_line_error(message):
    """
    Indicate a command line error and exit
    """
    raise CommandLineError(f"{message}\n{help_footer}")


class DuplicityAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        raise NotImplementedError


class DoNothingAction(DuplicityAction):
    def __call__(self, parser, *args, **kw):
        pass


class AddSelectionAction(DuplicityAction):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        addarg = os.fsdecode(value) if isinstance(values, bytes) else values
        config.select_opts.append((os.fsdecode(option_string), addarg))


class AddFilelistAction(DuplicityAction):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        config.select_opts.append((os.fsdecode(option_string), os.fsdecode(values)))
        try:
            config.select_files.append(io.open(values, "rt", encoding="UTF-8"))
        except Exception as e:
            command_line_error(str(e))


class AddRenameAction(DuplicityAction):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        key = os.fsencode(os.path.normcase(os.path.normpath(values[0])))
        config.rename[key] = os.fsencode(values[1])


class SplitOptionsAction(DuplicityAction):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        var = opt2var(option_string)
        opts = getattr(namespace, var)
        values = values.strip('"').strip("'")
        if opts == "":
            opts = values
        else:
            opts = f"{opts} {values}"
        setattr(namespace, var, opts)


class IgnoreErrorsAction(DuplicityAction):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        log.Warn(
            _("Running in 'ignore errors' mode due to --ignore-errors.\n" "Please reconsider if this was not intended")
        )
        config.ignore_errors = True


class WarnAsyncStoreConstAction(argparse._StoreConstAction):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        log.Warn(
            _(
                "Use of the --asynchronous-upload option is experimental "
                "and not safe for production! There are reported cases of "
                "undetected data loss during upload. Be aware and "
                "periodically verify your backups to be safe."
            )
        )
        setattr(namespace, self.dest, self.const)


def _check_int(val):
    try:
        return int(val)
    except Exception as e:
        command_line_error(_(f"'{val}' is not an int: {str(e)}"))


def _check_time(val):
    try:
        return dup_time.genstrtotime(val)
    except dup_time.TimeException as e:
        command_line_error(str(e))


def check_char(val):
    if len(val) == 1:
        return val
    else:
        command_line_error(_(f"'{val} is not a single character."))


def check_count(val):
    return _check_int(val)


def check_file(val):
    try:
        return os.fsencode(expand_fn(val))
    except Exception as e:
        command_line_error(f"{val} is not a valide pathname: {str(e)}")


def check_interval(val):
    try:
        return dup_time.intstringtoseconds(val)
    except dup_time.TimeException as e:
        command_line_error(str(e))


def check_remove_time(val):
    return _check_time(val)


def check_source_path(val):
    if not is_path(val):
        command_line_error(_(f"Source should be pathname, not url.  Got '{val}' instead."))
    if not os.path.exists(val):
        command_line_error(_(f"Argument source_path '{val}' does not exist."))
    return val


def check_source_url(val):
    if not is_url(val):
        command_line_error(_(f"Source should be url, not directory.  Got '{val}' instead."))
    return val


def check_target_dir(val):
    if not is_path(val):
        command_line_error(_(f"Target should be directory, not url.  Got '{val}' instead."))
    if not os.path.exists(val):
        try:
            os.makedirs(val, exist_ok=True)
        except Exception as e:
            command_line_error(_(f"Unable to create target dir '{val}': {str(e)}"))
    return val


def check_target_url(val):
    if not is_url(val):
        command_line_error(_(f"Target should be url, not directory.  Got '{val}' instead."))
    return val


def check_time(val):
    return _check_time(val)


def check_timeout(val):
    """
    set timeout for backends
    """
    val = _check_int(val)
    socket.setdefaulttimeout(val)
    return val


def check_verbosity(val):
    fail = False
    verb = log.NOTICE
    val = val.lower()
    if val in ["e", "error"]:
        verb = log.ERROR
    elif val in ["w", "warning"]:
        verb = log.WARNING
    elif val in ["n", "notice"]:
        verb = log.NOTICE
    elif val in ["i", "info"]:
        verb = log.INFO
    elif val in ["d", "debug"]:
        verb = log.DEBUG
    else:
        try:
            verb = int(val)
            if verb < 0 or verb > 9:
                fail = True
        except ValueError:
            fail = True

    if fail:
        # TRANSL: In this portion of the usage instructions, "[ewnid]" indicates which
        # characters are permitted (e, w, n, i, or d); the brackets imply their own
        # meaning in regex; i.e., only one of the characters is allowed in an instance.
        command_line_error(
            _(
                "Verbosity must be one of: digit [0-9], character [ewnid],\n"
                "or word ['error', 'warning', 'notice', 'info', 'debug'].\n"
                "The default is 3 (Notice).  It is strongly recommended\n"
                "that verbosity level is set at 2 (Warning) or higher."
            )
        )

    log.setverbosity(verb)
    return verb


def dflt(val):
    """
    Return printable value for default.
    """
    return val


def expand_fn(filename):
    return os.path.expanduser(os.path.expandvars(filename))


def expand_archive_dir(archdir, backname):
    """
    Return expanded version of archdir joined with backname.
    """
    assert config.backup_name is not False, "expand_archive_dir() called prior to config.backup_name being set"

    return expand_fn(os.path.join(archdir, os.fsencode(backname)))


def generate_default_backup_name(backend_url):
    """
    @param backend_url: URL to backend.
    @returns A default backup name (string).
    """
    # For default, we hash args to obtain a reasonably safe default.
    # We could be smarter and resolve things like relative paths, but
    # this should actually be a pretty good compromise. Normally only
    # the destination will matter since you typically only restart
    # backups of the same thing to a given destination. The inclusion
    # of the source however, does protect against most changes of
    # source directory (for whatever reason, such as
    # /path/to/different/snapshot). If the user happens to have a case
    # where relative paths are used yet the relative path is the same
    # (but duplicity is run from a different directory or similar),
    # then it is simply up to the user to set --archive-dir properly.
    burlhash = md5()
    burlhash.update(backend_url.encode())
    return burlhash.hexdigest()


def is_url(val):
    """
    Check if val is URL
    """
    return len(val.splitlines()) <= 1 and url_regexp.match(val)


def is_path(val):
    """
    Check if val is PATH
    """
    return not is_url(val)


def make_bytes(value):
    if isinstance(value, str):
        return bytes(value, "utf-8")


def var2cmd(s):
    """
    Convert var name to command string
    """
    return s.replace("_", "-")


def var2opt(s):
    """
    Convert var name to option string
    """
    if len(s) > 1:
        return f"--{s.replace('_', '-')}"
    else:
        return f"-{s}"


def cmd2var(s):
    """
    Convert command string to var name
    """
    return s.replace("-", "_")


def opt2var(s):
    """
    Convert option string to var name
    """
    return s.lstrip("-").replace("-", "_")


def set_log_fd(fd):
    try:
        fd = int(fd)
    except ValueError:
        command_line_error("log_fd must be an integer.")
    if fd < 1:
        command_line_error("log-fd must be greater than zero.")
    log.add_fd(fd)
    return fd


def set_log_file(fn):
    fn = check_file(fn)
    log.add_file(fn)
    return fn


def set_kilos(num):
    return _check_int(num) * 1024


def set_megs(num):
    return _check_int(num) * 1024 * 1024


def set_archive_dir(dirstring):
    """Check archive dir and set global"""
    if not os.path.exists(dirstring):
        try:
            os.makedirs(dirstring)
        except Exception:
            pass
    archive_dir_path = path.Path(dirstring)
    if not archive_dir_path.isdir():
        command_line_error(_(f"Specified archive directory '{archive_dir_path.uc_name}' is not a directory"))
    config.archive_dir_path = archive_dir_path


def set_encrypt_key(encrypt_key):
    """Set config.gpg_profile.encrypt_key assuming proper key given"""
    if not gpg_key_patt.match(encrypt_key):
        command_line_error(
            _(
                f"Encrypt key should be an 8, 16, or 40 character hex string, like 'AA0E73D2'.\n"
                f"Received '{encrypt_key}' length={len(encrypt_key)} instead."
            )
        )
    if config.gpg_profile.recipients is None:
        config.gpg_profile.recipients = []
    config.gpg_profile.recipients.append(encrypt_key)


def set_encrypt_sign_key(encrypt_sign_key):
    """Set config.gpg_profile.encrypt_sign_key assuming proper key given"""
    set_encrypt_key(encrypt_sign_key)
    set_sign_key(encrypt_sign_key)


def set_hidden_encrypt_key(hidden_encrypt_key):
    """Set config.gpg_profile.hidden_encrypt_key assuming proper key given"""
    if not gpg_key_patt.match(hidden_encrypt_key):
        command_line_error(
            _(
                f"Hidden dncrypt key should be an 8, 16, or 40 character hex string, like 'AA0E73D2'.\n"
                f"Received '{hidden_encrypt_key}' length={len(hidden_encrypt_key)} instead."
            )
        )
    if config.gpg_profile.hidden_recipients is None:
        config.gpg_profile.hidden_recipients = []
    config.gpg_profile.hidden_recipients.append(hidden_encrypt_key)


def set_sign_key(sign_key):
    """Set config.gpg_profile.sign_key assuming proper key given"""
    if not gpg_key_patt.match(sign_key):
        command_line_error(
            _(
                f"Sign key should be an 8, 16, or 40 character hex string, like 'AA0E73D2'.\n"
                f"Received '{sign_key}' length={len(sign_key)} instead."
            )
        )
    config.gpg_profile.sign_key = sign_key


def set_selection():
    """Return selection iter starting at filename with arguments applied"""
    sel = selection.Select(config.local_path)
    sel.ParseArgs(config.select_opts, config.select_files)
    config.select = sel.set_iter()
