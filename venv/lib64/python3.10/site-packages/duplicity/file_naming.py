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

"""Produce and parse the names of duplicity's backup files"""

import re

from duplicity import config
from duplicity import dup_time
from duplicity.errors import DuplicityError

full_vol_re = None
full_vol_re_short = None
full_manifest_re = None
full_manifest_re_short = None
inc_vol_re = None
inc_vol_re_short = None
inc_manifest_re = None
inc_manifest_re_short = None
full_sig_re = None
full_sig_re_short = None
new_sig_re = None
new_sig_re_short = None


def prepare_regex(force=False):
    global full_vol_re
    global full_vol_re_short
    global full_manifest_re
    global full_manifest_re_short
    global inc_vol_re
    global inc_vol_re_short
    global inc_manifest_re
    global inc_manifest_re_short
    global full_sig_re
    global full_sig_re_short
    global new_sig_re
    global new_sig_re_short
    global stat_re
    global stat_re_short

    # we force regex re-generation in unit tests because file prefixes might have changed
    if full_vol_re and not force:
        return

    full_vol_re = re.compile(
        b"^" + config.file_prefix + config.file_prefix_archive + b"duplicity-full"
        b"\\.(?P<time>.*?)"
        b"\\.vol(?P<num>[0-9]+)"
        b"\\.difftar"
        b"(?P<partial>(\\.part))?"
        b"($|\\.)"
    )

    full_vol_re_short = re.compile(
        b"^" + config.file_prefix + config.file_prefix_archive + b"df"
        b"\\.(?P<time>[0-9a-z]+?)"
        b"\\.(?P<num>[0-9a-z]+)"
        b"\\.dt"
        b"(?P<partial>(\\.p))?"
        b"($|\\.)"
    )

    full_manifest_re = re.compile(
        b"^" + config.file_prefix + config.file_prefix_manifest + b"duplicity-full"
        b"\\.(?P<time>.*?)"
        b"\\.manifest"
        b"(?P<partial>(\\.part))?"
        b"($|\\.)"
    )

    full_manifest_re_short = re.compile(
        b"^" + config.file_prefix + config.file_prefix_manifest + b"df"
        b"\\.(?P<time>[0-9a-z]+?)"
        b"\\.m"
        b"(?P<partial>(\\.p))?"
        b"($|\\.)"
    )

    inc_vol_re = re.compile(
        b"^" + config.file_prefix + config.file_prefix_archive + b"duplicity-inc"
        b"\\.(?P<start_time>.*?)"
        b"\\.to\\.(?P<end_time>.*?)"
        b"\\.vol(?P<num>[0-9]+)"
        b"\\.difftar"
        b"($|\\.)"
    )

    inc_vol_re_short = re.compile(
        b"^" + config.file_prefix + config.file_prefix_archive + b"di"
        b"\\.(?P<start_time>[0-9a-z]+?)"
        b"\\.(?P<end_time>[0-9a-z]+?)"
        b"\\.(?P<num>[0-9a-z]+)"
        b"\\.dt"
        b"($|\\.)"
    )

    inc_manifest_re = re.compile(
        b"^" + config.file_prefix + config.file_prefix_manifest + b"duplicity-inc"
        b"\\.(?P<start_time>.*?)"
        b"\\.to"
        b"\\.(?P<end_time>.*?)"
        b"\\.manifest"
        b"(?P<partial>(\\.part))?"
        b"(\\.|$)"
    )

    inc_manifest_re_short = re.compile(
        b"^" + config.file_prefix + config.file_prefix_manifest + b"di"
        b"\\.(?P<start_time>[0-9a-z]+?)"
        b"\\.(?P<end_time>[0-9a-z]+?)"
        b"\\.m"
        b"(?P<partial>(\\.p))?"
        b"(\\.|$)"
    )

    full_sig_re = re.compile(
        b"^" + config.file_prefix + config.file_prefix_signature + b"duplicity-full-signatures"
        b"\\.(?P<time>.*?)"
        b"\\.sigtar"
        b"(?P<partial>(\\.part))?"
        b"(\\.|$)"
    )

    full_sig_re_short = re.compile(
        b"^" + config.file_prefix + config.file_prefix_signature + b"dfs"
        b"\\.(?P<time>[0-9a-z]+?)"
        b"\\.st"
        b"(?P<partial>(\\.p))?"
        b"(\\.|$)"
    )

    new_sig_re = re.compile(
        b"^" + config.file_prefix + config.file_prefix_signature + b"duplicity-new-signatures"
        b"\\.(?P<start_time>.*?)"
        b"\\.to"
        b"\\.(?P<end_time>.*?)"
        b"\\.sigtar"
        b"(?P<partial>(\\.part))?"
        b"(\\.|$)"
    )

    new_sig_re_short = re.compile(
        b"^" + config.file_prefix + config.file_prefix_signature + b"dns"
        b"\\.(?P<start_time>[0-9a-z]+?)"
        b"\\.(?P<end_time>[0-9a-z]+?)"
        b"\\.st"
        b"(?P<partial>(\\.p))?"
        b"(\\.|$)"
    )
    stat_re = re.compile(
        b"^" + config.file_prefix + config.file_prefix_jsonstat + b"duplicity-(?P<type>full|inc)"
        b"\\.(?P<time>.*?)"
        b"(?:\\.to\\.(?P<end_time>.+?))?"
        b"\\.jsonstat"
        b"(?P<partial>(\\.part))?"
        b"(\\.|$)"
    )

    stat_re_short = re.compile(
        b"^" + config.file_prefix + config.file_prefix_jsonstat + b"(?P<type>dfst|dist)"
        b"\\.(?P<time>.*?)"
        b"(?:\\.to\\.(?P<end_time>.+?))?"
        b"\\.jst"
        b"(?P<partial>(\\.p))?"
        b"(\\.|$)"
    )


def to_base36(n):
    """
    Return string representation of n in base 36 (use 0-9 and a-z)
    """
    div, mod = divmod(n, 36)
    if mod <= 9:
        last_digit = str(mod)
    else:
        last_digit = chr(ord("a") + mod - 10)
    last_digit = last_digit.encode()
    if n == mod:
        return last_digit
    else:
        return to_base36(div) + last_digit


def from_base36(s):
    """
    Convert string s in base 36 to long int
    """
    total = 0
    for i in range(len(s)):
        total *= 36
        if isinstance(s, bytes):
            digit_ord = s[i]
        else:
            digit_ord = ord(s[i])
        if ord("0") <= digit_ord <= ord("9"):
            total += digit_ord - ord("0")
        elif ord("a") <= digit_ord <= ord("z"):
            total += digit_ord - ord("a") + 10
        else:
            assert 0, f"Digit {s[i]} in {s} not in proper range"
    return total


def get_suffix(encrypted, gzipped):
    """
    Return appropriate suffix depending on status of encryption or compression or neither.
    """
    if encrypted:
        gzipped = False
    if encrypted:
        suffix = b".gpg"
    elif gzipped:
        suffix = b".gz"
    else:
        suffix = b""
    return suffix


def get(
    type,
    volume_number=None,
    manifest=False,  # pylint: disable=redefined-builtin
    encrypted=False,
    gzipped=False,
    partial=False,
):
    """
    Return duplicity filename of specified type

    type can be "full", "inc", "full-sig", "new-sig", "full-stat", "inc-stat". volume_number
    can be given with the full and inc types.  If manifest is true the
    filename is of a full or inc manifest file.
    """
    assert dup_time.curtimestr
    if encrypted:
        gzipped = False
    suffix = get_suffix(encrypted, gzipped)
    part_string = b".part" if partial else b""
    if type == "full-sig" or type == "new-sig":
        assert not volume_number and not manifest
        assert not (volume_number and part_string)
        if type == "full-sig":
            return (
                config.file_prefix
                + config.file_prefix_signature
                + b"duplicity-full-signatures.%s.sigtar%s%s" % (dup_time.curtimestr.encode(), part_string, suffix)
            )
        elif type == "new-sig":
            return (
                config.file_prefix
                + config.file_prefix_signature
                + b"duplicity-new-signatures.%s.to.%s.sigtar%s%s"
                % (
                    dup_time.prevtimestr.encode(),
                    dup_time.curtimestr.encode(),
                    part_string,
                    suffix,
                )
            )
    elif type == "full-stat" or type == "inc-stat":
        assert not volume_number and not manifest
        assert not (volume_number and part_string)
        type_suffix = b"jsonstat"
        if type == "full-stat":
            main_name = b"duplicity-full"
            timestamp = b"%s" % (dup_time.curtimestr.encode())
        elif type == "inc-stat":
            main_name = b"duplicity-inc"
            start = dup_time.prevtimestr.encode()
            end = dup_time.curtimestr.encode()
            timestamp = b"%s.to.%s" % (start, end)
        else:
            raise ValueError("Not a know type {type}.")
        return (
            config.file_prefix
            + config.file_prefix_jsonstat
            + b"%s.%s.%s%s%s" % (main_name, timestamp, type_suffix, part_string, suffix)
        )
    else:
        assert volume_number or manifest
        assert not (volume_number and manifest)

        prefix = config.file_prefix

        if volume_number:
            vol_string = b"vol%d.difftar" % volume_number
            prefix += config.file_prefix_archive
        else:
            vol_string = b"manifest"
            prefix += config.file_prefix_manifest

        if type == "full":
            return b"%sduplicity-full.%s.%s%s%s" % (
                prefix,
                dup_time.curtimestr.encode(),
                vol_string,
                part_string,
                suffix,
            )
        elif type == "inc":
            return b"%sduplicity-inc.%s.to.%s.%s%s%s" % (
                prefix,
                dup_time.prevtimestr.encode(),
                dup_time.curtimestr.encode(),
                vol_string,
                part_string,
                suffix,
            )
        else:
            assert 0


def parse(filename):
    """
    Parse duplicity filename, return None or ParseResults object
    """

    def str2time(timestr, short):
        """
        Return time in seconds if string can be converted, None otherwise
        """
        if isinstance(timestr, bytes):
            timestr = timestr.decode()

        if short:
            t = from_base36(timestr)
        else:
            try:
                t = dup_time.genstrtotime(timestr.upper())
            except dup_time.TimeException:
                return None
        return t

    def get_vol_num(s, short):
        """
        Return volume number from volume number string
        """
        if short:
            return from_base36(s)
        else:
            return int(s)

    def check_full():
        """
        Return ParseResults if file is from full backup, None otherwise
        """
        prepare_regex()
        short = True
        m1 = full_vol_re_short.search(filename)
        m2 = full_manifest_re_short.search(filename)
        if not m1 and not m2:
            short = False
            m1 = full_vol_re.search(filename)
            m2 = full_manifest_re.search(filename)
        if m1 or m2:
            t = str2time((m1 or m2).group("time"), short)
            if t:
                if m1:
                    return ParseResults(
                        "full",
                        time=t,
                        volume_number=get_vol_num(m1.group("num"), short),
                    )
                else:
                    return ParseResults(
                        "full",
                        time=t,
                        manifest=True,
                        partial=(m2.group("partial") is not None),
                    )
        return None

    def check_inc():
        """
        Return ParseResults if file is from inc backup, None otherwise
        """
        prepare_regex()
        short = True
        m1 = inc_vol_re_short.search(filename)
        m2 = inc_manifest_re_short.search(filename)
        if not m1 and not m2:
            short = False
            m1 = inc_vol_re.search(filename)
            m2 = inc_manifest_re.search(filename)
        if m1 or m2:
            t1 = str2time((m1 or m2).group("start_time"), short)
            t2 = str2time((m1 or m2).group("end_time"), short)
            if t1 and t2:
                if m1:
                    return ParseResults(
                        "inc",
                        start_time=t1,
                        end_time=t2,
                        volume_number=get_vol_num(m1.group("num"), short),
                    )
                else:
                    return ParseResults(
                        "inc",
                        start_time=t1,
                        end_time=t2,
                        manifest=1,
                        partial=(m2.group("partial") is not None),
                    )
        return None

    def check_sig():
        """
        Return ParseResults if file is a signature, None otherwise
        """
        prepare_regex()
        short = True
        m = full_sig_re_short.search(filename)
        if not m:
            short = False
            m = full_sig_re.search(filename)
        if m:
            t = str2time(m.group("time"), short)
            if t:
                return ParseResults("full-sig", time=t, partial=(m.group("partial") is not None))
            else:
                return None

        short = True
        m = new_sig_re_short.search(filename)
        if not m:
            short = False
            m = new_sig_re.search(filename)
        if m:
            t1 = str2time(m.group("start_time"), short)
            t2 = str2time(m.group("end_time"), short)
            if t1 and t2:
                return ParseResults(
                    "new-sig",
                    start_time=t1,
                    end_time=t2,
                    partial=(m.group("partial") is not None),
                )
        return None

    def check_stat():
        """
        Return ParseResults if file is a signature, None otherwise
        """
        prepare_regex()
        short = True
        type = None
        time = None
        start_time = None
        end_time = None
        m = stat_re_short.search(filename)
        if not m:
            short = False
            m = stat_re.search(filename)
        if m:
            if m.group("type") in (b"full", b"dfst"):
                type = "full-stat"
                time = str2time(m.group("time"), short)
            elif m.group("type") in (b"inc", b"dist"):
                type = "inc-stat"
                start_time = str2time(m.group("time"), short)
                end_time = str2time(m.group("end_time"), short)
            else:
                raise DuplicityError(f'Statistic filename "{filename}" not valid')
            return ParseResults(
                type,
                time=time,
                start_time=start_time,
                end_time=end_time,
                partial=(m.group("partial") is not None),
            )

    def set_encryption_or_compression(pr):
        """
        Set encryption and compression flags in ParseResults pr
        """
        pr.compressed = filename.endswith(b".z") or filename.endswith(b".gz")
        pr.encrypted = filename.endswith(b".g") or filename.endswith(b".gpg")

    for check in (check_full, check_inc, check_sig, check_stat):
        pr = check()
        if pr:
            set_encryption_or_compression(pr)
            return pr
    return None


class ParseResults:
    """
    Hold information taken from a duplicity filename
    """

    def __init__(
        self,
        type,
        manifest=None,
        volume_number=None,  # pylint: disable=redefined-builtin
        time=None,
        start_time=None,
        end_time=None,
        encrypted=None,
        compressed=None,
        partial=False,
    ):
        assert type in ["full-sig", "new-sig", "inc", "full", "full-stat", "inc-stat"]

        self.type = type
        if type in ["inc", "full"]:
            assert manifest or volume_number
        if type in ["inc", "new-sig", "inc-stat"]:
            assert start_time and end_time
        else:
            assert time

        self.manifest = manifest
        self.volume_number = volume_number
        self.time = time
        self.start_time, self.end_time = start_time, end_time

        self.compressed = compressed  # true if gzip compressed
        self.encrypted = encrypted  # true if gpg encrypted

        self.partial = partial

    def __eq__(self, other):
        return (
            self.type == other.type
            and self.manifest == other.manifest
            and self.time == other.time
            and self.start_time == other.start_time
            and self.end_time == other.end_time
            and self.partial == other.partial
        )
