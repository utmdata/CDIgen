#!/usr/bin/env python3
# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# duplicity -- Encrypted bandwidth efficient backup
#
# Copyright 2002 Ben Escoto <ben@emerose.org>
# Copyright 2007 Kenneth Loafman <kenneth@loafman.com>
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
#
# See http://www.nongnu.org/duplicity for more information.
# Please send mail to me or the mailing list if you find bugs or have
# any suggestions.

import sys

import duplicity.errors
from duplicity import gpg
from duplicity import log
from duplicity import tempdir
from duplicity import util
from duplicity.dup_main import main

sys.stdout.reconfigure(errors="surrogateescape")
sys.stderr.reconfigure(errors="surrogateescape")


def with_tempdir(fn):
    """
    Execute function and guarantee cleanup of tempdir is called

    @type fn: callable function
    @param fn: function to execute

    @return: void
    @rtype: void
    """
    try:
        fn()
    finally:
        tempdir.default().cleanup()


def dup_run():
    try:
        log.setup()
        util.start_debugger()
        with_tempdir(main)

    # Don't move this lower.  In order to get an exit
    # status out of the system, you have to call the
    # sys.exit() function.  Python handles this by
    # raising the SystemExit exception.  Cleanup code
    # goes here, if needed.
    except SystemExit as e:
        # No traceback, just get out
        util.release_lockfile()
        sys.exit(e.code)

    except KeyboardInterrupt as e:
        # No traceback, just get out
        log.Info(_("INT intercepted...exiting."))
        util.release_lockfile()
        sys.exit(4)

    except gpg.GPGError as e:
        # For gpg errors, don't show an ugly stack trace by
        # default. But do with sufficient verbosity.
        util.release_lockfile()
        log.Info(_("GPG error detail: %s") % util.exception_traceback())
        log.FatalError(f"{e.__class__.__name__}: {e.args[0]}", log.ErrorCode.gpg_failed, e.__class__.__name__)

    except duplicity.errors.UserError as e:
        util.release_lockfile()
        # For user errors, don't show an ugly stack trace by
        # default. But do with sufficient verbosity.
        log.Info(_("User error detail: %s") % util.exception_traceback())
        log.FatalError(f"{e.__class__.__name__}: {util.uexc(e)}", log.ErrorCode.user_error, e.__class__.__name__)

    except duplicity.errors.BackendException as e:
        util.release_lockfile()
        # For backend errors, don't show an ugly stack trace by
        # default. But do with sufficient verbosity.
        log.Info(_("Backend error detail: %s") % util.exception_traceback())
        log.FatalError(f"{e.__class__.__name__}: {util.uexc(e)}", log.ErrorCode.user_error, e.__class__.__name__)

    except Exception as e:
        util.release_lockfile()
        if "Forced assertion for testing" in util.uexc(e):
            log.FatalError(f"{e.__class__.__name__}: {util.uexc(e)}", log.ErrorCode.exception, e.__class__.__name__)
        else:
            # Traceback and that mess
            log.FatalError(util.exception_traceback(), log.ErrorCode.exception, e.__class__.__name__)


if __name__ == "__main__":
    dup_run()
