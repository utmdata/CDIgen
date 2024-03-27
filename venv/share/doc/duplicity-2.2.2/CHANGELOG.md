# Changelog


## rel.2.2.2 (2024-02-03)

### Changes

* Ask google\_auth\_oauthlib not to open browser during authentication
flow. [Christopher Haglund]

* Run po/update-pot. [Kenneth Loafman]

* Update `python\_requires` to allow py3.12. [Kenneth Loafman]

### Fix

* Clean up debian/rules. [Kenneth Loafman]

* Add duplicity console script. [Kenneth Loafman]

    - Copied from pip install
    - LP does not generate it


## rel.2.2.0 (2024-01-27)

### Changes

* Use pytest not tox on GitLab CI. [Kenneth Loafman]

    - saves build time

* Run po/update-pot. [Kenneth Loafman]

* Remove support for old mock. [Alexandre Detiste]

    Project says "REQUIREMENTS: Python 3.8 to 3.12"

* Allow pipelines to run if not merge request. [Kenneth Loafman]

* Version as 2.2.0. [Kenneth Loafman]

* Upgrade current build and test systems. [Kenneth Loafman]

    # Changes:
      - move bin/duplicity to duplicity/__main__.py
      - add entry point dup_run() no args
      - rename bin to man (only contents now)
      - rename duplicity/tarfile.py to duplicity/dup_tarfile.py to avoid import problems
      - duplicity now runs as a module `python3 -m duplicity` as well as a script `/usr/bin/duplicity`
      - py2->py3 oddities changed, `"".__class__` and `b"".__class__` changed to `str` and `bytes`
      - tox v4 now runs correctly as `tox run -e code`
      - moved [pycodestyle] from tox.ini to setup.cfg
      - moved .pylintrc from to setup.cfg
      - sources released fully versioned
        - duplicity/\_\_init\_\_.py
        - man/duplicity.1
        - pyproject.toml
        - setup.py
        - snap/snapcraft.yaml

    Closes #774,#793

### Fix

* Remove test\_GPGWriteFile. [Kenneth Loafman]

    - Fails on GitLab
    - Runs on Linux and macOS just fine

* Invalid option error using `--[gpg|par2|rsync|ssh]-options '...' [Kenneth Loafman]

    Fixes #795.


## rel.2.1.5 (2023-12-28)

### New

* \_testbackend to simulate issues. [Thomas Laubrock]

    \_testbackend is a copy of the localbackend and allows to trigger certain miss behaviours. Failure type and condition can be set via env vars. Some test cases are added to test_badupload.py.

    This is pre-work for !153 but want to decouple it for better handling.

### Changes

* Fix debian/rules for versioned. [Kenneth Loafman]

* Version as 2.1.5. [Kenneth Loafman]

* Run po/update-pot. [Kenneth Loafman]

* Remove "backup" and "replicate" dead code. [Kenneth Loafman]

* Fix imports in \_testbackend.py. [Kenneth Loafman]

* Move addhandler() to \_\_init\_\_. [Kenneth Loafman]

    - Will not produce temp log unless in use
    - Reorg imports

* Deprecate PyDrive backend. Replaced with GDrive backend. [Kenneth Loafman]

* Setuptools\_scm not needed at runtime. [Gwyn Ciesla]

* Fix swift uploads to default to 5GB segment size. [Garth Williamson]

* Add venv* to .gitignore. [Kenneth Loafman]

* Some formatting fixes. [Kenneth Loafman]

* Fix check of versions in setup.py. [Kenneth Loafman]

* Limit range of versions in setup.py. [Kenneth Loafman]

    - We already had lower limit of 3.8, make 3.11 upper limit.

* Update version for LP. [Kenneth Loafman]

### Fix

* Swap implied and removed action checks. [Kenneth Loafman]

* Error on dry-run with verify. [Kenneth Loafman]

* Fix imports in boxbackend.py. [Kenneth Loafman]

* Multibackend not working with remove-all-but-n-full in stripe mode. [Kenneth Loafman]

    remove short-circuit logic that fails
    * add test in testing/regression

    Fixes #781

* Fix collection-status with file-changed argument. [JulianWgs]


## rel.2.1.4 (2023-10-20)

### Changes

* Run po/update-pot. [Kenneth Loafman]

* Add test\_black to test\_code.py.  Convert to black format. [Kenneth Loafman]

* --asynchronous-upload is not parsed correctly. [Kenneth Loafman]

* Update version for LP. [Kenneth Loafman]

### Fix

* Print command line error on empty commandline. [Kenneth Loafman]

* Print help on empty commandline. [Kenneth Loafman]

* --full-if-older-than being ignored? [Kenneth Loafman]


## rel.2.1.3 (2023-10-08)

### Changes

* Run po/update-pot. [Kenneth Loafman]

* Fix typo in cli\_data.py. [Rena Kunisaki]

### Fix

* Intermixed argument lists cause problems. [Kenneth Loafman]

* Exclude-other-filesystems seems to be ignored since duplicity 2. [Kenneth Loafman]

* Change backup to inc after CLI processing. [Kenneth Loafman]

* Fix test\_skip\_if\_no\_change to use \_runtest\_dir not /tmp. [Kenneth Loafman]

* Fix typos in cli\_data.py and release-prep. [Kenneth Loafman]

* --version showing 'duplicity\_logging' not 'duplicity' [Kenneth Loafman]

* --full-if-older-than being ignored? [Kenneth Loafman]


## rel.2.1.2 (2023-09-27)

### Changes

* Fix archive name in release-prep. [Kenneth Loafman]

* Ignore commit error in release-prep. [Kenneth Loafman]

* Run po/update-pot. [Kenneth Loafman]

* Don't truncate CHANGELOG.md. [Kenneth Loafman]

* Change message in check\_target\_url. [Kenneth Loafman]

### Fix

* More argparse refinements, especially wrt. removed/changed options ... [ede]

    - add a generic help footer
    - remove all options from parent parser, only add parent options
      needed for proper `duplicity --help` without command
    - re-add to removed options so the appropriate error is thrown
      - --s3-european-buckets,
      - --s3-use-new-style,
      - --s3-use-server-side-encryption
    - refactor deprecated to removed option, because they were
    - dynamically list removed options as opposed to former static string
    - fix handling of removed_backup_options (--time-separator).  Fixes #763
    - fix full-if-older-than being ignored.  Fixes #764

* Fix mega v1 backend.  Fixes #762. [Kenneth Loafman]

* Refix format of paramiko host authenticity message. [ede]

    do not enforce paramiko 3.2
    show SHA256 fingerprint only w/ paramiko 3.2+
    Fixes #760

* Fix format of authenticity message. [Kenneth Loafman]

    Also add requirements for paramiko>=3.2

    Fixes #760

* Add -f to lftp mkdir to ignore existing dirs. [Kenneth Loafman]

    Fixes #721

* Whoops, paramiko uses MD5 not SHA256. [Kenneth Loafman]

* Adjust paramiko host key format to hex. [Kenneth Loafman]

    Fixes #760.

* Adjust debian/control and requirements.txt. [Kenneth Loafman]

    - Change boto to boto3.
    - Remove python3-future.
    - Fixes #761.

* Restore s3\_use\_server\_side\_encryption. [Kenneth Loafman]

* Issue #759 "--asynchronous-upload is not parsed correctly" [ed]

    https://gitlab.com/duplicity/duplicity/-/issues/759

* Implement \_retry\_cleanup for ssh\_paramiko. [bonswouar]

* Fix python version requirement.  Fixes #754. [Kenneth Loafman]

* Adjust azure import handling.  Fixes #756. [Kenneth Loafman]


## rel.2.1.1 (2023-09-02)

### Changes

* Run po/update-pot. [Kenneth Loafman]

* Make action command missing error message more helpful. [ede]

* Allow duplicity --help and -h.  Fixes #749. [Kenneth Loafman]

* Do not wrap body of git commit. [Kenneth Loafman]

* Change backup abbrev 'b' to 'bu'. [Kenneth Loafman]

* Skip some tests on Launchpad. [Kenneth Loafman]

### Fix

* Pexpect backend fix. [DiegoRenner]


## rel.2.1.0 (2023-08-26)

### New

* Skip inc backup if nothing has changed. [Thomas Laubrock]

* Log a warning when using dangerous --asynchronous-upload option. [ed]

* Keep stats in files.  Fixes #722. [Thomas Laubrock]

### Changes

* Run po/update-pot. [Kenneth Loafman]

### Fix

* Implement implied commands via pre parsing. Fixes #733. [Kenneth Loafman]

    - detect 'backup' or 'restore' by parsing the arguments
    - new action command 'backup'
    - document 'backup' in man page
    - document new action command short aliases in man page
    - streamline url parameter checking
    - add more tests for implied commands

* Replace util.fsdecode with os.fsdecode.  Fixes #748. [Kenneth Loafman]

* Try import of setuptools\_scm.  Fixes #746. [Kenneth Loafman]


## rel.2.0.2 (2023-08-15)

### Fix

* Fixes to tools/release-prep. [Kenneth Loafman]

* Adjust to new azure module structure.  Fixes #731. [Kenneth Loafman]

* Handle --encrypt-sign-key.  Fixes #736. [Kenneth Loafman]

* Fix PEP8 error. [Kenneth Loafman]

* Fix *-options commands.  Fixes #732. [Kenneth Loafman]

* Enable selection options for verify.  Fixes #734. [vin01]


## rel.2.0.1 (2023-08-08)

### Fix

* Adjust regex for 2.0.0x. [Kenneth Loafman]

* Restore pre-parser. Fixes #727. [Kenneth Loafman]

    Revert "chg:usr: Remove implied command support for now."

    This reverts commit afbeb4082a87e2073b5ccdcd624cf5e6f4465608.

* Add missing import to cli\_util.py. Fixes #730. [Kenneth Loafman]

* Add missing import to b2backend.py.  Fixes #729. [Kenneth Loafman]

* Adjust version to build under LP. [Kenneth Loafman]

* Adjust to build under LP Mantic. [Kenneth Loafman]

    fix:pkg: Adjust to build under LP Mantic.

* Fix PEP8 issue. [Kenneth Loafman]


## rel.2.0.0x (2023-08-07)

### Changes

* Remove boto related doc. some reformatting. [ede]

* Add missing user options to manpage. [Kenneth Loafman]

* Improve --verbosity help. [Kenneth Loafman]

* Remove implied command support for now. [Kenneth Loafman]

* Remove --s3-european-buckets used by boto. [Kenneth Loafman]

* Fix short filenames use in new s3 files. [Kenneth Loafman]

### Fix

* Cannot run CLI tests on Launchpad. [Kenneth Loafman]

* S3 backend issues. Fixes #31. [Kenneth Loafman]

* Fix Exception Type for verbosity level. [Thomas Laubrock]

* Remove tests for py27 and py35. [Kenneth Loafman]


## rel.2.0.0rc2 (2023-07-24)

### Changes

* Fix format strings in idrivedbackend.py. [Kenneth Loafman]

* Add additional CLI checks. [Kenneth Loafman]

* Fix format strings in idrivedbackend.py. [Kenneth Loafman]

* Fix format string in statistics.py. [Kenneth Loafman]

* Remove kerberos from snap builds. [Kenneth Loafman]

    kerberos will not build in snapcraft.

* Changes to allow building snaps. [Kenneth Loafman]

    Found another bug in snapcraft, see:
    https://bugs.launchpad.net/snapcraft/+bug/2028303


## rel.2.0.0rc1 (2023-07-17)

### Changes

* Update CHANGELOG.md. [Kenneth Loafman]

* Fix implied command handling. [Kenneth Loafman]

* Create regression test dir from old scripts. [Kenneth Loafman]


## rel.2.0.0rc0 (2023-07-10)

### Changes

* Update CHANGELOG.md. [Kenneth Loafman]

### Fix

* Finish conversions to f-strings. [Kenneth Loafman]

    See https://github.com/ikamensh/flynt/issues/185

* Convert to f-strings via 'flynt -tc -tj'. [Kenneth Loafman]

* With py2 gone remove unicode string adornments. [Kenneth Loafman]

* Fix implied command when target is empty. [Kenneth Loafman]


## rel.2.0.0b2 (2023-07-02)

### Changes

* Update CHANGELOG.md. [Kenneth Loafman]

* Fix syntax error in .gitlab-ci.yml. [Kenneth Loafman]

* Fix website to only run with WEBSITE\_TRIGGER\_TOKEN. [Kenneth Loafman]

* Fix PEP8 issue.  Update CHANGELOG.md. [Kenneth Loafman]

* Resolve some minor merge issues. [Kenneth Loafman]

* Whoops, used f-string to fix #716. Fixed. [Kenneth Loafman]

* Fix #716.  Print filename on read error. [Kenneth Loafman]

* Fix #709.  Add docs on passphrase encryption used. [Kenneth Loafman]

* Fixes for handling snaps again. [Kenneth Loafman]

    Use requirements.txt instead of internal list.

* Fix #707 for test\_get\_stats\_string. [Kenneth Loafman]

    Move UTC set/unset to testing.__init__.

* Fix #707 for test\_get\_stats\_string. [Kenneth Loafman]

    Base time on UTC rather than where the test is run.

* Fix #707 for test\_get\_stats\_string. [Kenneth Loafman]

    Base time on UTC rather than where the test is run.

* Fix #707 for rclone backend testing. [Kenneth Loafman]

    Create 'duptest' config if needed, then remove after
    tests are complete.

    Add some more pytest options to tox.ini.

* Comment out test\_path:test\_compare, flaky. [Kenneth Loafman]

    Fixes #707 - 1.2.3 test failure

* Force cryptography<3.4 for py2 support. [Kenneth Loafman]

* Test if requirements.txt changes. [Kenneth Loafman]

* Revert back to tox < 4.0. [Kenneth Loafman]

### Fix

* Fix #710. Missing Content-Type header on webdav. [Kenneth Loafman]

* S3 filename encoding. [Thomas Laubrock]

* Fix #712 "if cache lost. `*.sigtar.gpg` files not accessible" [Thomas Laubrock]

    solution, do not add signature files to glacier

* Handle read-only remote parent folder better in gio backend. [Michael Terry]


## rel.2.0.0b1 (2023-06-30)

### Changes

* Update CHANGELOG.md. [Kenneth Loafman]

* Some basic PEP8 and code cleanup. [Kenneth Loafman]

* Set socket default timeout in CLI. [Kenneth Loafman]

* Fixes for deprecated/changed options. [Kenneth Loafman]


## rel.2.0.0b0 (2023-06-24)

### Changes

* Misc changes for compatibility. [Kenneth Loafman]

* Fix #24.  Allow users to tune copy block size. [Kenneth Loafman]

    - Added --copy-blocksize, default 128k to options.
    - Added tests for same and improved other testss.

* Fix .gitlab-ci.yml to skip website step if no token. [Kenneth Loafman]


## rel.2.0.0a2 (2023-06-14)

### Changes

* Remove pathvalidate from use.  Fixes #27. [Kenneth Loafman]


## rel.2.0.0a1 (2023-06-14)

### Changes

* More CLI improvements. [Kenneth Loafman]

    - Improve error message for implied commands.
    - Code and testing clean up.
    - Remove deprecated option handling.

* Add implied backup/restore back. [Kenneth Loafman]

* CLI improvements and cleanup. [Kenneth Loafman]

    - Remove 'backup' command.
    - Preparse options for config.

* Minor cleanup, rm dead code. [Kenneth Loafman]

* RcloneBackendTest now creates its own config. [Kenneth Loafman]

* "--ignore-errors" gets proper handling in CLI. [Kenneth Loafman]

### Fix

* Fix #22, “--no-compression” doesn't have effect. [Kenneth Loafman]

* Fix .gitlab-ci.yml file syntax error. [Kenneth Loafman]


## rel.2.0.0a0 (2023-06-01)

### New

* Add --webdav-headers to webdavbackend.  Fixes #94. [Kenneth Loafman]

* Add tests for Python 3.10. [Kenneth Loafman]

* Make sdist only provide necessary items for build. [Kenneth Loafman]

* Add changelog to deploy stage to build CHANGELOG.md. [Kenneth Loafman]

    - make job changelog to run tools/makechangelog in CI/CD.
    - make jobs build_pip and build_snap require changelog.



* Document rclone option setting via env vars. [edeso]

* Enable CI snapcraft amd64 builds with docker. [edeso]

    .gitlab-ci.yml
    job build_snap based on a working docker image
    commented 'only:' limitiation, it's manual anyway
    used split out tools/installsnap step
    upload artifact (duplicity-*.snap) regardless
    - so it can be downloaded and debugged
    - keep it for 30 deays by default

    snap/snapcraft.yaml
    - fixup PYTHONPATH

    new 'tools/installsnap' that detects and works with docker

    tools/testsnap
    remove installation step
    remove double test entries
    change testing to use gpg and compression

* Document rclone option setting via env vars. [edeso]

* Fix other archs, expose rdiffdir. [edeso]

    fix remote build of armhf, arm64, ppc64el
    arm64 was tested on Debian 11 arm64
    rdiffdir now avail as /snap/bin/duplicity.rdiffdir
    remove obsolete folder /usr/lib/python3.9/ in snap

* Demote boto backend to legacy ... [ede]

    usable via boto+s3:// or boto+gs:// now only
    removed s3+http:// scheme
    added --s3-endpoint-url option as replacement
    added --s3-use-deep-archive option
    changes are document in man page commit of the same patch set

* Promote boto3 backend to default s3:// backend ... [ede]

    add --s3-unencrypted-connection support

* Man page, major sorting, reformatting, S3/GCS documentation update. [ede]

    some updates, added s3 options, clarifications
    updated Notes on S3 and Google Cloud Storage usage
    sort Options, Url Formats, Notes on alphabetically
    consistently use "NOTE:"
    indent properly all over

* Minimize testing/manual/issue98.sh for issue #98. [Kenneth Loafman]

* Add testing/manual/issue98.sh to test issue #98. [Kenneth Loafman]

* Add Getting Versioned Source to README-REPO.md. [Kenneth Loafman]

    [no ci]

* Test case for issue 103 multi-backend prefix affinity. [Kenneth Loafman]

* Add --use-glacier-ir option for instant retrieval.  Fixes #102. [Kenneth Loafman]

* Add --par2-volumes entry to man page. [Kenneth Loafman]

* Add manual test for issue 100. [Kenneth Loafman]

* Add option --show-changes-in-set <index> to collection-status. [Kenneth Loafman]

    Patches provided by Peter Canning (@pcanning).  Closes #99.

* Add release-prep.sh for release preparation. [Kenneth Loafman]

* Add py310 to envlist to test against python 3.10. [Kenneth Loafman]

* Add update of API docs to deploy step. [Kenneth Loafman]

* Better looping.  Increase to 100 loops. [Kenneth Loafman]

* Repeating test for LP bug 487720. [Kenneth Loafman]

    Restore fails with "Invalid data - SHA1 hash mismatch"

### Changes

* Fix initial version. [Kenneth Loafman]

* Give up. Let setup mangle as it will. [Kenneth Loafman]

* Use semver tags, let setup mangle. [Kenneth Loafman]

* Make PEP 440 compatible, not semver yet. [Kenneth Loafman]

* Changes to allow alpha, beta, rc prerelease. [Kenneth Loafman]

* Update gitlab-ci.yml. [Kenneth Loafman]

* Update gitlab-ci.yml. [Kenneth Loafman]

* Remove 'rdiffdir'.  Not used. [Kenneth Loafman]

* Add 'make sdist' to Makefile. [Kenneth Loafman]

* Update .gitignore. [Kenneth Loafman]

* Setuptools\_scm.get\_version now uses 'fallback\_version'. [Kenneth Loafman]

* Remove old s3\_boto\_backend.py. [Kenneth Loafman]

    Deprecated options:
    --s3-multipart-max-timeout
    --s3-use-multiprocessing
    --s3-use-server-side-encryption
    --s3-use-server-side-kms-encryption

    Retired error codes:
    boto_old_style = 24
    boto_lib_too_old = 25
    boto_calling_format = 26

* Remove spaces in version specs. [Kenneth Loafman]

* Cleanup py2 cruft and more. [Kenneth Loafman]

* Cleanup py2 cruft and more. [Kenneth Loafman]

* Uncomment log.test\_command\_line\_error. [Kenneth Loafman]

* Raise CommandLineError on deprecated/changed options. [Kenneth Loafman]

* Whoops, don't move import\_backends. [Kenneth Loafman]

* Fix code, tests, and do cleanup. [Kenneth Loafman]

* Requirements and code cleanup. [Kenneth Loafman]

* Whoops, fix code style. [Kenneth Loafman]

* Add error/ignored msg for deprecated options. [Kenneth Loafman]

* Some cli cleanup for subcommands. [Kenneth Loafman]

* Normalize error handling in cli\_util.py. [Kenneth Loafman]

* Some small command line fixes. [Michael Terry]

    - Fix --verbosity
    - Fix --log-fd
    - Fix list-current-files

* Clean out the last py2 cruft, I hope. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Some py2 to py3 cleanup. [Kenneth Loafman]

    Ran '2to3 -f filter -f map -f xrange -f zip -f idioms'.  It put some
    list calls around some of the stuff that returns iterators (redundant
    in most cases I think).  Mainly it converted code to idiomatic python.



* Update a couple of lists in conf.py. [Kenneth Loafman]

* Whoops, still need Makefile in docs. [Kenneth Loafman]

* Port ReadTheDocs changes from main branch. [Kenneth Loafman]

* Port ReadTheDocs changes from main branch. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Fix version and required python version. [Kenneth Loafman]

* Fix version and required python version. [Kenneth Loafman]

* More refactoring and cleanup after merge. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Fix version and required python version. [Kenneth Loafman]

* More refactoring and cleanup after merge. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

    chg:usr: Change optparse to argparse.  Checkpoint.

    chg:usr: Change optparse to argparse.  Checkpoint.

    chg:usr: Change optparse to argparse.  Checkpoint.

    chg:usr: Change optparse to argparse.  Checkpoint.

* Add Note on --time-separator in manpage. [Kenneth Loafman]

* Remove refs to --old/short-filenames.  Fix CI. [Kenneth Loafman]

* Remove deprecated --short-filenames code. [Kenneth Loafman]

* Remove deprecated --old-filenames code. [Kenneth Loafman]

* Remove deprecated --gio code. [Kenneth Loafman]

* Remove globbing deprecated code. [Kenneth Loafman]

* Remove stdin deprecated code. [Kenneth Loafman]

* Remove incomplete replicate command. [Kenneth Loafman]

* Remove LINGUAS.  Replace with globbing. [Kenneth Loafman]

* More cleanup from inspections. [Kenneth Loafman]

* Util.fsdecode ==> os.fsdecode. [Kenneth Loafman]

* Remove par2+ from target schema.  Does not matter. [Kenneth Loafman]

* Add limits to chardet and urlllib to keep requests quiet. [Kenneth Loafman]

* Lower test to ulimit 2048 and reverse filename order. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Fix version and required python version. [Kenneth Loafman]

* Fix version and required python version. [Kenneth Loafman]

* More refactoring and cleanup after merge. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

* Change optparse to argparse. Checkpoint. [Kenneth Loafman]

* Fix version and required python version. [Kenneth Loafman]

* More refactoring and cleanup after merge. [Kenneth Loafman]

* Change optparse to argparse.  Checkpoint. [Kenneth Loafman]

    chg:usr: Change optparse to argparse.  Checkpoint.

    chg:usr: Change optparse to argparse.  Checkpoint.

    chg:usr: Change optparse to argparse.  Checkpoint.

    chg:usr: Change optparse to argparse.  Checkpoint.

* Add Note on --time-separator in manpage. [Kenneth Loafman]

* Remove refs to --old/short-filenames.  Fix CI. [Kenneth Loafman]

* Remove deprecated --short-filenames code. [Kenneth Loafman]

* Remove deprecated --old-filenames code. [Kenneth Loafman]

* Remove deprecated --gio code. [Kenneth Loafman]

* Remove globbing deprecated code. [Kenneth Loafman]

* Remove stdin deprecated code. [Kenneth Loafman]

* Remove incomplete replicate command. [Kenneth Loafman]

* Remove LINGUAS.  Replace with globbing. [Kenneth Loafman]

* More cleanup from inspections. [Kenneth Loafman]

* Util.fsdecode ==> os.fsdecode. [Kenneth Loafman]

* Remove par2+ from target schema.  Does not matter. [Kenneth Loafman]

* Add limits to chardet and urlllib to keep requests quiet. [Kenneth Loafman]

* Lower test to ulimit 2048 and reverse filename order. [Kenneth Loafman]

* Update README-SNAP.md to show options. [Kenneth Loafman]

* Add instructions for building snaps. [Kenneth Loafman]

* Add missing license metadata. [ede]

    [ci_skip]

* More docker cleanup. [Kenneth Loafman]

    - Add rclone to package installs.



* Trigger website rebuild on pushes/tags. [ede]

* More docker cleanup. [Kenneth Loafman]

    - remove copy of setup.py, not used
    - add testit.py for basic testing

* More docker cleanup. [Kenneth Loafman]

    - use 'docker compose' not docker-compose
    - remove more unused items

* Optimize build of duplicity\_test image. [Kenneth Loafman]

    - use buildkit to speed up build,
    - split huge layers into smaller ones
    - changes in testing dir trigger pipeline

* Fold requirements.dev into requirements.txt.  Del requirements.dev. [Kenneth Loafman]

* Fold requirements.dev into requirements.txt.  Del requirements.dev. [Kenneth Loafman]

* Fold requirements.dev into requirements.txt.  Del requirements.dev. [Kenneth Loafman]

* Extend code\_test to testing directory. [Kenneth Loafman]

    - Fix or mark issues found.
    - Will not run under py27.

* Fix .md formatting. [Kenneth Loafman]

* Mark slow tests > 10sec.  Use -m "not slow". [Kenneth Loafman]

* Ref requirements.dev in install. [Kenneth Loafman]

* Ref requirements files instead of listing in duplicate. [Kenneth Loafman]

* Action and Audience must be lowercased. [Kenneth Loafman]

* Nuke skip tests and skip ci in CHANGELOG.md. [Kenneth Loafman]

* New os\_options for SWIFT backend. [Florian Perrot]

* Clarify when --s3-endpoint-url,-region-name are needed. [ede]

* Change from master to main branch naming. [Kenneth Loafman]

* Better defaults for S3 mac procs and chunk sizing. [Josh Goebel]

* --s3\_multipart\_max\_procs applies to BOTO3 backend also. [Josh Goebel]

* Migrate to unittest.mock. [Gwyn Ciesla]

* Fix modeline, change utf8 to utf-8 to make emacs happy. [Kenneth Loafman]

* Replace pexpect.run with subprocess\_popen in par2backend. [Kenneth Loafman]

* Fix PEP8 issue. [Kenneth Loafman]

* Add py310 to list of versions supported. [Kenneth Loafman]

* Fix script pushsnap to handle errors. [Kenneth Loafman]

* Add returncode to BackendException for rclonebackend. [Kenneth Loafman]

* Snap use core20 coreutils if none in PATH env var. [ede]

    add "/snap/core20/current/usr/bin" to PATH

* Need to install python3 for pages. [Kenneth Loafman]

* Don't push to savannah any more. [Kenneth Loafman]

* Fix version for builds. [Kenneth Loafman]

* Use cicd image hosted on GitLab. [Kenneth Loafman]

* Create singular container for testing. [Kenneth Loafman]

* Fix PEP8 issue. [Kenneth Loafman]

* Remove build on merge request and unused variables. [Kenneth Loafman]

* Cosmetic changes only. [Kenneth Loafman]

* Make pages manual deploy. [Kenneth Loafman]

* Changelog removed, remove needs. [Kenneth Loafman]

* Only build pip and snap, don't push. [Kenneth Loafman]

* Fix misspelled stage name. [Kenneth Loafman]

* Fix deps format. [Kenneth Loafman]

* Fix deps format. [Kenneth Loafman]

* Add requirements.dev to tox.ini. [Kenneth Loafman]

* Include pydevd in requirements.txt. [Kenneth Loafman]

* Go back to ubuntudesktop/gnome-3-38-2004. [Kenneth Loafman]

* Add tools dir to changes list in deploy-template. [Kenneth Loafman]

* Try snap with utuntu:20.04. Fix artifacts loc. [Kenneth Loafman]

* Some debugging statements. [Kenneth Loafman]

* Some debugging statements. [Kenneth Loafman]

* Set up the SSH key and the known\_hosts file. [Kenneth Loafman]

* Set up config for git. [Kenneth Loafman]

* Clone repo so setuptools-scm works properly. [Kenneth Loafman]

* Move setuptools* to .dev.  Nuke report.xml artifact. [Kenneth Loafman]

* Add some more requirements. [Kenneth Loafman]

* Install git and intltool for changelog. [Kenneth Loafman]

* Add changes: to deploy-template. [Kenneth Loafman]

* Fix syntax. [Kenneth Loafman]

* Minimize CI/CD overhead. [Kenneth Loafman]

* Split requirements into .txt and .dev. [Kenneth Loafman]

    .txt - normal user
    .dev - developer

* Standardize startup sequence. [Kenneth Loafman]

* Remove deploy jobs needing secret keys. [Kenneth Loafman]

* Do not supply user/password to twine, just access token. [Kenneth Loafman]

* Do not supply user/password to twine, just access token. [Kenneth Loafman]

* Add default never to .test-template. [Kenneth Loafman]

* Change PYPI\_ACCESS\_TOKEN back to variable and just echo it. [Kenneth Loafman]

* Just cp PYPI\_ACCESS\_TOKEN to \~/.pypirc. [Kenneth Loafman]

* Fix usage of PYPI\_ACCESS\_TOKEN. [Kenneth Loafman]

* Set to run deploy only after a push event. [Kenneth Loafman]

* Whoops, can't run deploy on source branch to merge. [Kenneth Loafman]

* Use rules in templates.  Always run on merge requests. [Kenneth Loafman]

* Always run pipeline on merge request event. [Kenneth Loafman]

* Make sure we run all during merge requests. [Kenneth Loafman]

* Add deploy-template to only run when source changes. [Kenneth Loafman]

* Fix to only run tests if source code changes. [Kenneth Loafman]

* If no changes, exit 0 to allow pip and snap builds. [Kenneth Loafman]

* Set up pypi access token for uploading. [Kenneth Loafman]

* Keep pip build artifacts for 30 days as pipeline artifacts. [ede]

* Skip tests, not ci, so we can build snaps, pips, pages, etc. [Kenneth Loafman]

* Allow non-Docker environs to sign snaps. [Kenneth Loafman]

* Allow GitLab CI to upload snaps to the store. [Kenneth Loafman]

    still have not figured out how to store sign key on GitLab



* Update or add copyright and some cosmetic changes. [Kenneth Loafman]

* Remove install of snapcraft, snap, snapd. [Kenneth Loafman]

* Add grpcio-tools to top to get latest version. [Kenneth Loafman]

    This leaves two unresolvable problems (upper version conflicts):
    ERROR: mediafire 0.6.0 has requirement requests<=2.11.1,>=2.4.1, but
    you'll have requests 2.27.1 which is incompatible.
    ERROR: python-novaclient 2.27.0 has requirement pbr<2.0,>=1.6, but
    you'll have pbr 5.8.1 which is incompatible.



* Remove conflicting build env variable.  Nuke evil tabs. [Kenneth Loafman]

* Allow duplicity-core20 to run deploy steps, for now. [Kenneth Loafman]

* Install snapcraft snap snapd. [Kenneth Loafman]

* Allow pip and snap builds from branches for now. [Kenneth Loafman]

* Add build\_snap and build\_pip back. [Kenneth Loafman]

* More tests for tools/testsnap. [Kenneth Loafman]

    add backup/verify runs to check major pathways
    add multi-lib check to avoid SnapCraft bug 1965814

* More snapcraft.yaml fixups. [Kenneth Loafman]

    break up long strings for better readability
    preload pbr and requests to avoid most version warnings
    pbr and requests are now at latest version, not ancient

* Add further checks to testing for backup and multi-lib. [Kenneth Loafman]

* Remove SNAPCRAFT\_PYTHON\_INTERPRETER per edso, no change on U20. [Kenneth Loafman]

* Try to force Python 3.8 only. [Kenneth Loafman]

* More detailed error message. [Kenneth Loafman]

* Divide makesnap into makesnap, testsnap, and pushsnap. [Kenneth Loafman]

* Revert to core18.  core20 is still unusable. [Kenneth Loafman]

* Changes to run on Focal with core20. [Kenneth Loafman]

* Use multiple -m options on commit to split comment. [Kenneth Loafman]

* Remove build-pip and build-snap.  Build locally for now. [Kenneth Loafman]

* Remove build-pip and build-snap.  Build locally for now. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Remove sudo. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Core20 usess py38, not py36. [Kenneth Loafman]

* Core20 usess py38, not py36. [Kenneth Loafman]

* Attempt core20 again. [Kenneth Loafman]

* Fix syntax. [Kenneth Loafman]

* Remove unneeded Dockerfiles.  Rename. [Kenneth Loafman]

* Try remote snap build. [Kenneth Loafman]

* Remove unneeded Dockerfiles.  Rename. [Kenneth Loafman]

* Cosmetic fixes. [Kenneth Loafman]

* Try forcing snaps to use python3.6 in 18.04. [Kenneth Loafman]

* Add check for correct platform. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Add warning for replicate command.  See issue #98. [Kenneth Loafman]

* Minor tweaks. [Kenneth Loafman]

* Add wheels to .gitignore. [Kenneth Loafman]

* Cosmetic changes. [Kenneth Loafman]

* Add collection-status at end of test. [Kenneth Loafman]

* Remove gpg socket files during clean. [Kenneth Loafman]

* Back off to default image. [Kenneth Loafman]

    [skip-tests]

* Try adding apt-get upgrade. [Kenneth Loafman]

    [skip-tests]

* Add .test-template to allow skipping qual and tests. [Kenneth Loafman]

    [skip-tests]

* Try build with apt-get update. [Kenneth Loafman]

* Try building snap on 20.04. [Kenneth Loafman]

* Add targets to manually import/export translations. [Kenneth Loafman]

* Update duplicity.pot for LP translation. [Kenneth Loafman]

* Revert "Put out first 'post' release to fix pypi issue". [Kenneth Loafman]

* Put out first 'post' release to fix pypi issue. [Kenneth Loafman]

* Rename AUTHORS to CONTRIBUTING.md. [Kenneth Loafman]

* Rename dist dir to tools to avoid collision with setuptools. [Kenneth Loafman]

* Add line wrap to changelog process, body and subject. [Kenneth Loafman]

* When buiilding for amd64 build snap locally, else remote. [Kenneth Loafman]

* Fix build of pages. [Kenneth Loafman]

* Switch over to sphinx-rtd-theme. [Kenneth Loafman]

* Fix command line warning messages. [Kenneth Loafman]

* Fix clean command to include module doc .rst files. [Kenneth Loafman]

* Nuke generated .rst files. [Kenneth Loafman]

* Nuke before\_script.  [ci skip] [Kenneth Loafman]

* Move html to public dir. [Kenneth Loafman]

* Forgot to add myst-parser.  Comment out tests for now. [Kenneth Loafman]

* Back to alabaster theme.  Port changes from sqlite branch. [Kenneth Loafman]

* Remove Dockerfiles for .10 versions. [Kenneth Loafman]

* Fix some rst errors in docstrings.  Add doctest module. [Kenneth Loafman]

* Fixes to make API docs work right. [Kenneth Loafman]

* Whoops, left out import sys. [Kenneth Loafman]

* Skip test to allow py27 and py35 to pass. [Kenneth Loafman]

* Some tweaks to run cleaner. [Kenneth Loafman]

* Fix typo in test selection. [Kenneth Loafman]

* Remove redundant call to pre\_process\_download\_batch. [Kenneth Loafman]

* Fix mismatch between pre\_process\_download[\_batch] calls. [Kenneth Loafman]

    Implement both in backend and multibackend if hasattr True.

* Build\_ext now builds inplace for development ease. [Kenneth Loafman]

* Log difftar filename where kill happened. [Kenneth Loafman]

* Remove lockfile to avoid user confusion. [Kenneth Loafman]

* Allow customization. [Kenneth Loafman]

* Fix Support DynamicLargeObjects inside swift backend. [Mathieu Le Marec - Pasquet]

    Use high levels APIS to both:

    - correctly delete multipart uploads
    - correctly handle multipart uploads

    This fixes [launchpad #557374](https://answers.launchpad.net/duplicity/+question/557374)

* Fix makechangelog to output actual problems. [Kenneth Loafman]

* Add dependency scanning. [Kenneth Loafman]

* Make sure changelog is only change to commit. [Kenneth Loafman]

* Fix indentation. [Kenneth Loafman]

* Add support for --s3-multipart-chunk-size, default 25MB. [Kenneth Loafman]

    Fixes issue #61

* Add interruptable:true as default. [Kenneth Loafman]

* Fix snapcraft commands. [Kenneth Loafman]

* Fix snaplogin file use. [Kenneth Loafman]

* Add deployment for pip and snap builds. [Kenneth Loafman]

* Add build\_pip job. [Kenneth Loafman]

* Fix PEP8 issue. [Kenneth Loafman]

* More cleanup for snap builds. [Kenneth Loafman]

* Move arch selection to dist/makesnap. [Kenneth Loafman]

* Try snap build on all architectures. [Kenneth Loafman]

* Build for i386, amd64, armhf. [Kenneth Loafman]

* Move to remote build of armfh and amd64. [Kenneth Loafman]

* Attempt remote build of armfh. [Kenneth Loafman]

* More cleanup on requirements. [Kenneth Loafman]

* Megatools no longer supports py35. [Kenneth Loafman]

* Get more stuff from pypi than repo.  Some cleanup. [Kenneth Loafman]

* Fix spaces before inline comments. [Kenneth Loafman]

* Enable access-member-before-definition in pylintrc. [Kenneth Loafman]

* Fix indentation. [Kenneth Loafman]

* Fix formatting in A NOTE ON GDRIVE BACKEND.  Minor. [Kenneth Loafman]

* Module gdata still does not work on py3. [Kenneth Loafman]

* Tweak requirements for gdrivebackend.  Cosmetic changes. [Kenneth Loafman]

* Display merge comments.  Better formatting. [Kenneth Loafman]

* Clean up readability.  Minor changes. [Kenneth Loafman]

* Cosmetic chnges. [Kenneth Loafman]

* Make testing/manual/bug1893481 into a tarball, not directory. [Kenneth Loafman]

* Add Makefile and update docs. [Kenneth Loafman]

* Remove installs common between before\_script: and script: [Kenneth Loafman]

* Remove installs common between before\_script: and script: [Kenneth Loafman]

### Fix

* Add a missing super() call in path.py. [Kenneth Loafman]

* Add a missing method to some super calls. [Michael Terry]

* Add missing ':''. [Kenneth Loafman]

* Remove requirement for kerberos. [Kenneth Loafman]

    - it's an optional package in webdavbackend.py
    - it does not install properly under Docker

* Remove most 'pylint: disable=import-error'. [Kenneth Loafman]

    - add packages to requirements
    - 'gi' is not available on PyPi

* Fix more py3 problems. [Kenneth Loafman]

    - remove import future in some places,
    - fix azurebackend.py to use new azure.

* Recurse glob to include duplicity/backends. [Kenneth Loafman]

* Remove extra print statement. [Kenneth Loafman]

* Add back test\_unadorned...  Cleanup. [Kenneth Loafman]

* Fix pylint code issue. [Kenneth Loafman]

* Fix case where gpg return code is None. [Kenneth Loafman]

* Add pydevd-pycharm to requirements.txt. [Kenneth Loafman]

* Fix to allow using PyCharm or LiClipse pydevd. [Kenneth Loafman]

* Fix doctests to run again. [Kenneth Loafman]

* Remove redundant code. [Kenneth Loafman]

* Print stderr on gpg fail plus error code and string. [Kenneth Loafman]

* Fix handling of gpg\_error\_codes. [Kenneth Loafman]

    - return an 'unknown error code' message if not found
    - ignore error 2 GPG_ERR_UNKNOWN_PACKET, was "invalid packet (ctb=14)"

* Add \_() for translations of msgs in gpg\_error\_codes.py. [Kenneth Loafman]

* Add stderr\_fp back in.  Too much noise otherwise. [Kenneth Loafman]

* Remove stderr\_fp and use process return code to report errors. [Kenneth Loafman]

    - Added file make_gpg_error_codes.py which creates gpg_error_codes.py.
    - Modded gpg.py to remove use of stderr_fp, thus reducing FDs used.

* Remove status\_fd if no sign\_key in gpg.py. [Kenneth Loafman]

    - updated issue125.sh to use testing/gnupg keys
    - issue125.sh passes with `ulimit 1024`

* Cleanup, remove all uses of logger\_fd. [Kenneth Loafman]

* Add back status\_fd for signature verification. [Kenneth Loafman]

* Remove unused GPG file handles. [Kenneth Loafman]

    - removed status and logger filehandles for decrypt
    - testing/manual/issue125 now runs with 'ulimit -n 1536'

* Fix indentation cause by adorning. [Kenneth Loafman]

* Adorn python strings to make merges easier. [Kenneth Loafman]

* Remove extra newline in print. [Kenneth Loafman]

* Add list\_python\_files to tools. [Kenneth Loafman]

* Move find/fix un/adorned to tools. [Kenneth Loafman]

* Unadorn bin/duplicity and bin/rdiffdir. [Kenneth Loafman]

* Recover and add find/fix un/adorned strings. [Kenneth Loafman]

* Fix PEP8 issue. [Kenneth Loafman]

* Optimize imports. [Kenneth Loafman]

    - Remove 'from __future__ import .*'
    - Remove 'from past.utils import old_div'
    - Replace old_div with / or // as needed.

* Optimize imports. [Kenneth Loafman]

* Use os modules fsencode/fsdecode not ours. [Kenneth Loafman]

* Cleanup, remove test\_2to3. [Kenneth Loafman]

* Remove support for Python 2.7.  Second pass. [Kenneth Loafman]

    - remove test_unadorned_string_literals
    - remove find/fix_unadorned_strings.py
    - fix u'string' to be just 'string'

* Remove support for Python 2.7.  First pass. [Kenneth Loafman]

    - remove 'import future' and its call
    - remove 'import builtin *'
    - remove conditionals based on sys.version_info
    - remove mentions in readme and other docs

* Add missing ':''. [Kenneth Loafman]

* Remove requirement for kerberos. [Kenneth Loafman]

    - it's an optional package in webdavbackend.py
    - it does not install properly under Docker

* Remove most 'pylint: disable=import-error'. [Kenneth Loafman]

    - add packages to requirements
    - 'gi' is not available on PyPi

* Fix more py3 problems. [Kenneth Loafman]

    - remove import future in some places,
    - fix azurebackend.py to use new azure.

* Recurse glob to include duplicity/backends. [Kenneth Loafman]

* Remove extra print statement. [Kenneth Loafman]

* Add back test\_unadorned...  Cleanup. [Kenneth Loafman]

* Fix pylint code issue. [Kenneth Loafman]

* Fix case where gpg return code is None. [Kenneth Loafman]

* Add pydevd-pycharm to requirements.txt. [Kenneth Loafman]

* Fix to allow using PyCharm or LiClipse pydevd. [Kenneth Loafman]

* Fix doctests to run again. [Kenneth Loafman]

* Remove redundant code. [Kenneth Loafman]

* Print stderr on gpg fail plus error code and string. [Kenneth Loafman]

* Fix handling of gpg\_error\_codes. [Kenneth Loafman]

    - return an 'unknown error code' message if not found
    - ignore error 2 GPG_ERR_UNKNOWN_PACKET, was "invalid packet (ctb=14)"

* Add \_() for translations of msgs in gpg\_error\_codes.py. [Kenneth Loafman]

* Add stderr\_fp back in.  Too much noise otherwise. [Kenneth Loafman]

* Remove stderr\_fp and use process return code to report errors. [Kenneth Loafman]

    - Added file make_gpg_error_codes.py which creates gpg_error_codes.py.
    - Modded gpg.py to remove use of stderr_fp, thus reducing FDs used.

* Remove status\_fd if no sign\_key in gpg.py. [Kenneth Loafman]

    - updated issue125.sh to use testing/gnupg keys
    - issue125.sh passes with `ulimit 1024`

* Cleanup, remove all uses of logger\_fd. [Kenneth Loafman]

* Add back status\_fd for signature verification. [Kenneth Loafman]

* Remove unused GPG file handles. [Kenneth Loafman]

    - removed status and logger filehandles for decrypt
    - testing/manual/issue125 now runs with 'ulimit -n 1536'

* Fix indentation cause by adorning. [Kenneth Loafman]

* Adorn python strings to make merges easier. [Kenneth Loafman]

* Remove extra newline in print. [Kenneth Loafman]

* Add list\_python\_files to tools. [Kenneth Loafman]

* Move find/fix un/adorned to tools. [Kenneth Loafman]

* Unadorn bin/duplicity and bin/rdiffdir. [Kenneth Loafman]

* Recover and add find/fix un/adorned strings. [Kenneth Loafman]

* Fix PEP8 issue. [Kenneth Loafman]

* Optimize imports. [Kenneth Loafman]

    - Remove 'from __future__ import .*'
    - Remove 'from past.utils import old_div'
    - Replace old_div with / or // as needed.

* Optimize imports. [Kenneth Loafman]

* Use os modules fsencode/fsdecode not ours. [Kenneth Loafman]

* Cleanup, remove test\_2to3. [Kenneth Loafman]

* Remove support for Python 2.7.  Second pass. [Kenneth Loafman]

    - remove test_unadorned_string_literals
    - remove find/fix_unadorned_strings.py
    - fix u'string' to be just 'string'

* Remove support for Python 2.7.  First pass. [Kenneth Loafman]

    - remove 'import future' and its call
    - remove 'import builtin *'
    - remove conditionals based on sys.version_info
    - remove mentions in readme and other docs

* Replace pydrive with pydrive2. Fixes #62. [Kenneth Loafman]

* GDrive backend: Add environment args for configuring oauth flow. [Patrick Riley]

* GDrive backend: For Google OAuth, switch to loopback flow. [Patrick Riley]

* Reduce number of GPG file descriptors, add GPG translatable errors. [Kenneth Loafman]

* Remove sign-build step.  Does not work. [Kenneth Loafman]

* Add back overzealous removal of 'import re'. [Kenneth Loafman]

* Webdav listing failed on responses with namespace 'ns0' [Felix Prüter]

* Fix build of apsw/sqlite3 bundle.  Don't store apsw in repo. [Kenneth Loafman]

* Make sure that FileChunkIO#name is a string, not a bytes-like object. [Josh Goebel]

* Fix possible memory leaks.  Fixes #128.  Fixes #129. [Kenneth Loafman]

* Additional fixes/checks for pexpect version.  Fixes #125. [Kenneth Loafman]

    - Add check to ssh_pexpect_backend, par2backend, for version < 4.5.0
    - Skip test for par2backend instance if version < 4.5.0

* Fixes #125.  Add use\_poll=True to pexpect.run in par2backend. [Kenneth Loafman]

    - allows way too many incrementals to operate.
    - regression test, issue125.sh, added to manual.

* Fix issue #78 - Retry on SHA1 mismatch. [Kenneth Loafman]

* Add missing double quote. [ede]

* Install requirements.dev. [Kenneth Loafman]

* Fix LP bug #1970124 - obscure error message. [Kenneth Loafman]

    Fixes handling of error message with real path, not temp path.

* Nuke a couple of false pylint errors, use inline disable. [Kenneth Loafman]

* Nuke a couple of false pylint errors, fix spelling. [Kenneth Loafman]

* Nuke a couple of false pylint errors. [Kenneth Loafman]

* Minor formatting fix. [ede]

    /builds/duplicity/duplicity/duplicity/backends/s3_boto3_backend.py:93:81: W291 trailing whitespace

* Fixup some minor formatting issues. [ede]

    /builds/duplicity/duplicity/duplicity/backends/s3_boto3_backend.py:92:121: E501 line too long (159 > 120 characters)
    /builds/duplicity/duplicity/duplicity/backends/s3_boto3_backend.py:227:58: W292 no newline at end of file
    /builds/duplicity/duplicity/duplicity/backends/s3_boto_backend.py:34:1: W391 blank line at end of file

* Add --no-files-changed option.  Fixes issue #110. [Kenneth Loafman]

* Fix use of sorted() builtin (does not sort in place). [Kenneth Loafman]

* Revert snapcraft.yaml to build on core18.  core20 was flakey. [Kenneth Loafman]

* Fix #107 - TypeError in restart\_position\_iterator. [Kenneth Loafman]

* Need to pass kwargs to BaseIdentitu. [Kenneth Loafman]

* Fix \_\_init\_\_ in hubic.py.  Fixes #106. [Kenneth Loafman]

* Try building snap on core20. [Kenneth Loafman]

* Try building snap on core20. [Kenneth Loafman]

* Somehow missed boto when doing #102.  Now supported. [Kenneth Loafman]

* Fix logic of skipIf test. [Kenneth Loafman]

* Fix data\_files AUTHORS to CONTRIBUTING.md. [Kenneth Loafman]

* Fix #93 - dupliicity wants private encryption key. [Kenneth Loafman]

* PAR2 backend failes to create par2 file with spaces in name. [Kenneth Loafman]

* Fix bug 930151 - Restore symlink changes target attributes (2) [Kenneth Loafman]

* Fix LP bug 930151 - Restore a symlink changes target attributes. [Kenneth Loafman]

* Fix #89 part 2 - handle small input files where par2 fails. [Kenneth Loafman]

* Fix theme name, sphinx\_rtd\_theme. [Kenneth Loafman]

* Fix PEP8 issue. [Kenneth Loafman]

* Fix #90 - rclone backend fails with spaces in pathnames. [Kenneth Loafman]

* Fix #89 - Add PAR2 number volumes option. [Kenneth Loafman]

* Fix #88 - Add PAR2 creation failure error message. [Kenneth Loafman]

* Fix bug #87, Restore fails and stops on corrupted backup volume. [Kenneth Loafman]

* Fix bug #86, PAR2 backend fails on restore, with patch supplied. [Kenneth Loafman]

* Fixed Catch-22 in pyrax\_identity.hubic.  Debian bug #996577. [Kenneth Loafman]

    Name error on backend HubiC (Baseidentity).  Cannot avoid importing
    pyrax since HubicIdentity requires pyrax.base_identity.BaseIdentity.

* Fix PEP8 style errors. [Kenneth Loafman]

* Fix issue #81 - Assertion fail when par2 prefix forgotten. [Kenneth Loafman]

* Test with mirror and stripe modes. [Kenneth Loafman]

* Fix issue #79 - Multibackend degradation. [Kenneth Loafman]

* Add verbose exception on progress file failure. [Kenneth Loafman]

* Fix test file count after deleting lockfile. [Kenneth Loafman]

* Release lockfile only once. [Kenneth Loafman]

* Release lockfile only once. [Kenneth Loafman]

* Support -o{Global,User}KnownHostsFile in --ssh-options. [Kenneth Loafman]

    Fixes issue #60

* Add pydrive2 to requirements.txt. [Kenneth Loafman]

    Fixes #62.  pydrivebackend was updated to pydrive 2 over a year ago, but
    the requirements.txt file was not updated to reflect this.

* Fix error message on gdrivebackend. [Kenneth Loafman]

* Fix issue #57 SSH backends - IndexError: list index out of range. [Kenneth Loafman]

* Gdata module passes on py27 only. [Kenneth Loafman]

* Restore pylintrc, add requirement. [Kenneth Loafman]

* Fix unadorned string in restored pylint test. [Kenneth Loafman]

* Restored pylint test.  Fixed one issue found. [Kenneth Loafman]

* More py27 packages bit the dust. [Kenneth Loafman]

* Util.uexec() will return u'' if no err msg in e.args. [Kenneth Loafman]

* Util.uexec() should check for e==None on entry. [Kenneth Loafman]

* Mark skip those not usable on py27. Fix version. [Kenneth Loafman]

* Uncomment backends.  Mark skip those not usable on py27. [Kenneth Loafman]

* Lock in some module versions to last supporting py27. [Kenneth Loafman]

* Allow py27 to fail CI.  Restrict mock pkg to 3.05. [Kenneth Loafman]

* Fix bug #1547458 - more consistent passphrase prompt. [Kenneth Loafman]

* Fixes bug #1454136 - SX backend issues. [Kenneth Loafman]

* Fixes bug 1918981 - option to skip trash on delete on mediafire. [Kenneth Loafman]

    Added --mf-purge option to bypass trash

* Fix bug 1919017 - MultiBackend reports failure on file deletion. [Kenneth Loafman]

* Recomment, py2 does not support all backends. [Kenneth Loafman]

* Add azure-storage module requirement.  Uncomment all. [Kenneth Loafman]

* Remove requirement for python3-pytest-runner.  Not used. [Kenneth Loafman]

* Install older version of pip before py35 deprecation. [Kenneth Loafman]

* Add py27 and py35 back to CI. [Kenneth Loafman]

* Fix setup.py to handle Python 2 properly. [Kenneth Loafman]

* Fixes #41 - par2+rsync (non-ssh) fails. [Kenneth Loafman]

### Other

* Merge branch 'main' into branch 'duplicity-py3' [Kenneth Loafman]

* Merge branch 'main' into branch 'duplicity-py3' [Kenneth Loafman]

* Merge branch main into branch duplicity-py3. [Kenneth Loafman]

* Merge branch cleanup into branch duplicity-py3. [Kenneth Loafman]

* Merge main into duplicity-py3. [Kenneth Loafman]

* Merge main into branch duplicity-py3. [Kenneth Loafman]

* Merge branch 'main' into branch 'duplicity-py3' [Kenneth Loafman]

* Merge branch 'main' into branch 'duplicity-py3' [Kenneth Loafman]

* Merge branch main into branch duplicity-py3. [Kenneth Loafman]

* Merge branch cleanup into branch duplicity-py3. [Kenneth Loafman]

* Merge main into duplicity-py3. [Kenneth Loafman]

* Merge main into branch duplicity-py3. [Kenneth Loafman]

* Doc: some reformatting for better readability. [ede]

* Doc: clarify when --s3-endpoint-url,-region-name are need. [ede]

* Pkg:fix: make extra sure correct python binary is used. [edeso]

    remove unmaintained changelog
    add shell wrapper(launcher.sh)
    add debug script
    use shell wrapper as snap binary ignores PATH for python binary on debian

* Optimize CI/CD to only run when needed. [Kenneth Loafman]

* Upgrade to base core20. [Kenneth Loafman]

* Switch website to gitlab.io, promote duplicity.us. [ede]

* Fix website link. [ede]

* Revert "chg:dev:core20 usess py38, not py36." [Kenneth Loafman]

    This reverts commit c074a356d60336b611d096cbdfc98e7ae568475c.

* Slate Backend. [Shr1ftyy]

* Skip tests for ppc64le also. [Mikel Olasagasti Uranga]

* Resolve os option key naming mismatch. [Johannes Winter]

* Set up gdrive client credentials scope correctly. [Christopher Haglund]

* Don't query for filesize. [Johannes Winter]

* Upgrade docker test environment. [Johannes Winter]

* Merge branch 'master' of gitlab.com:duplicity/duplicity. [Kenneth Loafman]

* Fix TypeError. [Clemens Fuchslocher]

* SSHPExpectBackend: Implement \_delete\_list method. [Clemens Fuchslocher]

* MultiBackend: Don't log username and password. [Clemens Fuchslocher]

* Fix NameError. [Clemens Fuchslocher]

* Onedrive: Support using an external client id / refresh token. [Michael Terry]

* Fix functional tests when \_runtestdir is not /tmp. [Guillaume Girol]

* Allow to override manpage date with SOURCE\_DATE\_EPOCH. [Bernhard M. Wiedemann]

    in order to make builds reproducible.
    See https://reproducible-builds.org/ for why this is good
    and https://reproducible-builds.org/specs/source-date-epoch/
    for the definition of this variable.

    Also use UTC/gmtime to be independent of timezone.

* Improved management of volumes unsealing for PCA backend For PCA
backend, unseal all volumes at once when restoring them instead of
unsealing once at a time. Use pre\_process\_download method already
available in dup\_main. Need to implement it on BackendWrapper and
Multibackend as well. [Erwan B]

* Remove backup file. [kenneth@loafman.com]

* Don't skip CI. [Kenneth Loafman]

* Add support for new b2sdk V2 API. [Adam Jacobs]

* Have duplicity retry validate\_block so object storage can report
correct size. [Doug Thompson]

* Replace b2sdk private API references in b2backend with public API. [Adam Jacobs]

* Update b2 backend to use *public* b2sdk API. [Adam Jacobs]

* B2sdk 1.8.0 refactored minimum\_part\_size to recommended\_part\_size
(the value used stays the same) [Adam Jacobs]

    It's a breaking change that makes duplicity fail with the new SDK.

    This fix makes duplicity compatible with both pre- and post- 1.8.0 SDKs.

* Added Google MyDrive support updated man pages and --help text. [Anthony Uphof]

* Fix "Giving up after 5 attempts. timeout: The read operation timed
out" [Christian Perreault]

* Don't sync when removing old backups. [Matthew Marting]

* Fix util.uexc: do not return None. [Michael Kopp]

* Implement Box backend. [Jason Wu]

* Implement megav3 backend to to cater for change in MEGACmd. [Jason Wu]

* Fix documentation for azure backend. [Michael Kopp]

* Fix typo. [Moses Miller]

* Add IDrive backend. [SmilingM]

* Progress bar improvements. [Moses Miller]

* Fix;usr:Fixes bug #1652953 - seek(0) on /dev/stdin crashes. [Kenneth Loafman]

* Add a new Google Drive backend (gdrive:) [Jindřich Makovička]

    - Removes the PyDrive/PyDrive2 dependencies, and depends only on the
      Google API client libraries commonly available in distributions.

    - Uses unchanged JSON secret files as downloaded from GCP

    - Updates the Google Drive API to V3

* Replaced original azure implementation. [Erwin Bovendeur]

* Fixed code smells. [Erwin Bovendeur]

* Azure v12 support. [Erwin Bovendeur]

* Revert "fix:pkg:Remove requirement for python3-pytest-runner.  Not
used." [Kenneth Loafman]

    This reverts commit 2f18eeed907e0b674d1dad9177ce4db0ce1155e7.

* List required volumes when called with 'restore --dry-run' [Matthias Blankertz]

    When restoring in dry-run mode, and with the manifest available, list
    the volumes that would be gotten from the backend when actually
    performing the operation.
    This is intended to aid users of e.g. the S3 backend with (deep) glacier
    storage, allowing the following workflow to recover files, optionally at
    a certain time, from a long-term archive:
    1. duplicity restore --dry-run [--file-to-restore <file/dir>] [--time <time>] boto3+s3://...
    2. Start a Glacier restore process for all the listed volumes
    3. duplicity restore [--file-to-restore <file/dir>] [--time <time>] boto3+s3://...

* Fix sorting of BackupSets by avoiding direct comparison. [Stefan Wehrmeyer]

    Sorting should only compare their time/end_time, not BackupSets directly
    Closes #42

* Update mailing list link. [Chris Coutinho]

* Fixes #16 - Move from boto to boto3. [Kenneth Loafman]

* Py27 EOL 01/2020, py35 EOL 01/2021, remove tests. [Kenneth Loafman]

* Remove 2to3 from ub16 builds. [Kenneth Loafman]

* Move py35 back to ub16, try 2. [Kenneth Loafman]

* Move py35 back to ub16. [Kenneth Loafman]

* Move py27 tests to ub16 and py35 tests to ub18. [Kenneth Loafman]

* Fixes #16 - Move from boto to boto3. [Kenneth Loafman]

* Py27 EOL 01/2020, py35 EOL 01/2021, remove tests. [Kenneth Loafman]

* Move py27 tests to ub16 and py35 tests to ub18. [Kenneth Loafman]

    Move py35 back to ub16.

    Move py35 back to ub16, try 2.

    Remove 2to3 from ub16 builds.

* Fixes #33, remove quotes from identity filename option. [Kenneth Loafman]

* Fix to correctly build \_librsync.so. [Kenneth Loafman]

* Fix to add --inplace option to build\_ext. [Kenneth Loafman]

* Rename pylintrc to .pylintrc. [Kenneth Loafman]

* Multibackend: fix indentation error that was preventing from
registering more than one affinity prefix per backend. [KheOps]

* Move testfiles dir to a temp location. [Kenneth Loafman]

    - was crashing LiClipse/Eclipse when present in project.
    - so far only Darwin and Linux are supported, default Linux.
    - Darwin uses 'getconf DARWIN_USER_TEMP_DIR' for temp dir.
    - Linux uses TMPDIR, TEMP, or defaults to /tmp.

* Update .gitlab-ci.yml to need code test to pass. [Kenneth Loafman]

* Remove basepython in code and coverage tests. [Kenneth Loafman]

* Add report.xml. [Kenneth Loafman]

* Bulk replace testfiles with /tmp/testfiles. [Kenneth Loafman]

* Skip unicode tests that fail on non-Linux systems like macOS. [Kenneth Loafman]

* Onedrive: Support using an external client id / refresh token. [Michael Terry]

* Update .gitlab-ci.yml to need code test to pass. [Kenneth Loafman]

* Fix issue #26 Backend b2 backblaze fails with nameprefix restrictions. [Kenneth Loafman]

* Fix issue #29 Backend b2 backblaze fails with nameprefix restrictions. [Kenneth Loafman]

* Fix unadorned strings. [Kenneth Loafman]

* Report errors if B2 backend does exist but otherwise fails to import. [Phil Ruffwind]

    Sometimes import can fail because one of B2's dependencies is broken.

    The trick here is to query the "name" attribute of ModuleNotFoundError
    to see if B2 is the module that failed. Unfortunately this only works on
    Python 3.6+. In older versions, the original behavior is retained.

    This partially mitigates the issue described in
    https://github.com/henrysher/duplicity/issues/14.

* Add report.xml. [Kenneth Loafman]

* Remove basepython in code and coverage tests. [Kenneth Loafman]

* Fix pep8 warning. [Kenneth Loafman]

* Added option --log-timestamp to prepend timestamp to log entry. [Kenneth Loafman]

    The default is off so not to break anything, and is set to on when the
    option is present.  A Catch-22 hack was made since we had to get options
    for the log before adding a formatter, yet the commandline parser needs
    the logger.  Went old school on it.

* Improve. [Gwyn Ciesla]

* Improve patch for Python 3.10. [Gwyn Ciesla]

* Conditionalize for Python version. [Gwyn Ciesla]

* Patch for Python 3.10. [Gwyn Ciesla]

* Fixup ignore\_regexps for optional text. [Kenneth Loafman]

* Fix issue #26 (again) - duplicity does not clean up par2 files. [Kenneth Loafman]

* Fix issue #26 - duplicity does not clean up par2 files. [Kenneth Loafman]

* Fix issue #25 - Multibackend not deleting files. [Kenneth Loafman]

* Adjust setup.py for changelog changes. [Kenneth Loafman]

* Delete previous manual changelogs. [Kenneth Loafman]

* Tools to make a CHANGELOG.md from git commits. [Kenneth Loafman]

    $ [sudo] pip install gitchangelog

* Make exclude-if-present more robust. [Michael Terry]

    Specifically, handle all the "common errors" when listing a directory
    to see if the mentioned file is in it. Previously, we had done a
    check for read access before listing. But it's safe to try to list
    and just catch the errors that happen.

* Drop default umask of 0077. [Michael Terry]

    For most backends, it doesn't actually take effect. And it can be
    confusing for people that back up to a drive that is ext4-formatted
    but then try to restore on a new system.

    If folks are worried about others accessing the backup files,
    encryption is the recommended path for that.

    https://gitlab.com/duplicity/duplicity/-/issues/24

* Comment out RsyncBackendTest, again. [Kenneth Loafman]

* Fix some unadorned strings. [Kenneth Loafman]

* Fixed RsyncBackendTeest with proper URL. [Kenneth Loafman]

* Fix issue #23. [Yump]

    Fix unicode crash on verify under python3, when symlinks have changed targets since the backup was taken.

* Rclonebackend now logs at the same logging level as duplicity. [Kenneth Loafman]

* Allow sign-build to fail on walk away.  Need passwordless option. [Kenneth Loafman]

* Fix --rename typo. [Michael Terry]

* Move back to VM build, not remote.  Too many issues with remote. [Kenneth Loafman]

* Escape single quotes in machine-readable log messages. [Michael Terry]

    https://gitlab.com/duplicity/duplicity/-/issues/21

* Uncomment review-tools for snap. [Kenneth Loafman]

* Whoops, missing wildcard '*'. [Kenneth Loafman]

* Changes to allow remote build of snap on LP. [Kenneth Loafman]

* Changes to allow remote build of snap on LP. [Kenneth Loafman]

* Add a pylint disable-import-error flag. [Kenneth Loafman]

* Change urllib2 to urllib.request in parse\_digest\_challenge(). [Kenneth Loafman]

* Fix Python 3.9 test in .gitlab-ci.yaml. [Kenneth Loafman]

* Fix Python 3.9 test in .gitlab-ci.yaml. [Kenneth Loafman]

* Add Python 3.9 to .gitlab-ci.yaml. [Kenneth Loafman]

* Add Python 3.9 to the test suite.  It tests sucessfuly. [Kenneth Loafman]

* Fix bug #1893481 again for Python2.  Missed include. [Kenneth Loafman]

* Fix bug #1893481 Error when logging improperly encoded filenames. [Kenneth Loafman]

    - Reconfigure stdout/stderr to use errors='surrogateescape' in Python3
    	and errors='replace' in Python2.
      - Add a manual test case to check for regression.

* Merged in s3-unfreeze-all. [Kenneth Loafman]

* Wait for Glacier batch unfreeze to finish. [Marco Herrn]

    The ThreadPoolExecutor starts the unfreezing of volumes in parallel.
    However we can wait until it finishes its work for all volumes.

    This currently does _not_ wait until the unfreezing process has
    finished, but only until the S3 'restore()' operations have finished
    (which can take a bit time).

    The actual (sequential) pre_processing of the volumes to restore then
    waits for the actual unfreezing to finish by regularly checking the
    state of the unfreezing.

* Adorn string as unicode. [Marco Herrn]

* Utilize ThreadPoolExecutor for S3 glacier unfreeze. [Marco Herrn]

    Starting one thread per file to unfreeze from Glacier can start a huge
    amounts of threads in large backups.
    Using a thread pool should cut this down to a more appropriate number of
    threads.

* Refine codestyle according to PEP-8. [Marco Herrn]

* Adorn strings as unicode. [Marco Herrn]

* S3 unfreeze all files at once. [Marco Herrn]

    When starting a restore from S3 Glacier, start the unfreezing of all
    volumes at once by calling botos 'restore()' method for each volume in a
    separate thread.

    This is only implemented in the boto backend, not in the boto3 backend.

* Add boto3 to list of requirements. [Kenneth Loafman]

* Remove ancient CVS Id macro. [Kenneth Loafman]

* Merged in OutlawPlz:paramiko-progress. [Kenneth Loafman]

* Fixes paramiko backend progress bar. [Matteo Palazzo]

* Merged in lazy init for Boto3 network connections. [Kenneth Loafman]

* Initial crack at lazy init for Boto3. [Carl Alexander Adams]

* Record the hostname, not the fqdn, in manifest files. [Michael Terry]

    We continue to check the fqdn as well, to keep backward
    compatibility.

    https://bugs.launchpad.net/duplicity/+bug/667885

* Avoid calling stat when checking for exclude-if-present files. [Michael Terry]

    If a folder with rw- permissions (i.e. read and write, but no exec)
    is examined for the presence of an exclude-if-present file, we would
    previously throw an exception when trying to stat the file during
    Path object construction.

    But we don't need to stat in this case. This patch just calls
    listdir() and checks if the file is in that result.

* Fix build control files after markdown conversion. [Kenneth Loafman]

* Recover some changes lost after using web-ide. [Kenneth Loafman]

* Paperwork. [Kenneth Loafman]

* Set default values for s3\_region\_name and s3\_endpoint\_url. [Marco Herrn]

    Fixes #12

* Allow setting s3 region and endpoint. [Marco Herrn]

    This commit introduces the new commandline options
      --s3-region-name
      --s3-endpoint-url
    to specify these parameters. This allows using s3 compatible providers
    like Scaleway or OVH.

    It is probably useful for Amazon accounts, too, to have more fine
    grained influence on the region to use.

* Update README-REPO.md. [Kenneth Loafman]

* Make code view consistent. [Kenneth Loafman]

* Update setup.py. [Kenneth Loafman]

* Update README.md. [Kenneth Loafman]

* Paperwork. [Kenneth Loafman]

* Revert "Merge branch 's3-boto3-region-and-endpoint' into 'master'" [Kenneth Loafman]

    This reverts commit 6dac477cb3ddfb5f7a8f05162d1658725f4f379a, reversing
    changes made to cdfbaf8cfd4fcf2fbbecc3c2adc9fe1753ee6c30.

* Bump version for LP dev build. [Kenneth Loafman]

* Always paperwork. [Kenneth Loafman]

* Allow setting s3 region and endpoint. [Marco Herrn]

    This commit introduces the new commandline options
      --s3-region-name
      --s3-endpoint-url
    to specify these parameters. This allows using s3 compatible providers
    like Scaleway or OVH.

    It is probably useful for Amazon accounts, too, to have more fine
    grained influence on the region to use.

* Fix missing FileNotUploadedError in pydrive backend. [Martin Sucha]

    Since 5bba3ba98ed3560329a80b829154d24f5d881ad9, FileNotUploadedError
    is not imported anymore, resulting in an exception in case
    some of the files failed to upload. Adding the import back.

* Fixed indentation. [Joshua Chan]

* Added shared drive support to existing `pydrive` backend instead of a
new backend. [Joshua Chan]

* PydriveShared backend is identical to Pydrive backend, except that it
works on shared drives rather than personal drives. [Joshua Chan]

* Include the query when parsing the backend URL string, so users can
use it to pass supplementary info to the backend. [Joshua Chan]

* Fix caps on X-Python-Version. [Kenneth Loafman]

* Fix issue #10 - ppa:duplicity-*-git fails to install on Focal Fossa. [Kenneth Loafman]

    - Set correct version requirements in debian/control.

* Remove python-cloudfiles from suggestions. [Jairo Llopis]

    This dependency cannot be installed on Python 3:

    ```
    #12 19.82   Downloading python-cloudfiles-1.7.11.tar.gz (330 kB)
    #12 20.00     ERROR: Command errored out with exit status 1:
    #12 20.00      command: /usr/local/bin/python -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-2iwvh4bp/python-cloudfiles/setup.py'"'"'; __file__='"'"'/tmp/pip-install-2iwvh4bp/python-cloudfiles/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base /tmp/pip-pip-egg-info-b1gvstfs
    #12 20.00          cwd: /tmp/pip-install-2iwvh4bp/python-cloudfiles/
    #12 20.00     Complete output (9 lines):
    #12 20.00     Traceback (most recent call last):
    #12 20.00       File "<string>", line 1, in <module>
    #12 20.00       File "/tmp/pip-install-2iwvh4bp/python-cloudfiles/setup.py", line 6, in <module>
    #12 20.00         from cloudfiles.consts import __version__
    #12 20.00       File "/tmp/pip-install-2iwvh4bp/python-cloudfiles/cloudfiles/__init__.py", line 82, in <module>
    #12 20.00         from cloudfiles.connection     import Connection, ConnectionPool
    #12 20.00       File "/tmp/pip-install-2iwvh4bp/python-cloudfiles/cloudfiles/connection.py", line 13, in <module>
    #12 20.00         from    urllib    import urlencode
    #12 20.00     ImportError: cannot import name 'urlencode' from 'urllib' (/usr/local/lib/python3.8/urllib/__init__.py)
    #12 20.00     ----------------------------------------
    #12 20.00 ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.
    ```

    Also, it is no longer supported. Rackspace uses `pyrax` nowadays. Removing to avoid confusions.

* Update azure requirement. [Jairo Llopis]

    Trying to install `azure` today prints this error:

    ```
    Collecting azure
      Downloading azure-5.0.0.zip (4.6 kB)
        ERROR: Command errored out with exit status 1:
         command: /usr/local/bin/python -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-gzzfb6dp/azure/setup.py'"'"'; __file__='"'"'/tmp/pip-install-gzzfb6dp/azure/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base /tmp/pip-pip-egg-info-1xop0k3_
             cwd: /tmp/pip-install-gzzfb6dp/azure/
        Complete output (24 lines):
        Traceback (most recent call last):
          File "<string>", line 1, in <module>
          File "/tmp/pip-install-gzzfb6dp/azure/setup.py", line 60, in <module>
            raise RuntimeError(message)
        RuntimeError:

        Starting with v5.0.0, the 'azure' meta-package is deprecated and cannot be installed anymore.
        Please install the service specific packages prefixed by `azure` needed for your application.

        The complete list of available packages can be found at:
        https://aka.ms/azsdk/python/all

        Here's a non-exhaustive list of common packages:

        -  azure-mgmt-compute (https://pypi.python.org/pypi/azure-mgmt-compute) : Management of Virtual Machines, etc.
        -  azure-mgmt-storage (https://pypi.python.org/pypi/azure-mgmt-storage) : Management of storage accounts.
        -  azure-mgmt-resource (https://pypi.python.org/pypi/azure-mgmt-resource) : Generic package about Azure Resource Management (ARM)
        -  azure-keyvault-secrets (https://pypi.python.org/pypi/azure-keyvault-secrets) : Access to secrets in Key Vault
        -  azure-storage-blob (https://pypi.python.org/pypi/azure-storage-blob) : Access to blobs in storage accounts

        A more comprehensive discussion of the rationale for this decision can be found in the following issue:
        https://github.com/Azure/azure-sdk-for-python/issues/10646


        ----------------------------------------
    ```

    So it's better to update this suggestion to `azure-mgmt-storage` instead.

* Fix bug #1211481 with merge from Raffaele Di Campli. [Kenneth Loafman]

    - Ignores the uid/gid from the archive and keeps the current user's
    one.
      - Recommended for restoring data to mounted filesystem which do not
        support Unix ownership or when root privileges are not available.

* Added `--do-not-restore-ownership` option. [Jacotsu]

    Ignores the uid/gid from the archive and keeps the current user's one.
    Recommended for restoring data to mounted filesystem which do not
    support Unix ownership or when root privileges are not available.

    Solves launchpad bug #1211481

* Fix bug #1887689 with patch from Matthew Barry. [Kenneth Loafman]

    - Cleanup with Paramiko backend does not remove files due to missing
        filename byte decoding

* Bump version for LP build. [Kenneth Loafman]

* Fix check for s3 glacier/deep. [Michael Terry]

    This allows encryption validation to continue to work outside of
    those s3 glacier/deep scenarios.

* Change from push to upload. [Kenneth Loafman]

* Add specific version for six. [Kenneth Loafman]

* Set deprecation version to 0.9.0 for short filenames. [Kenneth Loafman]

* Fixes for issue #7, par2backend produces badly encoded filenames. [Kenneth Loafman]

* Added a couple of fsdecode calls for issue #7. [Kenneth Loafman]

* Generalize exception for failed get\_version() on LaunchPad. [Kenneth Loafman]

* Ignore *.so files. [Kenneth Loafman]

* Update docs. [Kenneth Loafman]

* Catch up on paperwork. [Kenneth Loafman]

* Fix --rename encoding. [Michael Terry]

* Skip tests failing on py27 under 18.04 (timing error). [Kenneth Loafman]

* Fix code style issue. [Kenneth Loafman]

* Add PATHS\_FROM\_ECLIPSE\_TO\_PYTHON to environ whan starting pydevd. [Kenneth Loafman]

* Add *.pyc to .gitignore. [Kenneth Loafman]

* Replace compilec.py with 'setup.py build\_ext', del compilec.py. [Kenneth Loafman]

* Fix unadorned string. [Kenneth Loafman]

* Fix usage of TOXPYTHON and overrides/bin shebangs. [Kenneth Loafman]

* Use default 'before\_script' for py27. [Kenneth Loafman]

* Don't collect coverage unless needed. [Kenneth Loafman]

* Support PyDrive2 library in the pydrive backend. [Jindrich Makovicka]

    Unlike PyDrive, the PyDrive2 fork is actively maintained.

* Tidy .gitlab-ci.yml, fix py3.5 test, add py2.7 test (allowed to fail) [Aaron Whitehouse]

* Test code instead of py27 since py27 is tested elsewhere. [Kenneth Loafman]

* Fix RdiffdirTest to use TOXPYTHON as well. [Kenneth Loafman]

* Set TOXPYTHON before tests. [Kenneth Loafman]

* Put TOXPYTHON in passed environment. [Kenneth Loafman]

* More fixes for bug #1877885 - Catch quota overflow on Mega upload. [Kenneth Loafman]

* More fixes for bug #1877885 - Catch quota overflow on Mega upload. [Kenneth Loafman]

* Undo: Try forcing python version to match tox testing version. [Kenneth Loafman]

* Always upgrade pip. [Kenneth Loafman]

* Try forcing python version to match tox testing version. [Kenneth Loafman]

* Uncomment all tests. [Kenneth Loafman]

* Test just py27 for now. [Kenneth Loafman]

* Replace bzr with git. [Kenneth Loafman]

* Don't load repo version of future, let pip do it. [Kenneth Loafman]

* Hmmm, Gitlab yaml does not like continuation lines.  Fix it. [Kenneth Loafman]

* Fix typo. [Kenneth Loafman]

* Update to use pip as module and add py35 test. [Kenneth Loafman]

* Add py35 to CI tests. [Kenneth Loafman]

* More changes to support Xenial. [Kenneth Loafman]

* Fix typo. [Kenneth Loafman]

* Fix duplicity to run under Python 3.5. [Kenneth Loafman]

* Fix duplicity to run under Python 3.5. [Kenneth Loafman]

* Update .gitlab-ci.yml to update pip before installing other pip
packages (to try to fix more-itertools issue:
https://github.com/pytest-dev/pytest/issues/4770 ) [Aaron Whitehouse]

* Don't include .git dir when building docker images. [Kenneth Loafman]

* Upgrade pip before installing requirements with it. Fixes more-
itertools error as newer versions of pip identify that the latest
more-itertools are incompatible with python 2. [Aaron Whitehouse]

* Patched in a megav2backend.py to update to MEGAcmd tools. [Kenneth Loafman]

    - Author: Jose L. Domingo Lopez <github@24x7linux.com>
      - Man pages, docs, etc. were included.

* Change log.Warning to log.Warn.  Whoops! [Kenneth Loafman]

* Fixed bug #1875937 - validate\_encryption\_settings() fails w/S3
glacier. [Kenneth Loafman]

    - Skip validation with a warning if S3 glacier or deep storage
    specified

* Restore commented our backend requirements. [Kenneth Loafman]

* Fixes for rclonebackend from Francesco Magno (original author) [Kenneth Loafman]

    - copy command has been replaced with copyto, that is a specialized
        version for single file operation. Performance-wise, we don't have
        to include a single file in the local side directory, and we don't
        have to list all the files in the remote to check what to
    syncronize.
        Additionally, we don't have to mess up with renaming because the
        copy command didn't support changing filename during transfer
        (because was oriented to transfer whole directories).
      - delete command has been replaced with deletefile. Same here, we
        have a specialized command for single file operation. Much more
    efficient.
      - ls command has been replaced with lsf, that is a specialized version
        that returns only filenames. Since duplicity needs only those, less
        bytes to transfer, and less parsing to do.
      - lastly, I have reintroduced a custom subprocess function because the
    one
        inherithed from base class is checked, and throws an exception in
    case of
        non zero return code. The ls command family returns a non zero value
    if
        the directory does not exist in the remote, so starting a new backup
        in a non existent directory is impossible at the moment because ls
    fails
        repeatedly until duplicity gives up. This is a bug in the current
    implementation.
        There is the same problem (but less severe) in _get method, using
    the default
        self.subprocess_popen a non zero return code will throw an exception
    before we
        can cleanup the partially downloaded file, if any.

* Version man pages during setup.py install. [Kenneth Loafman]

* More fixes for Launchpad build limitations. [Kenneth Loafman]

* More fixes for Launchpad build limitations. [Kenneth Loafman]

* Move setuptools\_scm to setup\_requires. [Kenneth Loafman]

* Back off requirements for fallback\_version in setup.py. [Kenneth Loafman]

* Add some requirements for LP build. [Kenneth Loafman]

* Make sure we get six from pip to support dropbox. [Kenneth Loafman]

* Provide fallback\_version for Launchpad builder. [Kenneth Loafman]

* Remove python3-setuptools-scm from setup.py. [Kenneth Loafman]

* Add python3-setuptools-scm to debian/control. [Kenneth Loafman]

* Try variation with hyphen seperator. [Kenneth Loafman]

* Try python3\_setuptools\_scm (apt repo name).  Probably too old. [Kenneth Loafman]

* Add setuptools\_scm to install\_requires. [Kenneth Loafman]

* Fixed release date. [Kenneth Loafman]

* Fixed bug #1876446 - WebDAV backend creates only tiny or 0 Byte files. [Kenneth Loafman]

* Fix to run with --dist-dir command. [Kenneth Loafman]

* Fixed bug #1876778 - byte/str issues in megabackend.py. [Kenneth Loafman]

* Fix to use 'setup.py develop' instead of sdist. [Kenneth Loafman]

* Fix to run with --dist-dir command. [Kenneth Loafman]

* Fixed bug #1875529 - Support hiding instead of deletin on B2. [Kenneth Loafman]

* Uncomment upload and sign. [Kenneth Loafman]

* Reworked versioning to be git tag based. [Kenneth Loafman]

* Migrate bzr to git. [Kenneth Loafman]

* Fixed bug #1872332 - NameError in ssh\_paramiko\_backend.py. [ken]

* Fix spelling error. [ken]

* Fixed bug #1869921 - B2 backup resume fails for TypeError. [ken]

* More changes for pylint. * Resolved conflict between duplicity.config
and testing.manual.config * Normalized emacs mode line to have
encoding:utf8 on all *.py files. [Kenneth Loafman]

* More changes for pylint. * Remove copy.com refs. [Kenneth Loafman]

* More changes for pylint. [Kenneth Loafman]

* More changes for pylint. [Kenneth Loafman]

* Enable additional pylint warnings.  Make 1st pass at correction.   -
unused-argument,     unused-wildcard-import,     redefined-builtin,
bad-indentation,     mixed-indentation. [Kenneth Loafman]

* Fixed bug #1868414 - timeout parameter not passed to   BlobService for
Azure backend. [Kenneth Loafman]

* Fixed bug #1867742 - TypeError: fsdecode()   takes 1 positional
argument but 2 were given   with PCA backend. [Kenneth Loafman]

* Fixed bug #1867529 - UnicodeDecodeError: 'ascii'   codec can't decode
byte 0x85 in position 0:   ordinal not in range(128) with PCA. [Kenneth Loafman]

* Fixed bug #1867468 - UnboundLocalError (local   variable 'ch\_err'
referenced before assignment)   in ssh\_paramiko\_backend.py. [Kenneth Loafman]

* Fixed bug #1867444 - UnicodeDecodeError: 'ascii'   codec can't decode
byte 0x85 in position 0:   ordinal not in range(128) using PCA backend. [Kenneth Loafman]

* Fixed bug #1867435 - TypeError: must be str,   not bytes using PCA
backend. [Kenneth Loafman]

* Move pylint config from test\_code to pylintrc. [Kenneth Loafman]

* Cleaned up some setup issues where the man pages   and snapcraft.yaml
were not getting versioned. [Kenneth Loafman]

* Fixed bug #1769267 - [enhancement] please consider   using rclone as
backend. [Kenneth Loafman]

* Fixed bug #1755955 - best order is unclear,   of exclude-if-present
and exclude-device-files   - Removed warning and will now allow these
two to     be in any order.  If encountered outside of the     first
two slots, duplicity will silently move     them to be in the first
two slots.  Within those     two slots the order does not matter. [ken]

* Fixed a couple of file history bugs:   - #1044715 Provide a file
history feature     + removed neutering done between series   -
#1526557 --file-changed does not work     + fixed str/bytes issue
finding filename. [ken]

* Fixed bug #1865648 - module 'multiprocessing.dummy' has   no attribute
'cpu\_count'.   - replaced with module psutil for cpu\_count() only
- appears Arch Linux does not support multiprocessing. [ken]

* Mod to get focal build on LP working. [ken]

* Mod to get focal build on LP working. [ken]

* Mod to get focal build on LP working. [ken]

* Fixed to work around par2 0.8.1 core dump on short name   -
https://github.com/Parchive/par2cmdline/issues/145. [ken]

* Fixed bug #1857818 - startswith first arg must be bytes   - use
util.fsdecode on filename. [ken]

* Fixed bug #1863018 - mediafire backend fails on py3   - Fixed handling
of bytes filename in url. [ken]

* Add rclone requirement to snapcraft.yaml. [ken]

* Fixed bug #1236248 - --extra-clean clobbers old backups   - Removed
--extra-clean, code, and docs. [ken]

* Fixed bug #1862672 - test\_log does not respect TMPDIR   - Patch
supplied by Jan Tojnar. [ken]

* Fixed bug #1860405 - Auth mechanism not supported   - Added
python3-boto3 requirement to snapcraft.yaml. [ken]

* More readthedocs munges. [ken]

* Don't format the po files for readthedocs. [ken]

* Add readthedocs.yaml config file, try 3. [ken]

* Add readthedocs.yaml config file, try 2. [ken]

* Add readthedocs.yaml config file. [ken]

* Remove intltool for readthedocs builder. [ken]

* Add python-gettext for readthedocs builder. [ken]

* Add gettext/intltool for readthedocs builder. [ken]

* Add gettext for readthedocs builder. [ken]

* Add intltool for readthedocs builder. [ken]

* Add intltools for readthedocs builder. [ken]

* Add intltools for readthedocs builder. [ken]

* Point readthedocs.io to this repo. [ken]

* Renamed botobackend.py to s3\_boto\_backend.py. [ken]

* Renamed MulitGzipFile to GzipFile to avoid future problems with
upstream author of mgzip fixing the Mulit -> Multi typo. [Byron Hammond]

* Adding missed mgzip import and adjusting untouched unit tests. [Byron Hammond]

* Adding multi-core support by using mgzip instead of gzip. [Byron Hammond]

* Missing comma. [ken]

* Some code cleanup and play with docs. [ken]

* Uncomment snapcraft sign-build.  Seems it's fixed now. [ken]

* Fix argument order on review-tools. [ken]

* Reworked setup.py to build a pip-compatible   distribution tarball of
duplicity. * Added dist/makepip for convenience. [ken]

* Adjust Dockerfiles to new requirements. [ken]

* Fix bug #1861287 - Removing old backup chains   fails using
pexpect+sftp. [ken]

* Adjust Dockerfiles to new requirements. [ken]

* Enhance setup.py/cfg to allow install by pip. [ken]

* Enhance setup.py/cfg to allow install by pip. [ken]

* Enhance setup.py/cfg to allow install by pip. [ken]

* Bump version. [Kenneth Loafman]

* Gave up fighting the fascist version control   munging on
snapcraft.io.  Duplicity now has the   form 0.8.10.1558, where the
last number is the   bzr revno.  Can't do something nice like having
a dev/fin indicator like 0.8.10dev1558 for dev   versions and a fin
for release or final. [Kenneth Loafman]

* Fixed bug #1858207 missing targets in multibackend   - Made it
possible to return default value instead     of taking a fatal
exception on an operation by     operation approach.  The only use
case now is for     multibackend to be able to list all targets and
report back on the ones that don't work. [Kenneth Loafman]

* Fixed bug #1858204 - ENODEV should be added to   list of recognized
error stringa. [Kenneth Loafman]

* Comment out test\_compare, again. [Kenneth Loafman]

* Clean up deprecation errors in Python 3.8. [Kenneth Loafman]

* Clean up some TODO tasks in testing code. [kenneth@loafman.com]

* Skip functional/test\_selection::TestUnicode if   python version is
less than 3.7. [kenneth@loafman.com]

* Fixed bug #1859877 - syntax warning on python 3.8. [kenneth@loafman.com]

* Move to single-sourceing the package version   - Rework setup.py,
dist/makedist, dist/makesnap,     etc., to get version from
duplicity/\_\_init\_\_.py   - Drop dist/relfiles.  It was problematic. [kenneth@loafman.com]

* Fixed bug #1859304 with patch from Arduous   - Backup and restore do
not work on SCP backend. [kenneth@loafman.com]

* Revert last change to duplicity.\_\_init\_\_.py. [kenneth@loafman.com]

* Py27 supports unicode returns for translations   - remove install that
does not incude unicode   - Removed some unneeded includes of gettext. [kenneth@loafman.com]

* Fixed bug #1858713 - paramiko socket.timeout   - chan.recv() can
return bytes or str based on     the phase of the moon.  Make
allowances. [kenneth@loafman.com]

* Switched to python3 for snaps. [kenneth@loafman.com]

* Fix unadorned string. [kenneth@loafman.com]

* Change of plans.  Skip test if rclone not present. [kenneth@loafman.com]

* Add rclone to setup testing requirements. [kenneth@loafman.com]

* Revert to testing after build. [kenneth@loafman.com]

* Fixed bug #1855736 again - Duplicity fails to start   - remove decode
from unicode string. [kenneth@loafman.com]

* Fixed bug #1858295 - Unicode error in source filename   - decode arg
if it comes in as bytes. [kenneth@loafman.com]

* Add snapcraft login to makesnap. [kenneth@loafman.com]

* Fix bug #1858153 with patch from az   - mega backend: fails to create
directory. [kenneth@loafman.com]

* Fix bug #1857734 - TypeError in ssh\_paramiko\_backend   - conn.recv()
can return bytes or string, make string. [kenneth@loafman.com]

* Fix bytes/string differences in subprocess\_popen()   - Now returns
unicode string not bytes, like python2. [kenneth@loafman.com]

* Convert all shebangs to python3 for bug #1855736. [kenneth@loafman.com]

* Fixed bug #1857554 name 'file' is not defined   - file() calls
replaced by open() in 3 places. [kenneth@loafman.com]

* Original rclonebackend.py from Francesco Magno for Python 2.7. [kenneth@loafman.com]

* Fix manpage indention clarify difference between boto backends add
boto+s3:// for future use when boto3+s3:// will become default s3
backend. [ed.so]

* Renamed testing/infrastructure to testing/docker. [kenneth@loafman.com]

* Fixed a mess I made.  setup.py was shebanged to   Py3, duplicity was
shebanged to Py2.  This meant   that duplicity ran as Py2 but could
not find its   modules because they were under Py3.  AArgh! [kenneth@loafman.com]

* Fixed bug #1855736 - duplicity fails to start   - Made imports
absolute in dup\_main.py. [kenneth@loafman.com]

* Fixed bug #1856447 with hint from Enno L   - Replaced with formatted
string. [kenneth@loafman.com]

* Fixed bug #1855736 with help from Michael Terry   - Decode Popen
output to utf8. [kenneth@loafman.com]

* Fixed bug #1855636 with patch from Filip Slunecko   - Wrong buf type
returned on error.  Make bytes. [kenneth@loafman.com]

* Merged in translation updates. [kenneth@loafman.com]

* Removed abandoned ref in README * Comment out signing in makesnap. [kenneth@loafman.com]

* Fixed bug #1854554 with help from Tommy Nguyen   - Fixed a typo made
during Python 3 conversion. [kenneth@loafman.com]

* Fixed bug #1855379 with patch from Daniel González Gasull   - Issue
warning on temporary connection loss. * Fixed misc coding style
errors. [kenneth@loafman.com]

* Disabling autotest for LP build.  I have run tests on all Ubuntu
releases since 18.04, so the code works.  To run tests manually, run
tox from the main directory.  Maybe LP build will work again soon. [kenneth@loafman.com]

* Update to manpage. [Carl A. Adams]

* BUGFIX: list should retun byte strings, not unicode strings. [Carl A. Adams]

* Updating comments. [Carl A. Adams]

* Select boto3/s3 backend via url scheme rather than by CLI option.  Doc
changes to support this. [Carl A. Adams]

* Renaming boto3 backend file. [Carl A. Adams]

* Adding support for AWS Glacier Deep Archive.  Fixing some typos. [Carl A. Adams]

* Manpage updates.  Cleaning up the comments to reflect my current
plans. Some minor clean-ups. [Carl A. Adams]

* Updating comments. [Carl A. Adams]

* SSE options comitted. AES tested, KMS not tested. [Carl A. Adams]

* Handling storage class on backup. [Carl A. Adams]

* Handling storage class on backup. [Carl A. Adams]

* Minor clean-ups. [Carl A. Adams]

* Rename boto3 backend py file. [Carl A. Adams]

* Removing 'todo' comment for multi support.  Defaults in Boto3 chunk
the upload and attempt to use multiple threads.  See https://boto3.ama
zonaws.com/v1/documentation/api/latest/reference/customizations/s3.htm
l#boto3.s3.transfer.TransferConfig. [Carl A. Adams]

* Format fix. [Carl A. Adams]

* Fixing status reporting.  Cleanup. [Carl A. Adams]

* Better exception handling. Return -1 for unknwon objects in \_query. [Carl A. Adams]

* Updating comment. [Carl A. Adams]

* Making note of a bug. [Carl A. Adams]

* Removing unused imports. [Carl A. Adams]

* Implementing \_query for boto3. [Carl A. Adams]

* Minor clean-up. [Carl A. Adams]

* Some initial work on a boto3 back end. [Carl A. Adams]

* Convert debian build to Python 3. [kenneth@loafman.com]

* Replace python with python3 in shebang. [kenneth@loafman.com]

* Convert debian build to Python 3. [kenneth@loafman.com]

* Fixed bug #1853809 - Tests failing with Python 3.8 / Deprecation
warnings   - Fixed the deprecation warnings with patch from Sebastien
Bacher   - Fixed test\_globmatch to handle python 3.8 same as 3.7   -
Fixed tox.ini to include python 3.8 in future tests. [kenneth@loafman.com]

* Fixed bug #1853655 - duplicity crashes with --exclude-older-than   -
The exclusion setup checked for valid string only.  Made     the code
comprehend datetime (int) as well. [kenneth@loafman.com]

* Just some cosmetic changes. [kenneth@loafman.com]

* Fixed bug #1851668 with help from Wolfgang Rohdewald   - Applied
patches to handle translations. [kenneth@loafman.com]

* Fixed bug #1852876 '\_io.BufferedReader' object has no attribute
'uc\_name'   - Fixed a couple of instances where str() was used in
place of util.uexc()   - The file was opened with builtins, so use
name, not uc\_name. [kenneth@loafman.com]

* Added build signing to dist/makesnap. [kenneth@loafman.com]

* Fixed bug #1852848 with patch from Tomas Krizek   - B2 moved the API
from "b2" package into a separate "b2sdk" package.     Using the old
"b2" package is now deprecated. See link:     https://github.com/Backb
laze/B2\_Command\_Line\_Tool/blob/master/b2/\_sdk\_deprecation.py   -
b2backend.py currently depends on both "b2" and "b2sdk", but use of
"b2"     is enforced and "b2sdk" isn't used at all.   - The attached
patch uses "b2sdk" as the primary dependency. If the new     "b2sdk"
module isn't available, it falls back to using the old "b2" in
order to keep backward compatibility with older installations. [kenneth@loafman.com]

* Fixed bug #1851727 - InvalidBackendURL for multi backend   - Encode to
utf8 only on Python2, otherwise leave as unicode. [kenneth@loafman.com]

* Fix resuming without a passphrase when using just an encryption key. [Michael Terry]

* Fix bytes/string issue in pydrive backend upload. [Michael Terry]

* Fixed bug #1851167 with help from Aspen Barnes   - Had Popen() to
return strings not bytes. [kenneth@loafman.com]

* Added dist/makesnap to make spaps automagically. [kenneth@loafman.com]

* Fixed bug #1850990 with suggestion from Jon Wilson   - --s3-use-
glacier and --no-encryption cause slow backups. [kenneth@loafman.com]

* Fix header in CHANGELOG. [kenneth@loafman.com]

* Added b2sdk to snapcraft.yaml * Fixed bug #1850440 - Can't mix strings
and bytes. [kenneth@loafman.com]

* Updated snapcraft.yaml to remove python-lockfile and fix spelling. [kenneth@loafman.com]

* Updated snapcraft.yaml to remove rdiffdir and add libaft1 to stage. [kenneth@loafman.com]

* Updated snapcraft.yaml to include rdiffdir and did some reformatting. [kenneth@loafman.com]

* Updated snapcraft.yaml to include rdiffdir and did some reformatting. [kenneth@loafman.com]

* Removed file() call in swiftbackend.  It's been deprecated since py2. [kenneth@loafman.com]

* Revisited bug #1848783 - par2+webdav raises TypeError on Python 3   -
Fixed so bytes filenames were compared as unicode in re.match() [kenneth@loafman.com]

* Removed a couple of disables from pylint code test.   - E1103 - Maybe
has no member   - E0712 - Catching an exception which doesn't inherit
from BaseException. [kenneth@loafman.com]

* Added additional fsdecode's to uses of local\_path.name and
source\_path.name in b2backend's \_get() and \_put.  See bug
#1847885 for more details. [kenneth@loafman.com]

* Fixed bug #1849661 with patch from Graham Cobb   - The problem is that
b2backend uses 'quote\_plus' on the     destination URL without
specifying the 'safe' argument as     '/'. Note that 'quote' defaults
'safe' to '/', but     'quote\_plus' does not! [kenneth@loafman.com]

* Fixed bug #1848166 - Swift backend fails on string concat   - added
util.fsdecode() where needed. [kenneth@loafman.com]

* Fixed bug #1848783 with patch from Jacob Middag   - Don't use b''
strings in re.* [kenneth@loafman.com]

* Fixed bug #1848783 with patch from Jacob Middag   - Don't use b''
strings in re.* [kenneth@loafman.com]

* Fixed bug #1626061 with patch from Michael Apozyan   - While doing
multipart upload to s3 we need to report the     total size of
uploaded data, and not the size of each part     individually.  So we
need to keep track of all parts     uploaded so far and sum it up on
the fly. [kenneth@loafman.com]

* Removed revision 1480 until patch is validated. [kenneth@loafman.com]

* Fixed bug #1626061 with patch from Michael Apozyan   - While doing
multipart upload to s3 we need to report the     total size of
uploaded data, and not the size of each part     individually.  So we
need to keep track of all parts     uploaded so far and sum it up on
the fly. [kenneth@loafman.com]

* Fixed bug #1848203 with patch from Michael Apozyan   - convert to
integer division. [kenneth@loafman.com]

* Fix unadorned string. [kenneth@loafman.com]

* Fix unadorned string. [kenneth@loafman.com]

* Update changelogs. [Adam Jacobs]

* In version 1 of the B2sdk, the list\_file\_names method is removed
from the B2Bucket class. [Adam Jacobs]

    This change makes the b2 backend backwards-compatible with the old version 0 AND forward-compatible with the new version 1.

* Complete fix for string concatenation in b2 backend. [Adam Jacobs]

* Fixed Resouce warnings when using paramiko.  It turns out   that
duplicity's ssh\_paramiko\_backend.py was not handling   warning
suppression and ended up clearing all warnings,   including those that
default to off. [kenneth@loafman.com]

* Fixed Resouce warnings when using paramiko.  It turns out   that
duplicity's ssh\_paramiko\_backend.py was not handling   warning
suppression and ended up clearing all warnings,   including those that
default to off. [kenneth@loafman.com]

* Removed a setting in tox.ini that causes coverage to   be activated
during testing duplicity. [kenneth@loafman.com]

* Fixed bug #1846678 - --exclude-device-files and -other-filesystems
crashes   - assuming all options had arguments was fixed. [kenneth@loafman.com]

* Fixed bug #1844950 - ssh-pexpect backend syntax error   - put the
global before the import. [kenneth@loafman.com]

* Fixed bug #1846167 - webdavbackend.py: expected bytes-like object, not
str   - base64 now returns bytes where it used to be strings, so just
decode(). [kenneth@loafman.com]

* Fixed bug reported on maillist - Python error in Webdav backend.  See:
https://lists.nongnu.org/archive/html/duplicity-
talk/2019-09/msg00026.html. [kenneth@loafman.com]

* Fix bug #1844750 - RsyncBackend fails if used with multi-backend.   -
used patch provided by KDM to fix. [kenneth@loafman.com]

* Fix bug #1843995 - B2 fails on string concatenation.   - use
util.fsdecode() to get a string not bytes. [kenneth@loafman.com]

* Clean up some pylint warnings. [kenneth@loafman.com]

* Add testenv:coverage and took it out of defaults.  Some cleanup. [kenneth@loafman.com]

* Fix MacOS tempfile selection to avoid /tmp and /var/tmp.  See thread:
https://lists.nongnu.org/archive/html/duplicity-
talk/2019-09/msg00000.html. [kenneth@loafman.com]

* Sort of fix bugs #1836887 and #1836888 by skipping the   tests under
question when running on ppc64el machines. [kenneth@loafman.com]

* Added more python future includes to support using   python3 code
mixed with python2. [kenneth@loafman.com]

* Fix exc.args handling.  Sometimes it's (message, int),   other times
its (int, message).  We look for the   message and use that for the
exception report. [kenneth@loafman.com]

* Adjust exclusion list for rsync into duplicity\_test. [kenneth@loafman.com]

* Set to allow pydevd usage during tox testing. [kenneth@loafman.com]

* Don't add extra newline when building dist/relfiles.txt. [kenneth@loafman.com]

* Changed dist/makedist to fall back to dist/relfiles.txt   in case bzr
or git is not available to get files list.   Tox sdist needs setup.py
which needs dist/makedist. * Updatated LINGUAS file to add four new
translations. [kenneth@loafman.com]

* Made some changes to the Docker infrastructure:   - All scripts run
from any directory, assuming directory     structure remains the same.
- Changed from Docker's COPY internal command which is slow to
using external rsync which is faster and allows excludes.   - Removed
a couple of unused files. [kenneth@loafman.com]

* Run compilec.py for code tests, it needs the import. [kenneth@loafman.com]

* Simplify README-TESTING and change this to recommend using the Docker
images to test local branches in a known-good environment. [Aaron A Whitehouse]

* Convert Dockerfile-19.10 to new approach (using local folder instead
of remote repo) * run-tests passes on 19.10 Docker (clean: commands
succeeded; py27: commands succeeded; SKIPPED: py36:
InterpreterNotFound: python3.6; py37: commands succeeded; report:
commands succeeded) [Aaron A Whitehouse]

* Convert Dockerfile-19.04 to new approach (using local folder instead
of remote repo) * run-tests passes on 19.04 Docker (clean: commands
succeeded; py27: commands succeeded; SKIPPED:  py36:
InterpreterNotFound: python3.6;  py37: commands succeeded; report:
commands succeeded) [Aaron A Whitehouse]

* Edit Dockerfile-18.10 to use the local folder. * Tests all pass on
18.10 except for the same failures as trunk (4 failures on python 3.6:
TestUnicode.test\_unicode\_filelist;
TestUnicode.test\_unicode\_paths\_asterisks;
TestUnicode.test\_unicode\_paths\_non\_globbing;
TestUnicode.test\_unicode\_paths\_square\_brackets) [Aaron A Whitehouse]

* Use local folder instead of bzr revision, so remove the revision
arguments in the setup script. * Modify Dockerfile and
Dockerfile-18.04 to copy the local folder rather than the remote
repository. * Tests all pass on 18.04 except for the same failures as
trunk (4 failures on python 3.6: TestUnicode.test\_unicode\_filelist;
TestUnicode.test\_unicode\_paths\_asterisks;
TestUnicode.test\_unicode\_paths\_non\_globbing;
TestUnicode.test\_unicode\_paths\_square\_brackets) [Aaron A Whitehouse]

* Fix .bzrignore. [kenneth@loafman.com]

* Encode Azure backend file names. [Frank Fischer]

* Change README-TESTING to be correct for running individual tests now
that we have moved to Pytest. [Aaron A Whitehouse]

* Fix debian/rules file. [kenneth@loafman.com]

* Fix setup.py shebang. [kenneth@loafman.com]

* Fix debian/rules file. [kenneth@loafman.com]

* Fix debian/rules file. [kenneth@loafman.com]

* Fix debian/rules file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Ran futurize selectively filter-by-filter to find the ones that work. [kenneth@loafman.com]

* Fixed build on Launchpad for 0.8.x, so now there is a new PPA at
https://launchpad.net/\~duplicity-team/+archive/ubuntu/daily-dev-trunk. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Add snap package creation files * Modify dist/makedist to version the
snapcraft.yaml. [Aaron A Whitehouse]

* Remove a mess I made. [Kenneth Loafman]

* Fixed bug #1839886 with hint from denick   - Duplicity crashes when
using --file-prefix * Removed socket.settimeout from backend.py.   It
was already set in commandline.py. * Removed pycryptopp from README
requirements. [kenneth@loafman.com]

* Fixed bug #1839728 with info from Avleen Vig   - b2 backend requires
additional import. [kenneth@loafman.com]

* More changes to provide Python test coverage:   - Moved bulk of code
from bin/duplicity to     duplicity/dup\_main.py for coverage. * Fixed
some 2to3 issues in dup\_main.py * Fixed division differences with
futurize. [kenneth@loafman.com]

* More changes to provide Python test coverage:   - Moved bulk of code
from bin/duplicity to     duplicity/dup\_main.py for coverage. * Fixed
some 2to3 issues in dup\_main.py * Fixed division differences with
futurize. [kenneth@loafman.com]

* More changes to provide Python test coverage:   - Moved bulk of code
from bin/duplicity to     duplicity/dup\_main.py for coverage. * Fixed
some 2to3 issues in dup\_main.py. [kenneth@loafman.com]

* More changes to provide Python test coverage:   - Now covers
functional tests spawning duplicity   - Does not cover bin/duplicity
for some reason. [kenneth@loafman.com]

* Fixed bugs #1838427 and #1838702 with a fix   suggested by Stephen
Miller.  The fix was to   supply tarfile with a unicode grpid, not
bytes. [kenneth@loafman.com]

* Some changes to provide Python test coverage:   - Coverage runs with
every test cycle   - Does not cover functional tests that spawn
duplicity itself.  Next pass.   - After a run use 'coverage report
html' to see     an overview list and links to drill down.  It
shows up in htmlcov/index.html. [kenneth@loafman.com]

* Fix dist/makedist to run on python2/3. [kenneth@loafman.com]

* Fix dist/makedist to run on python3. [kenneth@loafman.com]

* Fix dist/makedist to run on python3. [kenneth@loafman.com]

* One last change for bug #1829416 from charlie4096. [kenneth@loafman.com]

* Enhanced build\_duplicity\_test.sh   - Use -h to get help and defaults
- Takes arguments for distro, revno, help   - Distros supported are
18.04, 18.10, 19.04, 19.10   - Revnos are passed to bzr -r option. [kenneth@loafman.com]

* Fix so Docker image duplicity\_test will update and pull   new bzr
revisions if changed since last build. [kenneth@loafman.com]

* Remove speedup in testing backup.  The math was correct,   but it's
failing on Docker and Launchpad testing. [kenneth@loafman.com]

* Move pytest-runner setup requirement to a test requirement. [Michael Terry]

* Removed python-gettext from setup.py.  Whoops! [kenneth@loafman.com]

* Optimize loading backup chains; reduce file\_naming.parse calls. [Matthew Glazar]

    For each filename in filename_list,
    CollectionsStatus.get_backup_chains calls file_naming.parse
    (through BackupSet.add_filename) between 0 and len(sets)*2
    times. In the worst case, this leads to a *ton* of redundant
    calls to file_naming.parse.

    For example, when running 'duplicity collection-status' on
    one of my backup directories:

    * filename_list contains 7545 files
    * get_backup_chains creates 2515 BackupSet-s
    * get_backup_chains calls file_naming.parse 12650450 times!

    This command took 9 minutes and 32 seconds. Similar
    commands, like no-op incremental backups, also take a long
    time. (The directory being backed up contains only 9 MiB
    across 30 files.)

    Avoid many redundant calls to file_naming.parse by hoisting
    the call outside the loop over BackupSet-s. This
    optimization makes 'duplicity collection-status' *20 times
    faster* for me (572 seconds -> 29 seconds).

    Aside from improving performance, this commit should not
    change behavior.

* Correct types for os.join in Dropbox backend. [Gwyn Ciesla]

* Fixed bug #1836829 progress.py: old\_div not defined   - also fixed
old\_div in \_boto\_multi.py. [kenneth@loafman.com]

* Fixed bug #1836829 progress.py: old\_div not defined   - also fixed
old\_div in \_boto\_multi.py. [kenneth@loafman.com]

* Remove python-gettext from requirements.txt.  Normal   Python
installation includes gettext. * Mod README to include Python 3.6 and
3.7. [kenneth@loafman.com]

* Comment out HSIBackendTest since shim is not up-to-date. [kenneth@loafman.com]

* Install python3.6 and 3.7 explicitly in Dockerfile.  Tox and Docker
now support testing Python 2,7, 3.6, and 3.7. [kenneth@loafman.com]

* Make sure test filenames are bytes not unicode. * Fix
test\_glob\_to\_regex to work on Python 3.7. [kenneth@loafman.com]

* Going back to original.  No portable way to ignore warning. [kenneth@loafman.com]

* Another unadorned string. [kenneth@loafman.com]

* Cleanup some trailing spaces/lines in Docker files. [kenneth@loafman.com]

* Fix so we start duplicity with the base python we run under. [kenneth@loafman.com]

* Adjust POTFILES.in for compilec.py move. [kenneth@loafman.com]

* Ensure \_librsync.so is regenned before toc testing. [kenneth@loafman.com]

* Add encoding to logging.FileHandler call to make log file utf8. [kenneth@loafman.com]

* Fix warning in \_librsync.c module. [kenneth@loafman.com]

* Fix some issues found by test\_code.py (try 2) [kenneth@loafman.com]

* Fix some issues found by test\_code.py. [kenneth@loafman.com]

* Fix reversed port assignments (FTP & SSH) in docker-compose.yml. [kenneth@loafman.com]

* Convert the docker duplicity\_test image to pull the local branch into
the container, rather than lp:duplicity. This allows the use of the
duplicity Docker testing containers to test local changes in a known-
good environment before they are merged into trunk. The equivalent of
the old behaviour can be achieved by starting with a clean branch from
lp:duplicity. * Expand Docker context to parent branch folder and use
-f in the docker build command to point to the Dockerfile. * Simplify
build-duplicity\_test.sh now that the whole folder is copied
(individual files no longer need to be copied) [Aaron A Whitehouse]

* Fix reimport problem where "from future.builtins" was being treated
the differently than "from builtins".  They are both the same, so
converted to shorter form "from builtins" and removed duplicates. [kenneth@loafman.com]

* Fix s3 backups by encoding remote filenames. [Michael Terry]

* Add 2to3 as a dependency to dockerfile. [Aaron A. Whitehouse]

* Add tzdata back in as a dependency and set
DEBIAN\_FRONTEND=noninteractive so no tzdata prompt. [Aaron A. Whitehouse]

* Set docker container locale to prevent UTF-8 errors. [Aaron A. Whitehouse]

* Change dockerfile to use 18.04 instead of 16.04 and other fixes. [Aaron A. Whitehouse]

* Fix s3 backups by importing the boto module. [Michael Terry]

* Normalize shebang to just python, no version number * Fix so most
testing/*.py files have the future suggested lines   - from
\_\_future\_\_ import print\_function     from future import
standard\_library     standard\_library.install\_aliases() [kenneth@loafman.com]

* Fixed failing test in testing/unit/test\_globmatch.py   - Someone is
messing with regex.  Fix same.   - See
https://bugs.python.org/issue29995 for details. [kenneth@loafman.com]

* Fixed bug #1833559 0.8 test fails with 'duplicity not found' errors
- Fixed assumption that duplicity/rdiffdir were in $PATH. [kenneth@loafman.com]

* Fixed bug #1833573 0.8.00 does not work on Python 2   - Fixed shebang
to use /usr/bin/python instead of python2. [kenneth@loafman.com]

* Fix some test\_code errors that slipped by. [kenneth@loafman.com]

* Fix Azure backend for python 3. [Frank Fischer]

    By definition, the list of keys from "list" is byte-formatted.
    As such we have to decode the parameter offered to "get"

* Fixed bug #1831178 sequence item 0: expected str instance, int found
- Simply converted int to str when making list. [kenneth@loafman.com]

* Fix some import conflicts with the "past" module   - Rename
collections.py to dup\_collections.py   - Remove all "from
future.utils import old\_div"   - Replace old\_div() with "//" (in
py27 for a while).   - All tests run for py3, unit tests run for py3.
The new     import fail is "from future import standard\_library" [kenneth@loafman.com]

* Spaces to tabs for makefile. [Kenneth Loafman]

* Change to python3 for build. [kenneth@loafman.com]

* Have uexc to always return a string. [Michael Terry]

    This fixes unhandled exception reporting

* Add requirements for python-gettext. [kenneth@loafman.com]

* Fix gio and pydrive backends to use fsdecode. [Michael Terry]

* Remove unnecessary sleeping after running backups in tests. [Matthew Glazar]

    ptyprocess' 'PtyProcess.close' function [1] closes the
    terminal, then terminates the process if it's still alive.
    Before checking if the process is alive, ptyprocess
    unconditionally sleeps for 100 milliseconds [2][3].

    In 'run_duplicity', after we call 'child.wait()', we know
    that the process is no longer alive. ptyprocess' 100 ms
    sleep just slows down tests. Tell ptyprocess to not sleep.

    [1] pexpect uses ptyprocess. 'PtyProcess.close' is called by
        'PtyProcess.__del__', so 'PtyProcess.close' is called
        when 'run_duplicity' returns.
    [1] https://github.com/pexpect/ptyprocess/blob/3931cd45db50ee8533b8b0fef424b8d75f7ba1c2/ptyprocess/ptyprocess.py#L403
    [2] https://github.com/pexpect/ptyprocess/blob/3931cd45db50ee8533b8b0fef424b8d75f7ba1c2/ptyprocess/ptyprocess.py#L173

* Minimize time spent sleeping between backups. [Matthew Glazar]

    During testing, if a backup completes at time 10:49:30.621,
    the next call to 'backup' sleeps to ensure the new backup
    has a different integer time stamp (10:49:31). Currently,
    'backup' sleeps for an entire second, even though the next
    integer time stamp is less than half a second away (0.379
    seconds). This extra sleeping causes tests to take longer
    than they need to.

    Make tests run faster by sleeping only enough to reach the
    next integer time stamp.

* Ensure all duplicity output is captured in tests. [Matthew Glazar]

    The loop in 'run_duplicity' which captures output has a race
    condition. If duplicity writes output then exits before
    'child.isalive()' is called, then 'run_duplicity' exits the
    loop before calling 'child.readline()'. This means that some
    output is not read into the 'lines' list.

    Fix this race condition by reading all output until EOF,
    then waiting for the child to exit.

* Fix TestGlobToRegex.test\_glob\_to\_regex for py3.6 and above   - see
https://bugs.python.org/issue29995 for details. [kenneth@loafman.com]

* Some more work on unadorned strings   - Fixed
test\_unadorned\_string\_literals to list all strings found   - Added
bin/duplicity and bin/rdiffdir to list of files tested   - All
unadorned strings have now been adorned. [kenneth@loafman.com]

* Fixed bug #1828662 with patch from Bas Hulsken   - string.split() had
been deprecated in 2, removed in 3.7. [kenneth@loafman.com]

* Setup.py: allow python 2.7 again. [Mike Gorse]

* Bug #1828869: update CollectionsStatus after sync. [Mike Gorse]

* Imap: python 3 fixes. [Mike Gorse]

* Sync: handle parsed filenames without start/end times. [Mike Gorse]

    Signatures set time, rather than start_time and end_time, so comparisons
    against the latter generate an exception on Python 3.

* More PEP 479 fixes. [Mike Gorse]

* Fix some unadorned strings. [kenneth@loafman.com]

* Fix some unadorned strings. [kenneth@loafman.com]

* Fix to allow >=2.7 or >=3.5. [kenneth@loafman.com]

* Fix to always compile \_librsync before testing. [kenneth@loafman.com]

* Manual merge of lp:\~yajo/duplicity/duplicity   - Support partial
metadata sync.   - Fixes bug #1823858 by letting the user to choose
partial syncing. Only the metadata for the target chain     will be
downloaded. If older (or newer) chains are encrypted with a different
passphrase, the user will     be able to restore to a given time by
supplying only the passphrase for the chain selected by     the
`--restore-time` option when using this new option.   - A side effect
is that using this flag reduces dramatically the sync time when moving
files from one to     another location, in cases where big amounts of
chains are found. [kenneth@loafman.com]

* Change to Python >= 3.5. [kenneth@loafman.com]

* Added documentation on how to use the new AWS S3 Glacier option. [Brandon Anderson]

* Fixed a typo in prior commit. [Brandon Anderson]

* Added support for AWS glacier storage class. [Brandon Anderson]

* Fix bug #1811114 with revised onedrivebackend.py from David Martin   -
Adapt to new Microsoft Graph API. [kenneth@loafman.com]

* Removed last mention of copy.com from man page with help from edso. [kenneth@loafman.com]

* Fix pylint style issues (over-indented text, whitespace on blank lines
etc) * Removed "pylint: disable=bad-string-format-type" comment, which
was throwing an error and does not seem to be needed. [Aaron A Whitehouse]

* Accomodate unicode input for uexc and add test for this. [Aaron A Whitehouse]

* Convert deprecated .message to args[0] [Aaron A Whitehouse]

* Add test case for lp:1770929 * Added fix (though using deprecated
.message syntax) [Aaron A Whitehouse]

* Attempt to port sx backend to python 3. [Mike Gorse]

    Untested, but likely needed changes similar to some other backends.

* Rsync: py3 fixes. [Mike Gorse]

* Ncftp: py3 fixes. [Mike Gorse]

* Test\_selection.py: fix an invalid escape sequence on py3. [Mike Gorse]

* Fix sync\_archive on python 3. [Mike Gorse]

    The recognized suffixes were being stored as unicode, but they were being
    compared against filenames that are stored as bytes, so the comparisons
    were failing.

* Ssh\_pexpect: py3 fixes. [Mike Gorse]

* Fixed bug #1817375 with hint from mgorse   - Added 'global pexpect' at
end of imports. [kenneth@loafman.com]

* Pydrive: delete temporary root file. [Michael Terry]

* \_\_unicode\_\_ -> \_\_str\_\_ [Mike Gorse]

* Fix a regex substitution on python 3. [Mike Gorse]

* Return temporary filenames as bytes. [Mike Gorse]

    We should be consistent in terms of the class used for filenames.
      Fixes warnings about forgetting unknown tempfiles.

* Modify some generators to return when finished. [Mike Gorse]

    Per PEP 479, the proper way to terminate a generator is to return, rather
    than throwing StopIteration.
    Fixes a traceback on Python 3 where RuntimeError is raised.

* Bug #1813214 was marked fixed in 0.7.13.  There were still a couple of
copy.com references remaining in the docs and web.  Got those nuked,
finally. [kenneth@loafman.com]

* Added s3 kms server side encryption support with kms-grants support. [vam]

* Putting option in man in alphabetical order + description improvement. [Marcin Okraszewski]

* Adds setting to specify Azure Blob standard storage tier. [Marcin Okraszewski]

* Fixed bug #1803896 with patch from slawekbunka   - Add \_\_enter\_\_
and \_\_exit\_\_ to B2ProgressListener. [Kenneth Loafman]

* Fix some punctuation. [kenneth@loafman.com]

* Fixed bug #1798206 and bug #1798504   * Made paramiko a global with
import during \_\_init\_\_ so it would     not be loaded unless
needed. [kenneth@loafman.com]

* Change WebDAV backend to not read/write files into memory, but stream
them from/to disk to/from the remote endpoint. [Maurus Cuelenaere]

* Tox: Target py3, rather than py36. [Mike Gorse]

    This should make tox accept versions of python 3 other than 3.6 (ie, 3.7).

* \_librsyncmodule.c: Use s in format parameters again under python 2. [Mike Gorse]

* Fix comment from last commit. [Mike Gorse]

* Compilec.py: work around conflict with collections.py vs. built-in
collections module. [Mike Gorse]

* First pass at a python 3 port. [Mike Gorse]

    Futurized, adjusted some string adornments, added py36 to tox, etc.

* Tox: pass LC\_CTYPE. [Mike Gorse]

    Without this, LC_CTYPE is unset in the test environment. If it is unset and
    LANG is also unset, then sys.getfilesystemencoding() will return "ascii" or
    something similar.

* Fixed but #1797797 with patch from Bas Hulsken   - use bytes instead
of unicode for '/' in filenames. [Kenneth Loafman]

* Run futurize --stage1 on rdiffdir. [Mike Gorse]

* Run futurize --stage1 on bin/duplicity. [Mike Gorse]

* Run futurize --stage1, and adjust so that tests still pass. [Mike Gorse]

* Adorn some remaining strings. [Mike Gorse]

* Fix error message on unmatched glob rules. [Quentin Santos]

* Fix required Python version in README. [Quentin Santos]

* Fixed bug #1795227 global name Dropbox is not defined   - Applied
patch from Pedro Gimeno to restore globals. [kenneth@loafman.com]

* Annotate more strings in duplicity/*.py. [Mike Gorse]

* Adorn strings in some duplicity/*.py files. Several files are still
tbd. [Mike Gorse]

* Unicode fixes. [Mike Gorse]

    All tests pass now

* Make files executable. [kenneth@loafman.com]

* Mark adorned all but one of testing/unit. [kenneth@loafman.com]

* Released some things without proper paperwork: * Adorned strings in
testing/, testing/functional/, and testing/unit * Added AUTHORS file
listing all copyright claimants in headers. [kenneth@loafman.com]

* Missed a couple.  Simple sort. [kenneth@loafman.com]

* Add AUTHORS file. [kenneth@loafman.com]

* Checkpoint: Fixing unadorned strings for testing/unit/*. [Kenneth Loafman]

* Fixed unadorned strings for testing/functional/*. [Kenneth Loafman]

* Fixed unadorned strings for testing/*. [Kenneth Loafman]

* Reverted back to rev 1317 and reimplemented revs 1319 to 1322. [kenneth@loafman.com]

* Reverted back to rev 1317 and reimplemented revs 1319 to 1322. [kenneth@loafman.com]

* Whoops, my bad!  Released before fully testing.  Reverting to rev 1317
and proceeding from there with unadorned string conversion. [kenneth@loafman.com]

* Move docs/conf.py to ignored.  Sphinx rewrites it. [kenneth@loafman.com]

* Fix a misspelling. [kenneth@loafman.com]

* Fix 2to3 error found with newer 2to3 module. [kenneth@loafman.com]

* Nuke remnants of copycom and acdcli backends * Regen docs. [kenneth@loafman.com]

* Fixed unadorned strings to unicode in duplicity/*/*   - Some fixup due
to shifting indenataion not matching PEP8.   - Substituted for non-
ascii char in jottlibbackend.py comment. [kenneth@loafman.com]

* Fixed unadorned strings to unicode in duplicity/backends/*   - Some
fixup due to shifting indenataion not matching PEP8. [kenneth@loafman.com]

* Fixed unadorned strings to unicode in duplicity/backends/*   - Some
fixup due to shifting indenataion not matching PEP8. [kenneth@loafman.com]

* Added function to fix unadorned strings
(testing/fix\_unadorned\_strings.py)   - Fixes by inserting 'u' before
token string   - Solves 99.9% of the use cases we have   - Fix
unadorned strings to unicode in bin/duplicity and bin/rdiffdir   - Add
import for \_\_future\_\_.print\_function to
find\_unadorned\_strings.py. [kenneth@loafman.com]

* Fix unadorned strings to unicode. [kenneth@loafman.com]

* Add gpg sockets to ignore list. [kenneth@loafman.com]

* Add fix\_unadorned\_strings.py to ignore list. [kenneth@loafman.com]

* Add function to fix unadorned strings by inserting 'u' before.
Solves 99.9% of the use cases we have. [kenneth@loafman.com]

* Add import for \_\_future\_\_.print\_function. [kenneth@loafman.com]

* Adorn globs in functional/test\_selection.py and
unit/test\_selection.py * Remove ignores for these files in
test\_code.py. [Aaron A Whitehouse]

* Remove selection.py exception from test\_code.py. [Aaron A Whitehouse]

* Adorn globs in selection.py. [Aaron A Whitehouse]

* Fixed bug #1780617 Test fail when GnuPG >= 2.2.8   - Relevant change
in GnuPG 2.2.8: https://dev.gnupg.org/T3981   - Added '--ignore-mdc-
error' to all gpg calls made. [kenneth@loafman.com]

* Add support for S3 One Zone - Infrequent Access storage class. [Excitable Snowball]

* Adorn strings in testing/unit/test\_globmatch.py. [Aaron A Whitehouse]

* Adorn string literals in duplicity/globmatch.py. [Aaron A Whitehouse]

* Added new script to find unadorned strings
(testing/find\_unadorned\_strings.py python\_file) which prints all
unadorned strings in a .py file. * Added a new test to test\_code.py
that checks across all files for unadorned strings and gives an error
if any are found (most files are in an ignore list at this stage, but
this will allow us to incrementally remove the exceptions as we adorn
the strings in each file). [Aaron A Whitehouse]

* Adorn string literals in test\_code.py with u/b * Add test for
unadorned string literals (currently only single file) [Aaron A Whitehouse]

* Tox changes to accommodate new pycodestyle version warnings. Ignored
W504 for now and marked as a TODO. Marked W503 as a permanent ignore,
as it is prefered to the (mutually exclusive) W504 under PEP8. *
Marked various regex strings as raw strings to avoid the new W605
"invalid escape sequence". [Aaron A Whitehouse]

* Fixed bug #x1717935 with suggestion from strainu   - Use
urllib.quote\_plus() to properly quote pathnames passed via URL. [kenneth@loafman.com]

* Fixed bug #1768954 with patch from Max Hallden   - Add
AZURE\_ENDPOINT\_SUFFIX environ variable to allow setting to non-U.S.
servers. [kenneth@loafman.com]

* Only check decryptable remote manifests   - fixup of revision 1252
which introduces a non-fatal error message (see #1729796)   - for
backups the GPG private key and/or it's password are typically not
available   - also avoid interactive password queries through e.g. gpg
agent. [Martin Nowak]

* Check last manifest only with prev. backup. [Martin Nowak]

* Mass update of po files from launchpad translations. [kenneth@loafman.com]

* Avoid redundant replication of already present backup sets - Add back
BackupSet.\_\_eq\_\_ which was accidentally removed in 1251. [Martin Nowak]

* Reduce dependencies on backend libraries   - Moved backend imports
into backend class \_\_init\_\_ method   - Surrounded imports with
try/except to allow better errors   - Put all library dependencies in
requirements.txt. [kenneth@loafman.com]

* Make backend.tobytes use util.fsencode rather than reimplementing. [Aaron A Whitehouse]

* Fixes so pylint 1.8.1 does not complain about missing conditional
imports.   - Fix dpbxbackend so that imports require instantiation of
the class.   - Added pylint: disable=import-error to a couple of
conditional imports. [kenneth@loafman.com]

* Change util.fsdecode to use "replace" instead of "ignore" (matching
behaviour of util.ufn) * Replace all uses of ufn with fsdecode. [Aaron A Whitehouse]

* Update docs. [kenneth@loafman.com]

* More pytest changes   - Use requirements.txt for dependencies   - Run
unit tests first, then functional   - Some general cleanup. [kenneth@loafman.com]

* More pytest changes   - Use requirements.txt for dependencies   - Run
unit tests first, then functional   - Some general cleanup. [kenneth@loafman.com]

* Converted to use pytest instead of unittest (setup.py test is now
discouraged)   - We use @pytest.mark.nocapture to mark the tests (gpg)
that require     no capture of file streams (currently 10 tests).   -
The rest of the tests are run normally. [kenneth@loafman.com]

* Remove precise-lpbuild.  EOL as of April 28, 1917. [kenneth@loafman.com]

* Remove unused import. [kenneth@loafman.com]

* First cut converting to pytest.   - 'setup.py test' now uses pytest.
We still use tox for     correct virtualenv setup.  All seem to be
current best     practices since 'setup.py test' use is discouraged.
- Global --capture=no option to allow gpg tests to complete
successfully.  Future should only turn off capture to the     gpg
tests themselves.  Creates a still messy output. [kenneth@loafman.com]

* Replace util.ufn(path.name) with path.uc\_name throughout. [Aaron A Whitehouse]

* Various code tidy-ups pre submitting for merge. None should change
behaviour. [Aaron A Whitehouse]

* Change fsdecode to use globals.fsencoding * Add 'ANSI\_X3.4-1968' to
the list of fsencodings that globals.fsencode treats as probably UTF-8. [Aaron A Whitehouse]

* Specify debian dependency too. [Michael Terry]

* Specify future requirement. [Michael Terry]

* Fix PEP8 issues. [Kenneth Loafman]

* Dpbxbackend: fix small files upload (API change) [Eugene Crosser]

    Dropbox file upload API for small files (that do not requre chunking)
    changed as described here:

    https://github.com/dropbox/dropbox-sdk-python/releases/tag/v7.1.0

    Now a data blob needs to be passed to the API instead of a file object.

* Dpbxbackend: check for specific API error for missing folder. [crosser@average.org]

* The "new" Dropbox API for directory listing raises an exception when
the directory is empty (and duplicity directory will be empty on the
first run). We actually want and empty list of files if the list of
files is emtpy. So catch the ListFolderError and continue. [crosser@average.org]

* The "new" Dropbox OAuth API return objects rather than tuples. Adjust
auth flow to that. [Eugene Crosser]

* More fixes for Unicode handling   - Default to 'utf-8' if
sys.getfilesystemencoding() returns 'ascii' or None   - Fixed bug
#1386373 with suggestion from Eugene Morozov. [kenneth@loafman.com]

* Fixed bug #1733057 AttributeError: 'GPGError' object has no attribute
'decode'   - Replaced call to util.ufn() with call to util.uexc().
Stupid typo! [kenneth@loafman.com]

* Fix attribution for patch of 1448094 to Wolfgang Rohdewald. [kenneth@loafman.com]

* Remove non-UTF8 filename from testfiles.tar.gz. [Kenneth Loafman]

* Fixed bug #1730902 GPG Error Handling   - use util.ufn() not str() to
handle encoding. [kenneth@loafman.com]

* Fixed bug #1723890 with patch from Killian Lackhove   - Fixes error
handling in pydrivebackend.py. [kenneth@loafman.com]

* Fixed bug #1720159 - Cannot allocate memory with large manifest file
since 0.7.03   - filelist is not read if --file-changed option in
collection-status not present   - This will keep memory usage lower in
non collection-status operations. [kenneth@loafman.com]

* Fix PEP8 issues in b2backend.py. [kenneth@loafman.com]

* Fixed bug #1724144 "--gpg-options unused with some commands"   - Add
--gpg-options to get version run command. [kenneth@loafman.com]

* Fixed bug #1448094 with patch from Tomáš Zvala   - Don't log
incremental deletes for chains that have no incrementals. [kenneth@loafman.com]

* Fixed bug #1654756 with new b2backend.py module from Vincent Rouille
- Faster (big files are uploaded in chunks)   - Added upload progress
reporting support. [kenneth@loafman.com]

* Patched in lp:\~mterry/duplicity/rename-dep   - Make rename command a
dependency for LP build. [kenneth@loafman.com]

* Remove conditional pexpect in testing/functional/\_\_init\_\_.py --
while the commented-out text is the nicer approach in versions after
pexpect 4.0, we need to support earlier versions at this stage and a
single code path is simpler. [Aaron A Whitehouse]

* Fixed bug #1714663 "Volume signed by XXXXXXXXXXXXXXXX, not XXXXXXXX"
- Normalized comparison length to min length of compared keys before
comparison   - Avoids comparing mix of short, long, or fingerprint
size keys. [kenneth@loafman.com]

* Fix PEP8 issues. [kenneth@loafman.com]

* Fixed bug #1715650 with patch from Mattheww S   - Fix to make
duplicity attempt a get first, then create, a container     in order
to support container ACLs. [Kenneth Loafman]

* More fixes to backend.py plus some cleanup. [Kenneth Loafman]

* Fix backend.py to allow string, list, and tuple types to support
megabackend.py. [Kenneth Loafman]

* Fix some unicode decode errors around exceptions. [Michael Terry]

* Fixed bug introduced in new megabackend.py where
process\_commandline()   takes a string not a list.  Now it takes
both. * Updated web page for new megabackend requirements. [Kenneth Loafman]

* Fixed bug #1638033 Remove leading slash on --file-to-restore   - code
already used rstrip('/') so change to just strip('/') [Kenneth Loafman]

* 2017-08-31  Kenneth Loafman  <kenneth@loafman.com> [Kenneth Loafman]

    Fixed bug #1538333 Assertion error in manifest.py: assert filecount == ...
          - Made sure to never pass .part files as true manifest files
          - Changed assert to log.Error to warn about truncated/corrupt filelist
          - Added unit test to make sure detection works
          - Note: while this condition is serious, it will not affect the basic backup and restore
            functions.  Interactive options like --list-files-changed and --file-changed will not
            work correctly for this backup set, so it is advised to run a full backup as soon as
            possible after this error occurs.
        * Fixed bug #1638033 Remove leading slash on --file-to-restore
          - code already used rstrip('/') so change to just strip('/')

* Fixed bug #1394386 with new module megabackend.py from Tomas Vondra
- uses megatools from https://megatools.megous.com/ instead of mega.py
library     which has been deprecated   - fixed copyright and PEP8
issues   - replaced subprocess.call() with self.subprocess\_popen() to
standardize. [Kenneth Loafman]

* Fixed bug #1394386 with new module megabackend.py from Tomas Vondra
- uses megatools from https://megatools.megous.com/ instead of mega.py
library     which has been deprecated   - fixed copyright and PEP8
issues. [Kenneth Loafman]

* Support gpg versions with -tag suffixes. [Michael Terry]

* Fix errors where log.Warn was invoked with log.warn in
webdavbackend.py. [ken]

* Gio: be slightly more correct and get child GFiles based on display
name. [Michael Terry]

* Fixed PEP8 errors in bin/duplicity. [Kenneth Loafman]

* Fixed bug #1709047 with suggestion from Gary Hasson   * fixed so
default was to use original filename. [Kenneth Loafman]

* Giobackend: handle a wider variety of gio backends by making less
assumptions; in particular, this fixes the google-drive: backend. [Michael Terry]

* Fixed encrypted remote manifest handling to merely put out a non-fatal
error message and continue if the private key is not available. [Kenneth Loafman]

* Fixed slowness in 'collection-status' by basing the status on the
remote system only.  The local cache is treated as empty. [Kenneth Loafman]

* Fix text of last change. [Kenneth Loafman]

* Collection-status should not sync metadata - up-to-date local metadata
is not needed as collection-status is generated from remote file list
- syncing metadata might require to download several GBs. [Martin Nowak]

* Fixed problem in dist/makedist when building on Mac where AppleDouble
files were being created in the tarball.  See:
https://superuser.com/questions/61185/why-do-i-get-files-like-foo-in-
my-tarball-on-os-x. [Kenneth Loafman]

* Merged in lp:\~xlucas/duplicity/swift-multibackend-bug   - Fix a bug
when swift backend is used in a multibackend configuration. [Kenneth Loafman]

* Copy.com is gone so remove copycombackend.py. [Kenneth Loafman]

* Fixed bug #1265765 with patches from Matthias Larisch and Edgar Soldin
- SSH Paramiko backend now uses BufferedFile implementation to enable
collecting the entire list of files on the backend. [Kenneth Loafman]

* Fix bug #1672540 with patch from Benoit Nadeau   - Rename would fail
to move par files when moving across filesystems.   - Patch uses
shutil.move() to do the rename instead. [Kenneth Loafman]

* Some changes ported 0.7 to/from 0.8 to keep up-to-date. [Kenneth Loafman]

* Revisited bug #670891 with patch from Edgar Soldin   - Forced
librsync.PatchedFile() to extract file object from TemporaryFile()
object when on Windows or Cygwin systems.  This allows us to avoid the
problem of tmpfile() use which creates temp files in the wrong place.
- See discussion at https://bugs.launchpad.net/duplicity/+bug/670891. [Kenneth Loafman]

* May have finally fixed bug #1556553, "Too many open files...".   -
Applied patch from Howard Kaye, question #631423.  The fix is to dup
the file descriptor, and then close the file in the deallocator
routine in the glue code. Duping the file lets the C code and the
Python     code each close the file when they are done with it.   -
Invalidated and removed the fix put in for bug #1320832.   - Caveat:
long incremental chains will still eat up a large number of file
descriptors.  It's a very risky practice, so I'm not inclined to fix
it. [Kenneth Loafman]

* Remove run-tests-ve - not needed * move stdin\_test.sh to manual dir. [Kenneth Loafman]

* Fix comments on ignored pylint messages. [Kenneth Loafman]

* Remove precise-lpbuild test since precise is EOL. [Kenneth Loafman]

* Adjust control for LP build process, fasteners not lockfile. [Kenneth Loafman]

* Fixed bug #1320641 and others regarding lockfile   - swap from
lockfile to fasteners module   - use an fcntl() style lock for process
lock of duplicity cache   - lockfile will now clear if duplicity is
killed or crashes. [Kenneth Loafman]

* Fixed bug #1689632 with patch from Howard Kaye   - On MacOS, the
tempfile.TemporaryFile call erroneously raises an     IOError
exception saying that too many files are open. This causes
restores to fail randomly, after thousands of files have been
restored. [Kenneth Loafman]

* Fixed bug #1320832 with suggestion from Oskar Wycislak   - Use chunks
instead of reading it all in swiftbackend. [Kenneth Loafman]

* Quick fix for bug #1680682 and gnupg v1, add missing comma. [ken]

* Fixed bug #1684312 with suggestion from Wade Rossman   - Use
shutil.copyfile instead of os.system('cp ...')   - Should reduce
overhead of os.system() memory usage. [Kenneth Loafman]

* Fixed bug #1680682 with patch supplied from Dave Allan   - Only
specify --pinentry-mode=loopback when --use-agent is not specified *
Fixed man page that had 'cancel' instead of 'loopback' for pinentry
mode. [Kenneth Loafman]

* Add some commented-out debug print and move under error condition. [Kenneth Loafman]

* Fixed bug #1668750 - Don't mask backend errors   - added exception
prints to module import errors. [Kenneth Loafman]

* Fixed bug #1671852 - Code regression caused by revision 1108   -
change util.uexc() back to bare uexc() [Kenneth Loafman]

* Fixed bug #1367675 - IMAP Backend does not work with Yahoo server   -
added the split() as needed in 'nums=list[0].strip().split(" ")'   -
the other fixes mentioned in the bug report comments were already done. [Kenneth Loafman]

* Some fixes to gpg.py to handle gpg1 & gpg2 & gpg2.1 commandline issues
- --gpg-agent is optional on gpg1, but on gpg2 it is used
automatically   - --pinentry-mode is not a valid opt until gpg2.1, so
condition on that. [Kenneth Loafman]

* Fixed the documentation of --use-agent in the man page. [Martin Wilck]

* Fixed bug #1657916 with patch supplied by Daniel Harvey   - B2
provider cannot handle two backups in the same bucket. [Kenneth Loafman]

* Add detail about import exceptions in onedrivebackend.py. [ken]

* Merged in lp:\~matthew-t-bentley/duplicity/duplicity   - Sets a user
agent. Backblaze asked for this in case there are errors that
originate     from the Duplicity B2 backend   - Only retrieves a new
upload URL when the current one expires, to bring it in line     with
their best practices for integrations:
https://www.backblaze.com/b2/docs/integration\_checklist.html. [Kenneth Loafman]

* Fixed bug #1658283 "Duplicity 0.7.11 broken with GnuPG 2.0"   - Made
gpg version check more robust than just major version   - Now use
--pinentry-mode=loopback on gpg 2.1 and greater   - Removed check for
non-Linux systems, a false problem. [Kenneth Loafman]

* Fixed bug #1655268 "--gpg-binary option not working"   - If gpg binary
is specified rebuild gpg profile using new binary location. [Kenneth Loafman]

* Fixed bug #1654220 with patch supplied by Kenneth Newwood   -
Duplicity fails on MacOS because GPG version parsing fails. [Kenneth Loafman]

* Fixed bug #1623342 with patch supplied by Daniel Jakots   - Failing
test on OpenBSD because tar/gtar not found. [Kenneth Loafman]

* Merged in lp:\~breunigs/duplicity/amazondrive3   - As reported on the
mailinglist, if a space is entered while duplicity asks for the URL,
it fails.     Since all important spaces are URL encoded anyway, this
should be fine even if there are spaces in     the URL at all. I also
patched it in the onedrive backend, because it must have similar
issues. [Kenneth Loafman]

* Fix Bug #1642813 with patch from Ravi   - If stat() returns None,
don't attempt to set perms. [Kenneth Loafman]

* Fix problem with gpg2 in yakety and zesty. [ken]

* Some fixes for MAC where gpg2 does not implement --pinentry-mode. [Kenneth Loafman]

* Skip locked folders tests if not on Linux platform. [Kenneth Loafman]

* Added tests to ensure behaviour is as expected for expressions
containing globs, as these traverse a different code path. [Aaron A Whitehouse]

* Fixed Bug #1624725, so that an include glob ending in "/" now includes
folder contents (for globs with and without special characters) [Aaron A Whitehouse]

* Added inline comment to globmatch.py explaining glob matching. *
Removed trailing / from Path() unittests, as paths used in duplicity
do not normally have these, even if they are folders. * Added unit
test to show files within a matched folder are included without a
trailing slash. * Fixed return value of
test\_slash\_star\_scans\_folder unittest from include to scan. [Aaron A Whitehouse]

* Add unittests and code comments to explain glob processing/regex
behaviour. [Aaron A Whitehouse]

* Add more tests for trailing slash behaviour. [Aaron A Whitehouse]

* Added (failing) test to show behaviour in Bug #1624725. [Aaron A Whitehouse]

* Temp fix for tempfile.TemporaryFile failures. [Kenneth Loafman]

* Fix encryption tests by specifying long key instead of short. [Kenneth Loafman]

* Merged in lp:\~horgh/duplicity/copy-symlink-targets-721599   - Add
--copy-links to copy symlink contents, not just the link itself. [Kenneth Loafman]

* Fix html output via rman. [ed.so]

* Merged in lp:\~dernils/duplicity/robust-dropbox-backend   - Added new
command line option --backend-retry-delay     that allows to determine
the time that duplicity sleeps     before retrying after an error has
occured.   - Added some robustness to dpbxbackend.py that ensures re-
authentication     happens in case that a socket is changed (e.g. due
to a forced reconnect     of a dynamic internet connection). [Kenneth Loafman]

* Revert to rev 1246. [Kenneth Loafman]

* Minor fix in manpage. [DerNils]

* Added --backend-retry-delay to the manpage. [DerNils]

* Added new command line option --backend-retry-delay. [DerNils]

* Added some robustness to dpbxbackend.py. [DerNils]

* Revert to rev 1246. [Kenneth Loafman]

* Merged in lp:\~dernils/duplicity/robust-dropbox-backend   - Added new
command line option --backend-retry-delay     that allows to determine
the time that duplicity sleeps     before retrying after an error has
occured.   - Added some robustness to dpbxbackend.py that ensures re-
authentication     happens in case that a socket is changed (e.g. due
to a forced reconnect     of a dynamic internet connection). [Kenneth Loafman]

* Merged in lp:\~dernils/duplicity/robust-dropbox-backend   - Added new
command line option --backend-retry-delay     that allows to determine
the time that duplicity sleeps     before retrying after an error has
occured.   - Added some robustness to dpbxbackend.py that ensures re-
authentication     happens in case that a socket is changed (e.g. due
to a forced reconnect     of a dynamic internet connection). [Kenneth Loafman]

* Fix bug using 40-char sign keys, from Richard McGraw on mail list   -
Remove truncation of argument and adjust comments. [Kenneth Loafman]

* Fixed bug #1642098 - does not create PAR2 archives when '--
par2-options' is used   - Missing space between par2-options plus
default options. [ken]

* Fixed bug #1621194 with code from Tornhoof   - Do backup to google
drive working without a service account. [Kenneth Loafman]

* Merged in lp:\~mwilck/duplicity/duplicity   - GPG: enable truly non-
interactive operation with gpg2   - This patch fixes the IMO
unexpected behavior that, when using GnuPG2, a pass phrase dialog
always pops up for     saving backups. This is particularly annoying
when trying to do unattended / fully automatic backups. [ken]

* GPG: enable truly non-interactive operation with gpg2. [Martin Wilck]

    GPG always tries to grab a passphrase from the gpg agent, even
    if is run with "--batch --no-tty" (as enforced by the
    meta_interactive = 0 setting of gpginterface.py).

    Sometimes this behavior is not intended. I would like to be able
    to run a backup job truly interactively. This would be possible,
    but duplicity's check_manifests() function calls gpg to compare
    the remote (encrypted) and local manifest, which, with gpg2,
    will pop up the gpg agent pinentry every time I try to save backup
    (with gpg1, duplicity will just give up on the verification).

    I found that it's possible to force gpg2 to behave like gpg1 by
    using the command line option "--pinentry-mode=cancel". My patch
    applies this option if duplicity's "--use-agent" option is unset.

    Now, even with gpg2, backups can be saved without any passphrase
    dialog, at the cost of not being able to verify the manifests. Users
    who want the verification would just need to use "--use-agent", as
    with gpg1.

    For restore, this change has no effect, as duplicity will ask for the
    passphrase anyway if "--use-agent" is not specirfied.

* Fixed bug #1623342 with patch from Daniel Jakots   - failing test on
OpenBSD because tar/gtar not found. [Kenneth Loafman]

* Fixed bug #1620085: OSError when using --exclude-if-present with a
locked directory in backup path. * Added tests for errors on locked
files. [Aaron A Whitehouse]

* Add functional tests for --exclude-if-present. [Aaron A Whitehouse]

* Move and rename second TestTrailingSlash block to TestTrailingSlash2. [Aaron A Whitehouse]

* Merged in lp:\~mstoll-de/duplicity/duplicity   - Backblaze announced a
new domain for the b2 api. [Kenneth Loafman]

* Fixed bugs #815510 and #1615480   - Changed default --volsize to 200MB. [Kenneth Loafman]

* Merged in lp:\~fenisilius/duplicity/acd\_init\_mkdir   - Allow
duplicity to create remote folder. [Kenneth Loafman]

* Whoops, committed too much! [Kenneth Loafman]

* Fixed conflict in merge from Martin Wilck and applied   -
https://code.launchpad.net/\~mwilck/duplicity/0.7-series/+merge/301492
- merge fixes setsid usage in functional testing. [ken]

* Remove -w from setsid in functional tests. [ken]

* Fix unit test failures for {Old,Short}FilenamesFinalTest. [Martin Wilck]

    These unit test fail because of the following tricky series of events:

    1. duplicity is started with setsid(1). The setsid process forks duplicity
       and terminates
    2. duplicity prints a warning about depracated option (--old-filenames,
       --short-filenames) before asking for the passphrase. This causes pexpect
       to call os.waitpid(self.pid) but self.pid is the PID of the setsid(1)
       process which has already terminated.
    3. pexpect quits the expect loop for the passphrase with EOF.

    The problem can be solved by using the -w flag for sedsid (wait for child),
    so that the setsid process won't exit before duplicity itself.

* Fix failures of unit tests with --hidden-encrypt-key. [Martin Wilck]

    On distributions that don't have genuine gpg 1.x any more (gpg is a symlink
    to gpg2), such as OpenSUSE Factory, the tests with --hidden-encrypt-key fail
    without the gpg option --try-all-secrets.

    Not even that will help for gpg2 2.1.13 which has a bug preventing
    --try-all-secrets from working correctly
    (https://bugs.gnupg.org/gnupg/issue1985).

* Selection.py: use closure for matching paths with glob expressions. [Martin Wilck]

    (merged from lp:~mwilck/duplicity/duplicity)

    Glob matching in current duplicity uses a selector function that calls path_matches_glob(). This means that whenever a filename is matched, path_matches_glob() goes through the process of transforming a glob expression into regular expressions for filename and directory matching.

    My proposed patches create a closure function instead that uses precalculated regular expressions; the regular expressions are thus constructed only once at initialization time.

    This change speeds up duplicity a *lot* when complex include/exclude lists are in use: for my use case (dry-run, backup of an SSD filesystem), the speedup is a factor of 25 (runtime: 4s rather than 90s).

* Fixed PEP8 and 2to3 issues. [Kenneth Loafman]

* Add support for OVH Public Cloud Archive backend. [Xavier Lucas]

* Support prefix affinity in multibackend. [Xavier Lucas]

* Add integration test for newly added replicate command. [Martin Nowak]

    - also see https://code.launchpad.net/~dawgfoto/duplicity/replicate/+merge/322836

* Fixed problem in dist/makedist when building on Mac where AppleDouble
files were being created in the tarball.  See:
https://superuser.com/questions/61185/why-do-i-get-files-like-foo-in-
my-tarball-on-os-x. [Kenneth Loafman]

* Remove util.bytes\_to\_uc (as either .decode or fsdecode is
preferable). * Move unicode conversion for select options from
selection.py to commandline.py. [Aaron A Whitehouse]

* Replace util.py functions to and from unicode with direct calls to
.encode and .decode, as it did not save much code, means the
"strict"/"ignore"/"replace" decision can be made per call. Also helps
narrow down on why sys.getfilesystemencoding() is not working as
expected in some places. [Aaron A Whitehouse]

* Merge remaining file from trunk. Tests pass. [Aaron A Whitehouse]

* Merged in lp:\~xlucas/duplicity/swift-multibackend-bug   - Fix a bug
when swift backend is used in a multibackend configuration. [Kenneth Loafman]

* Copy.com is gone so remove copycombackend.py. [Kenneth Loafman]

* Fixed bug #1265765 with patches from Matthias Larisch and Edgar Soldin
- SSH Paramiko backend now uses BufferedFile implementation to enable
collecting the entire list of files on the backend. [Kenneth Loafman]

* Added capability to mount user workspace for testing local code. [Kenneth Loafman]

* Added variable substitution to docker-compose.yml   - .env file
contains first 24 bits of subnet addr * Added teardown.sh as
completion of setup.sh. [Kenneth Loafman]

* Fix bin/duplicity.1 entries for --verify and --compare-data. [Aaron A Whitehouse]

* Test infrastructure now using docker-compose. [DerNils]

* Fix bug #1672540 with patch from Benoit Nadeau   - Rename would fail
to move par files when moving across filesystems.   - Patch uses
shutil.move() to do the rename instead. [Kenneth Loafman]

* Some changes ported 0.7 to/from 0.8 to keep up-to-date. [Kenneth Loafman]

* Revisited bug #670891 with patch from Edgar Soldin   - Forced
librsync.PatchedFile() to extract file object from TemporaryFile()
object when on Windows or Cygwin systems.  This allows us to avoid the
problem of tmpfile() use which creates temp files in the wrong place.
- See discussion at https://bugs.launchpad.net/duplicity/+bug/670891. [Kenneth Loafman]

* Fix spurious warning message, return value not needed. [Kenneth Loafman]

* Checkpoint - docker testbed mostly running   - lots of format changes
in setup.sh   - made sure to kill off network and restart   -
simplified container naming and killall process   - most tests run now
with tox, 5 fail. [Kenneth Loafman]

* Go back to original requirements file. [Kenneth Loafman]

* May have finally fixed bug #1556553, "Too many open files...".   -
Applied patch from Howard Kaye, question #631423.  The fix is to dup
the file descriptor, and then close the file in the deallocator
routine in the glue code. Duping the file lets the C code and the
Python     code each close the file when they are done with it.   -
Invalidated and removed the fix put in for bug #1320832.   - Caveat:
long incremental chains will still eat up a large number of file
descriptors.  It's a very risky practice, so I'm not inclined to fix
it. [Kenneth Loafman]

* Fix spelling and rearrange some. [Kenneth Loafman]

* Added lpbuild-trusty to replace lpbuild-precise pre Aaron Whitehouse's
comment that there was a bug in pexpect < 3.4 that affects us. [Kenneth Loafman]

* Minor changes to setup.sh. [DerNils]

* Minor fix to setup.sh. [DerNils]

* Added more test infrastructure. [DerNils]

* Support for Swift storage policies. [Xavier Lucas]

* Changes needed to run-tests without pylint E0401(import-error) errors. [Aaron A Whitehouse]

* Move stdin\_test.sh to manual dir. [Kenneth Loafman]

* Precise is EOL so drop testing for it. [Kenneth Loafman]

* Adjust control for LP build process, fasteners not lockfile. [Kenneth Loafman]

* Fixed bug #1320641 and others regarding lockfile   - swap from
lockfile to fasteners module   - use an fcntl() style lock for process
lock of duplicity cache   - lockfile will now clear if duplicity is
killed or crashes. [Kenneth Loafman]

* Fixed bug #1689632 with patch from Howard Kaye   - On MacOS, the
tempfile.TemporaryFile call erroneously raises an     IOError
exception saying that too many files are open. This causes
restores to fail randomly, after thousands of files have been
restored. [Kenneth Loafman]

* Moved some things around in testing/infrastructure to clean up. [Kenneth Loafman]

* Moved Dockerfile for duplicitytest into
testinfrastructure/duplicity\_test. [Kenneth Loafman]

* Added furhter files for test infrastructure. [DerNils]

* Fixed bug #1320832 with suggestion from Oskar Wycislak   - Use chunks
instead of reading it all in swiftbackend. [Kenneth Loafman]

* Added ftp client to Dockerfile. [DerNils]

* Updated Dockerfile. [DerNils]

* Remove unnecessary unicode conversion on commandline.py filelist
append. * Tests all pass (and in previous commit). [Aaron A Whitehouse]

* Use unicode version of pexpect.spawn for version >= 4.0, but bytes
version below this. [Aaron A Whitehouse]

* Bzr does not honor perms so fix the perms at the start of the testing
and   avoid annoying error regarding testing/gnupg having too lenient
perms. [Kenneth Loafman]

* Replace incoming non-ASCII chars in commandline.py. [Kenneth Loafman]

* Merged in lp:\~marix/duplicity/add-azure-arguments   - Using the Azure
backend to store large amounts of data we found that     performance
is sub-optimal. The changes on this branch add command line
parameters to fine-tune some parameters of the Azure storage library,
allowing to push write performance towards Azure above 1 Gb/s for
large     back-ups. If a user does not provide the parameters the
defaults of the     Azure storage library will continue to be used. [Kenneth Loafman]

* Add command line arguments to fine-tune the Azure backend. [Bjoern Meier]

    Using the default values for internal block sizes and connection
    numbers works well for small back-ups, but provides suboptimal
    performance for larger ones.

* Delete tempfiles as soon as possible. [Martin Nowak]

* Add replicate command - useful to replicate/archive backups to another
backend - allows to partially replicate only older backup sets -
checks existing backup sets on target to avoid redundant copies. [Martin Nowak]

* We need tzdata (timezone data). [ken]

* You need tox to run tox.  Doh! [ken]

* Add libffi-dev back.  My bad. [ken]

* Fixed tox.ini. [DerNils]

* Separated pip requirements into duplicity and testing. [DerNils]

* Separated pip requirements into duplicity and testing. [DerNils]

* Remove dependencies we did not need. [ken]

* Add test user and swap to non-priviledged. [ken]

* Move branch duplicity up the food chain. [ken]

* Simplify Dockerfile per https://docs.docker.com/engine/userguide/eng-
image/dockerfile\_best-practices/ - Add a .dockerignore file -
Uncomment some debug prints - quick fix for bug #1680682 and gnupg v1,
add missing comma. [ken]

* Quick fix for bug #1680682 and gnupg v1, add missing comma. [ken]

* A little reorg, just keeping pip things together. [ken]

* More changes for testing: - keep gpg1 version for future testing -
some changes for debugging functional tests - add gpg-agent.conf with
allow-loopback-pinentry. [Kenneth Loafman]

* Edited Dockerfile. [DerNils]

* Whoops, deleted too much.  Add rdiff again. [Kenneth Loafman]

* Move pep8 and pylint to requirements. [Kenneth Loafman]

* Add rdiff install and newline at end of file. [ken]

* Edited requirements.txt, minor changes to README-REPO and README-
TESTING. [DerNils]

* Added README-TESTING, removed hmtlcov folder. [DerNils]

* Edited requirements.txt. [DerNils]

* Cleaned test cases. [DerNils]

* Added Dockerfile. [DerNils]

* Updated requirements.txt. [DerNils]

* Updated requirements.txt. [DerNils]

* Updated requirements.txt. [DerNils]

* Working on dpbx backend tests§ [DerNils]

* Working on the READMEs. [DerNils]

* Worked on the requirements and README. [DerNils]

* Added some experiences to the README. [DerNils]

* Make all tests pass on py27 tox environment. * lpbuildd-precise tests
still fail because the outdated pexpect (2.4) has issues with unicode
(pexpect.spawn does not support unicode and spawnu.readline fails). [Aaron A Whitehouse]

* Unit/test\_globmatch.py, unit/test\_selection.py,
functional/test\_selection.py tests all pass. * Assume UTF-8 encoding
for filelists (which also allows ASCII encoding). * Use new io module
for selection filelist access. * Create new path.uc\_name that is a
unicode version of the path, which is then used throughout the
selection code for path name matching etc. * Move selection.py to
using unicode strings and uc\_name versions of paths. * Made
functional/\_\_init\_\_.py use unicode arguments to run duplicity for
tests. * Use new io module in functional/test\_selection.py. * Remove
@unittest.expectedFailure from test\_unicode\_paths\_square\_brackets,
which no longer fails. * Make unit/test\_selection.py ParseTest
support unicode and add test\_unicode\_paths\_non\_globbing unit test
version of functional test. [Aaron A Whitehouse]

* Make test\_selection.py use unicode string literals and still pass. *
funtional/test\_selection.py still fails. [Aaron A Whitehouse]

* Make path.py only accept unicode. * Make all string literals in
test\_selection.py unicode. * Create path.uc\_name as an alternative
to path.name, allowing existing  code to continue using bytes during
transition. * Make file writes in test\_selection.py use io.open. *
Tests do not yet pass. [Aaron A Whitehouse]

* Make globmatch.py deal with either unicode or string globs. * Make
path.uc\_name for unicode name of path (vs path.name for bytes). *
Functional select test failures. [Aaron A Whitehouse]

* Test\_globmatch.py now passing with unicode globs/paths *
test\_square\_bracket\_options\_unicode now passing. [Aaron A Whitehouse]

* Glob\_to\_regex converted to unicode, globmatch.py not yet passing
tests. [Aaron A Whitehouse]

* Fixed bug #1668750 - Don't mask backend errors   - added exception
prints to module import errors. [Kenneth Loafman]

* Added future imports to globmatch.py and added future to tox.ini deps. [Aaron A Whitehouse]

* Added (failing) unicode test. [Aaron A Whitehouse]

* Add tests for square brackets. [Aaron A Whitehouse]

* Add test for unicode paths with asterisks in globs. [Aaron A Whitehouse]

* Added files with unicode names to testfiles and added
TestUnicode.test\_unicode\_paths\_non\_globbing, which tests --include
and --exclude works as expected with these files. [Aaron A Whitehouse]

* Fixed bug #1671852 - Code regression caused by revision 1108   -
change util.uexc() back to bare uexc() [Kenneth Loafman]

* Skip pylint on dpbxbackend.py for now. [Kenneth Loafman]

* Refresh docs. [Kenneth Loafman]

* Fixed PEP8 errors: E402 module level import not at top of file. [Aaron A Whitehouse]

* Uses the globals.archive\_dir variable to store only a string in the
case of a path, uses globals.archive\_dir\_path. [benoit@benoit-desktop]

* Fixed bug #1367675 - IMAP Backend does not work with Yahoo server   -
added the split() as needed in 'nums=list[0].strip().split(" ")'   -
the other fixes mentioned in the bug report comments were already done. [Kenneth Loafman]

* Fixed variable name change in last merge which broke a bunch of tests
- Changed archive\_dir\_root back to archive\_dir. [Kenneth Loafman]

* Change the global name archive\_dir to archive\_dir\_root       add
the arglist to the optparser. [benoit@benoit-desktop]

* Fix E305 PEP8 errors: expected 2 blank lines after class or function
definition, found 1 * Remove E305 from pycodestyle ignores. [Aaron A Whitehouse]

* Fix PEP-8 testing by moving to using pycodestyle library. *
Temporarily add ignores to allow these tests to pass. [Aaron A Whitehouse]

* Fix minor pep8 issue - line too long. [Kenneth Loafman]

* Add support for Shared Access Signatures to the Azure backend. [Matthias Bach]

    Authenticating to the Azure storage via the account is suboptimal as it
    grants the process full administrative permissions on the storage
    account. Usage of a shared access signature allows to pass only the
    minimal permissions on a single container to Duplicity. This makes it
    much more sutable for automated usage, e.g. in cron jobs.

* Fix backup creation using azure-storage > 0.30.0. [Matthias Bach]

    The previous fix only fixed restore and verification of backups.

* Make the Azure backend compatible with azure-storage 0.30.0 and up. [Matthias Bach]

* Update setup.py to show only Python 2.7 support. [Aaron A Whitehouse]

* Fixed bug #1603704 with patch supplied by Maciej Bliziński   - Crash
with UnicodeEncodeError. [Kenneth Loafman]

* Fixed bug #1657916 with patch supplied by Daniel Harvey   - B2
provider cannot handle two backups in the same bucket. [Kenneth Loafman]

* Rename path\_matches\_glob\_fn to select\_fn\_from\_glob, as this more
accurately reflects the return value. * Significantly refactored
unit/test\_globmatch.py to make this cleaner and clearer. [Aaron A Whitehouse]

* Add detail about import exceptions in onedrivebackend.py. [ken]

* Remove time from run-tests, in case this causes any issues (e.g. cross
platform support). [Aaron A Whitehouse]

* Add more scan tests. [Aaron A Whitehouse]

* Removed unused non-globbing code (\_glob\_get\_filename\_sf and
\_glob\_get\_tuple\_sf). * Made run-tests time test runs. * Removed
run-tests-ve, which was identical to run-tests. [Aaron A Whitehouse]

* Move to using single (globing, glob\_get\_normal\_sf) function for
glob strings with and without globbing characters. No performance
impact. [Aaron A Whitehouse]

* Make globs of "/" work with globbing code. * Make globs of "/" match
everything. [Aaron A Whitehouse]

* Made \_glob\_get\_filename\_sf and \_glob\_get\_tuple\_sf internal
functions to ensure no unit tests depend on them directly. [Aaron A Whitehouse]

* Only get a new upload URL when needed.  Add a user agent. [Matthew Bentley]

* Fix pep8 issue. [Kenneth Loafman]

* Fixed bug #1655268 "--gpg-binary option not working"   - If gpg binary
is specified rebuild gpg profile using new binary location. [Kenneth Loafman]

* Futurize -stage1 all files, leaving the isinstance(s,
types.StringType) tests unchanged. * Reverted earlier changes to
types.StringType test in test files. * Created python 2/3 compatible
tests for int and long. [Aaron A Whitehouse]

* Futurize -stage1 on py files in testing for improved python 2/3
support. [Aaron A Whitehouse]

* Fix PEP error on adbackend.py. * Add jottalib as a tox dep to fix
pylint error. [Aaron A Whitehouse]

* Merge in TestExcludeIfPresent from 0.7-series, which tests the
behaviour of duplicity's --exclude-if-present option. [Aaron A Whitehouse]

* Move and rename TestTrailingSlash2 test. [Aaron A Whitehouse]

* Fixed bug #1654220 with patch supplied by Kenneth Newwood   -
Duplicity fails on MacOS because GPG version parsing fails. [Kenneth Loafman]

* Fixed bug #1623342 with patch supplied by Daniel Jakots   - Failing
test on OpenBSD because tar/gtar not found. [Kenneth Loafman]

* Merged in lp:\~breunigs/duplicity/amazondrive3   - As reported on the
mailinglist, if a space is entered while duplicity asks for the URL,
it fails.     Since all important spaces are URL encoded anyway, this
should be fine even if there are spaces in     the URL at all. I also
patched it in the onedrive backend, because it must have similar
issues. [Kenneth Loafman]

* Fix Bug #1642813 with patch from Ravi   - If stat() returns None,
don't attempt to set perms. [Kenneth Loafman]

* Whoops, make a couple of changes to match series-7. [Kenneth Loafman]

* Whoops, fix bad patch * Add gpg2 dir to .bzrignore. [Kenneth Loafman]

* Fix some issues with testing on MacOS * Fix problem with gpg2 in
yakety and zesty. [ken]

* Merged in lp:\~aaron-
whitehouse/duplicity/Bug\_1624725\_files\_within\_folder\_slash   -
Fixed Bug #1624725, so that an include glob ending in "/" now includes
folder contents (for globs with     and without special characters).
This preserves the behaviour that an expression ending in "/" only
matches a folder, but now the contents of any matching folder is
included. [Kenneth Loafman]

* Improve description of new argument in man page. [Will Storey]

* Add new argument to duplicity manpage. [Will Storey]

* Add flag to copy target of symlinks rather than the link. [root]

    This allows us to dereference and include what symlinks point to in our backup.
    I named the argument --copy-links. This is the name rsync gives to a similar
    flag. There is a bug requesting this feature on launchpad, 721599:
    https://bugs.launchpad.net/duplicity/+bug/721599

* Merged in lp:\~ed.so/duplicity/manpage.fixes   - Fix html output via
rman on the website. [Kenneth Loafman]

* Merged in lp:\~dernils/duplicity/robust-dropbox-backend   - Added new
command line option --backend-retry-delay     that allows to determine
the time that duplicity sleeps     before retrying after an error has
occured.   - Added some robustness to dpbxbackend.py that ensures re-
authentication     happens in case that a socket is changed (e.g. due
to a forced reconnect     of a dynamic internet connection). [Kenneth Loafman]

* Fix bug using 40-char sign keys, from Richard McGraw on mail list   -
Remove truncation of argument and adjust comments. [Kenneth Loafman]

* Fixed bug #1642098 - does not create PAR2 archives when '--
par2-options' is used   - Missing space between par2-options plus
default options. [ken]

* Fixed missing rename in Amazon Drive backend. [Stefan Breunig]

* Rename to just "AD" to avoid any possible trademark issues. [Stefan Breunig]

* Document peculiarities of AmazonDrive. [Stefan Breunig]

* Add and document native AmazonDrive backend. [Stefan Breunig]

* Remove uses\_netloc directive. [Håvard Gulldahl]

* JottaCloudBackend: Don't return bytestrings in \_list() [Håvard Gulldahl]

* Adding JottaCloud backend. [Håvard Gulldahl]

* Fixed bug #1621194 with code from Tornhoof   - Do backup to google
drive working without a service account. [Kenneth Loafman]

* Merged in lp:\~mwilck/duplicity/duplicity   - GPG: enable truly non-
interactive operation with gpg2   - This patch fixes the IMO
unexpected behavior that, when using GnuPG2, a pass phrase dialog
always pops up for     saving backups. This is particularly annoying
when trying to do unattended / fully automatic backups. [Kenneth Loafman]

* Fixed bug #1623342 with patch from Daniel Jakots   - failing test on
OpenBSD because tar/gtar not found. [Kenneth Loafman]

* Add requirements.txt - Remove module mocks in conf.py. [Kenneth Loafman]

* OK, finally grokked how to mock out \_librsync, but it did mean having
to change librsync.py with a conditional.  Would have preferred a
cleaner solution. - Fixed the remaining warnings in READTHEDOCS build,
including the removal of a couple of files that were extraneous. [Kenneth Loafman]

* Try autodoc\_mock\_imports... [ken]

* Try autodoc\_mock\_imports... [ken]

* Try autodoc\_mock\_imports... [ken]

* Try fully qualified module name, again. [ken]

* Remove fully qualified name. [ken]

* Resolve recursion in Mock. [ken]

* Try fully qualified and not qualified module names. [ken]

* Try without \_librsync. [ken]

* Try fully qualified module name. [ken]

* Try with virtualenv. [ken]

* Try again... [ken]

* Mock sucks, big time! [ken]

* Mock sucks, big time! [ken]

* Mock sucks! [ken]

* Try MagicMock. [ken]

* Try MagicMock. [ken]

* Fix build on RTD. [ken]

* Fix build on RTD. [ken]

* Fix build on RTD. [ken]

* Fix build on RTD. [ken]

* Fix build on RTD. [ken]

* Remove \_build dir from git. Fix some names, authors. [ken]

* Merged in lp:\~mstoll-de/duplicity/duplicity   - Backblaze announced a
new domain for the b2 api. [Kenneth Loafman]

* Fixed bugs #815510 and #1615480   - Changed default --volsize to 200MB. [Kenneth Loafman]

* First pass at some Sphinx docs for moving to readthedocs.org. [Kenneth Loafman]

* Merged in lp:\~fenisilius/duplicity/acd\_init\_mkdir   - Allow
duplicity to create remote folder. [Kenneth Loafman]

* Added documentation for connecting to IBM Bluemix ObjectStorage. [Arashad Ahamad]

* Added support to connect IBM Bluemix ObjectStorage. [Arashad Ahamad]

* Fixed bug #1612472 with patch from David Cuthbert   - Restore from S3
fails with --with-prefix-archive if prefix includes '/' [Kenneth Loafman]

* Restore testing/gnupg/gpg.conf and testing/gnupg/README. [Kenneth Loafman]

* Fixed conflict in merge from Martin Wilck and applied   -
https://code.launchpad.net/\~mwilck/duplicity/0.7-series/+merge/301492
- merge fixes setsid usage in functional testing. [ken]

* Selection.py: glob\_get\_normal\_sf: use closure
path\_matches\_glob\_fn. [Martin Wilck]

    Use the closure function for checking paths rather than path_matches_glob().

* Globmatch: path\_matches\_glob\_fn: return closure for path match. [Martin Wilck]

    path_matches_glob() re-calculates the regular expressions for
    path matching in every match operation. This is highly inefficient.
    Return a closure with pre-calculated REs instead which can be used
    for path matching later.

* Revert log.Error to log.Warn, as it was prior to the merge in rev
1224, as this was affecting other applications (deja dup). [Aaron A Whitehouse]

* Fixed bug #1600692 with patch from Wolfgang Rohdewald   - Allow
symlink to have optional trailing slash during verify. [ken]

* Fix date in CHANGELOG.  Release date was 2016-07-02, not 01. [ken]

* Fixed bug #1600692 with patch from Wolfgang Rohdewald   - Allow
symlink to have optional trailing slash during verify. [ken]

* Remove import of unittest2 for Python <2.7, now that Python 2.7 is the
minimum version. [Aaron A Whitehouse]

* Remove Python 2.6 settings from tox.ini. [Aaron A Whitehouse]

* Remove Python 2.6 support from the test suite and references to it
from README and README-REPO. [Aaron A Whitehouse]

* Merge 0.7-series changes to README-REPO. [Aaron A Whitehouse]

* Merge 0.7 series changes to README. [Aaron A Whitehouse]

* Merge 0.7 series changes to tox.ini. [Aaron A Whitehouse]

* Fix date in CHANGELOG.  Release date was 2016-07-02, not 01. [ken]

* Properly remove line too long errors (E501) from PEP8 ignores. [Aaron A Whitehouse]

* Fixed lines longer than 120 chars. [Aaron A Whitehouse]

* Set line length error length to 120 (matching tox.ini) and fixed PEP8
E501(line too long) errors. [Aaron A Whitehouse]

* Fix PEP8 W503, line break before binary operator. [Aaron A Whitehouse]

* Fixed bug #1594780 with patches from B. Reitsma   - Use re.finditer()
to speed processing. [Kenneth Loafman]

* Only give an error about not being able to access possibly locked file
if that file is supposed to be included or scanned (i.e. not
excluded). [Aaron A Whitehouse]

* Fixed README-REPO to no longer mention 0.6-series. [Kenneth Loafman]

* Fixed bug #822697 ssh-options not passed in rsync over ssh   - Added
globals.ssh\_options to rsync command line * Increased default volume
size to 200M, was 25M. [Kenneth Loafman]

* Fix PEP8 error in onedrivebackend.py (space before bracket). [Aaron A Whitehouse]

* Fix pep8 issues from last two patch sets. [ken]

* B2 reauth: use other log level. [Markus Stoll]

* Handle expired auth token. [Markus Stoll]

* Fixed bug #1589038 with patches from Malte Schröder   - Added
ignore\_case option to selection functions. [ken]

* Fixed bug #1586992 with patches from Dmitry Nezhevenko   - Patch adds
\_delete\_list to Par2Backend. And \_delete\_list fallbacks to
\_delete calls if wrapped backend has no \_delete\_list. [ken]

* Fixed bug #1586934 with patches from Dmitry Nezhevenko   - fixes error
handling in wrapper. [ken]

* Fixed bug #1573957 with patches from Dmitry Nezhevenko   - upload last
chunk with files\_upload\_session\_finish to avoid extra request   -
upload small files using non-chunked api. [ken]

* Adds prefix support to swift backend. [Ghozlane TOUMI]

    Right now duplicity's swift backend only accept a container as target (swift://container)
    trying to use a prefix / pseudo folder (swift://container/backup/path ) results in a JSON exception.

    This patch adds the abiliy to use path in the swift backend, in order to have multiple backups to the same container neatly organized.

    It borrows some code from the S3 backend, and is quite unobtrusive .

* Fix typo in error handling code. [Scott McKenzie]

* Add missing build-dep apparently now not installed by default with
python2 in xenial+ [Michael Terry]

* Fixed bug #1570293   - removed flush() after write.   - revert to
previous version. [ken]

* Fixed bug #1571134 and #1558155   - used patch from
https://bugs.debian.org/820725 but made changes     to allow the user
to continue using the old version. [ken]

* Remove unused (default) argument. [ken]

* Fixed bug #1569523   - bug introduced in improper fix of bug #1568677
- gotta love those inconsistent APIs. [ken]

* Blasted JIT imports got me again! [ken]

* Fixed bug #1568677   - bug introduced by incomplete fix of bug 1296793
- simplified setting of bucket locations. [ken]

* Fixed bug 1568677 with suggestions from Florian Kruse   - bug
introduced by incomplete fix of bug 1296793. [ken]

* Fix bug reported on the mailing list from Mark Grandi (assertion error
while backing up).  In file\_naming.parse() the filename was being
lower   cased prior to parsing.  If you had used a prefix with mixed
case, we   were writing the file properly, but could not find it in
the backend. [Kenneth Loafman]

* Re-added import of re, as re.compile still used in selection.py. [Aaron Whitehouse]

* Move complexity of matching paths to globs into globmatch.py
path\_matches\_glob, rather than in selection.py Select. [Aaron Whitehouse]

* Move ignorecase handling out of re.compile to use .lower() instead. [Aaron Whitehouse]

* Remove glob\_get\_prefix\_res from selection.py, now that it has moved
to globmatch.py. [Aaron Whitehouse]

* Move content of glob\_get\_prefix\_res to globmatch.py
glob\_get\_prefix\_regexs. [Aaron Whitehouse]

* Fixed globmatch tests. Tests pass. [Aaron Whitehouse]

* Move glob\_to\_re to globmatch.py. Moved associated tests into
test\_globmatch.py. [Aaron Whitehouse]

* Move the logic of the glob\_to\_re method into the glob\_to\_regex
function in globmatch.py. [Aaron Whitehouse]

* Improve man page entry for --exclude-if-present. [Aaron Whitehouse]

* Applied patch from Dmitry Nezhevenko to upgrade dropbox backend:   -
update to SDK v2   - use chunked upload. [Kenneth Loafman]

* Path may be unset. [ed.so]

* Duplicity.1, commandline.py, globals.py - added --ssl-cacert-path
parameter backend.py - make sure url path component is properly url
decoded,   in case it contains special chars (eg. @ or space)
lftpbackend.py - quote \_all\_ cmd line params - added missing
lftp+ftpes protocol - fix empty list result when chdir failed silently
- added ssl\_cacert\_path support webdavbackend.py - add ssl default
context support for python 2.7.9+   (using system certs eg. in
/etc/ssl/certs) - added ssl\_cacert\_path support for python 2.7.9+ -
gettext wrapped all log messages - minor refinements. [ed.so]

* Reverted changes made in rev 1164 w.r.t. getting the source from   VCS
rather than local directory.  Fixes bug #1548080. [Kenneth Loafman]

* Use built-in username/password support in backends.py. [Roman Yepishev]

    Backend is no longer reading environment variables.

    MEDIAFIRE_EMAIL ->
       mf://duplicity%40example.com@mediafire.com/some_path

    MEDIAFIRE_PASSWORD ->
       provided via command line via get_password() or
       FTP_PASSWORD env var or
       mf://duplicity%40example.com:some%20password@mediafire.com/some_path

* Remove custom logging, add usage info. [Roman Yepishev]

* Create folder recursively. [Roman Yepishev]

* Use upload session context manager. [Roman Yepishev]

    This context manager allocates an action token that replaces
    session/signature during uploads. This avoids signature check
    failure if an upload operation needs to be retried.

* Allow importing module, but fail on init. [Roman Yepishev]

* MediaFire Backend - initial version. [Roman Yepishev]

* Backed out changes made by patching for bug #1541314.  These   patches
should not have been applied to the 0.7 series. [Kenneth Loafman]

* Added acdclibackend.py from Stefan Breunig and Malay Shah   - renamed
from amazoncloudbackend to stress use of acd\_cli * Fixed some 2to3
and Pep8 issues that had crept in. [Kenneth Loafman]

* Fixed bug 1474994 Multi backend should offer mirror option  - added
query parameter option to multi-backend  - added mode parameter to
alter how the backend list is operated on (mirror/stripe)  - added
onfail parameter to alter how backend failure is handled  - updated
man-page with documentation. [Thomas Harning Jr]

* Make kerberos optional for webdav backend. [Filip Pytloun]

* Applied patch from kay-diam to fix error handling in ssh pexpect,
fixes bug #1541314. [ken]

* Fix bug #1540279 - mistake in --help. [Kenneth Loafman]

* Clean up pep8 issues. [Kenneth Loafman]

* Fix for bug #1538333 - assert filecount == len(self.files\_changed)
- added flush after every write for all FileobjHooked files which
should prevent some errors when duplicity is forcibly closed. [Kenneth Loafman]

* Add more pylint ignore warnings tags * Adjust so test\_restart.py can
run on Mac as well. [Kenneth Loafman]

* Support GSSAPI authentication in webdav backend. [Filip Pytloun]

* Fix submitter name in changelogs. - Change comment to be correct. [ken]

* Fixed bug #1492301 with patch from askretov (manually refresh oauth). [Kenneth Loafman]

* Fixed bug #1379575 with patch from Tim Ruffling (shorten webdav
response). [Kenneth Loafman]

* Fixed bug #1375019 with patch from Eric Bavier (home to tmp). [Kenneth Loafman]

* Fixed bug #1369243 by adjusting messages to be more readable. [Kenneth Loafman]

* Fixed bug #1260666 universally by splitting the   filelist for delete
before passing to backend. [Kenneth Loafman]

* Pep8 corrections for recently released code. [Kenneth Loafman]

* Bug #1313964 fix. lstrip('/') removed all the slashes, it was an
issue. [mchip]

* Fixed bug #1296793 - Failed to create bucket   - use
S3Connection.lookup() to check bucket exists   - skips Boto's
Exception processing for this check   - dupe of bug #1507109 and bug
#1537185. [ken]

* Applied changes from ralle-ubuntu to fix bug 1072130.   - duplicity
does not support ftpes:// [ken]

* Undo changes to test\_restart.py.  GNU tar is needed. * Fix minor pep8
nit in collections.py. [ken]

* Applied patch from abeverly to fix bug #1475890   - allow port to be
specified along with hostname on S3   - adjusted help text and man
page to reflect the change. [ken]

* Applied patch from shaochun to fix bug #1531154,   - --file-changed
failed when file contains spaces. [Kenneth Loafman]

* Fix stupid issue with functional test path for duplicity. [Kenneth Loafman]

* Make test\_restart compatible with both GNUtar and BSDtar. [Kenneth Loafman]

* Partial fix for bug #1529606 - shell code injection in lftpbackend   -
still need to fix the other backends that spawn shell commands. [Kenneth Loafman]

* Random stuff:   - supply correct path for pydevd under Mac   - fix
some tests to run under Mac as well. [Kenneth Loafman]

* Checkpoint: - remove RPM stuff from makedist - have makedist pull
directly from VCS, not local dir - update po translation directory and
build process - clean up some odd error messages - move Pep8 ignores
to tox.ini. [Kenneth Loafman]

* Checkpoint: - remove RPM stuff from makedist - have makedist pull
directly from VCS, not local dir - update po translation directory and
build process - clean up some odd error messages - move Pep8 ignores
to tox.ini. [Kenneth Loafman]

* 2to3 cleanup. [Kenneth Loafman]

* Pep8 cleanup. [Kenneth Loafman]

* Fix date. [ken]

* Make sure listed files are exactly in the requested path Thanks to
Andreas Knab <knabar@gmail.com> for the pull request. [Matthew Bentley]

* Set fake (otherwise unused) hostname for prettier password prompt
Thanks to Andreas Knab <knabar@gmail.com> for the patch. [Matthew Bentley]

* Add debugging for b2backend. [Matthew Bentley]

* Allow multiple backups in the same bucket. [Matthew Bentley]

* Fix missing import and typos. [Matthew Bentley]

* Undo changes to po files. [Matthew Bentley]

* Remove unnecessary requirements section in manpage. [Matthew Bentley]

* Documentation. [Matthew Bentley]

* Add help text for b2. [Matthew Bentley]

* Add basic error handling. [Matthew Bentley]

* Add BackBlaze B2 backend. Still needs some work (error handling, etc) [Matthew Bentley]

* Support new version of Azure Storage SDK * Refactor \_list method to
support containers with >5000 blobs. [Scott McKenzie]

* Make sure which() returns absolute pathname. [Kenneth Loafman]

* Remove some print statements. [Kenneth Loafman]

* Fix bug #1520691 - Shell Code Injection in hsi backend   - Replace use
of os.popen3() with subprocess equivalent.   - Added code to expand
relative program path to full path.   - Fix hisbackend where it
expected a list not a string. [Kenneth Loafman]

* Fix missing self. [Kenneth Loafman]

* Fix bug #1520691 - Shell Code Injection in hsi backend   - Replace use
of os.popen3() with subprocess equivalent. [Kenneth Loafman]

* Fix #1519694. [Feraudet Cyril]

* Debugged storage class import. [Michal Smereczynski]

* Fixed bug #1511308 - Cannot restore no-encryption, no-compression
backup   - Corrected code to include plain file in
write\_multivolume()   - Added PlainWriteFile() to gpg.py. [Kenneth Loafman]

* Make sure packages using python's tempfile create temp files in
duplicity's temp dir. [ede]

* Reversed previous changes to lockfile.  Now it will take any version
extant in the LP build repository.  (PyPi is not avail in LP build). [Kenneth Loafman]

* Reversed previous changes to lockfile.  Now it will take any version
extant in the LP build repository.  (PyPi is not avail in LP build). [Kenneth Loafman]

* Try adding spaces. [Kenneth Loafman]

* Try lockfile>=0.11.0 (use full version number). [Kenneth Loafman]

* Revert last change. [Kenneth Loafman]

* Try lockfile==0.11.0 instead of lockfile>=0.9. [Kenneth Loafman]

* WindowsAzureMissingResourceError and  WindowsAzureConflictError
classes changed due to SDK changes. [Michal Smereczynski]

* Cleanup issues around Launchpad build, mainly lockfile >= 0.9. [Kenneth Loafman]

* Also check python version number upper bound. we run on 2.6 and 2.7
currently. [ede]

* Don't touch my shebang. [ede]

* Modded tox.ini to use the latest lockfile. [Kenneth Loafman]

* Applied patch from Alexander Zangerl to update to changes in lockfile
API 0.9 and later.  Updated README to notify users. [Kenneth Loafman]

* Add \_\_pycache\_\_. [Kenneth Loafman]

* Upgrade to newest version of pep8 and pylint.   Add three ignores   to
test\_pep8 and one to test\_pylint to get the rest to pass.  They
are all valid in our case. [Kenneth Loafman]

* Fix header date. [Kenneth Loafman]

* The ptyprocess module no longer supports Python 2.6, so fix tox.ini to
use an older version.  Make explicit environs for all tests. [Kenneth Loafman]

* Add support for AWS S3 Standard - Infrequent Access storage class. [Min-Zhong John Lu]

* Fix up broken merge. [Bruce Merry]

* Fix bug #1494228 CygWin: TypeError: basis\_file must be a (true) file
- The problem that caused the change to tempfile.TemporaryFile was due
to the fact that os.tmpfile always creates its file in the system
temp directory, not in the directory specified.  The fix applied was
to use os.tmpfile in cygwin/windows and tempfile.TemporaryFile in all
the rest.  This means that cygwin is now broken with respect to temp
file placement of this one file (deleted automatically on close). [Kenneth Loafman]

* Fix bug #1493573.  Correct option typo in man page. [Kenneth Loafman]

* Add more logging info. [Bruce Merry]

* Fix missing argument in \_error\_code. [Bruce Merry]

* Add an ID cache to the PyDrive backend. [Bruce Merry]

    This is an in-memory cache mapping filenames to object IDs. This potentially
    speeds up searching for a filename (although there is some cost to validate the
    cache on each use). It also ensures that running _query immediately after _put
    will find the file, even if the server doesn't have list-after-write
    consistency (Google Cloud Storage doesn't, but I can't find any info on Drive).

    There are also a number of other improvements:
    - Putting a file with a filename that already exists will replace the file
      in-place, instead of creating a new file with identical filename (which
      Google Drive allows).
    - id_by_name now does a targeted search for just the filename, instead of
      iterating over a complete directory listing.
    - Added _error_code to map 404 errors to backend_not_found
    - Files in the trash are excluded from listings
    - Print a warning when trying to delete a file that doesn't exist.

    This should fix cases where duplicate filenames are created, but it doesn't yet
    deal explicitly with cases where they already exist (it's untested).

    There is also a race condition where if a file is externally deleted during
    _delete, it will raise an exception (which is mapped to backend_not_found).
    That is probably acceptable behaviour, but the behaviour really ought to be
    consistent.

* Par2 backend remove par2 files. [Germar]

* Added debug msgs to the routine checking path selection. [Wojciech Baranowski]

* Refactored the selection.Select.Select method; fewer exit points now. [Wojciech Baranowski]

* Fixed Bug 1438170 duplicity crashes on resume when using gpg-agent
with   patch from Artur Bodera (abodera).  Applied the same patch to
incremental   resumes as well. [Kenneth Loafman]

* Rename tox profile for Launchpad's Precise build server to "lpbuildd-
precise" for clarity (and to make it clear it should be removed once
Precise is no longer supported). [Aaron Whitehouse]

* Set RUN\_CODE\_TESTS to 0 for lpbuildd tox profile, reflecting its
value on the Launchpad build server (and therefore skipping PEP8, 2to3
and pylint). More accurately reflects the system we are mimicking and
saves approximately 1 minute per test run. [Aaron Whitehouse]

* Add further instructions in README-REPO on how to test against one
environment. [Aaron Whitehouse]

* Add lpbuilldd as an additional tox profile, replicating the setup of
the launchpad build server. [Aaron Whitehouse]

* Fixed Bug 1476019 S3 storage bucket not being automatically created
with patch from abeverley. [Kenneth Loafman]

* Fixed Bug 1476019 S3 storage bucket not being automatically created
with patch from abeverley. [Kenneth Loafman]

* Change use of mock.patch to accommodate the obsolete version of
python-mock on the build server (and avoid the following error:
TypeError: patch() got an unexpected keyword argument 'return\_value'
) [Aaron Whitehouse]

* Fixed 2to3 issues. Updated README-REPO with more test information.
Updated pylint and test\_diff2 descriptions to make it clear these
require packages to be installed on the system to pass. All tests pass
on Python 2.6 and Python 2.7 as at this revision. [Aaron Whitehouse]

* Added support for Identity v3. [Dag Stenstad]

* Made globs with trailing slashes only match directories, not files,
fixing Bug #1479545. [Aaron Whitehouse]

* Added functional unittests to exhibit current behaviour of trailing
slashes in globs. See Bug #1479545. [Aaron Whitehouse]

* Delete redundant second sys import in test\_code.py. [Aaron Whitehouse]

* Fixed tox.ini to correctly run individual tests. Updated test\_code.py
to use unittest2 for Python versions < 2.7 (instead of failing).
Improved testing directions in README-REPO. [Aaron Whitehouse]

* Re-enable tests that had been temporarily commented out. [Aaron Whitehouse]

* Add test\_glob\_re unit test back in. [Aaron Whitehouse]

* Remove unnecessary use of mock.patch in unit.test\_selection.py. [Aaron Whitehouse]

* Remove special casing for final glob in glob list as no longer
necessary. [Aaron Whitehouse]

* Fixed Bug #932482 by checking for a trailing slash in each glob and
removing it if present. Enabled tests checking this behaviour. PEP8
fixes along the way. [Aaron Whitehouse]

* Stopped an exclude glob trumping an earlier scan glob, but also
ensured that an exclude glob is not trumped by a later include. Fixed
Bug #884371. Activated the (expectedFailure) tests that were failing
because of this bug. [Aaron Whitehouse]

* Additional tests to exhibit current exclude/scan interaction and
implement two functional tests as unit tests. [Aaron Whitehouse]

* Added unit tests for negative square brackets ([!a,b,c] and [!1-4]). [Aaron Whitehouse]

* Added test cases (unit and functional) to test the current behaviour
of selection.py. [Aaron Whitehouse]

* Fixed bug 1471348 Multi back-end doesn't work with hubiC (again)    -
hubiC should reach up to duplicity.backend.\_\_init\_\_ [Kenneth Loafman]

* Fixed bug 1471348 Multi back-end doesn't work with hubiC   - added
init of appropriate superclass in both cases. [Kenneth Loafman]

* Re-enable the test of the --progress option
(test\_exclude\_filelist\_progress\_option), which was marked as an
expected failure. The issue causing this test to fail was fixed in
revision 1095 and the test now passes. [Aaron Whitehouse]

* Fixed two filename references in po/POTFILES.in, a mistake which crept
in in rev 1093 and caused testing/run-tests to fail with "IndexError:
list index out of range". [Aaron Whitehouse]

* New parameter --gpg-binary allows user to point to a different gpg
binary, not necessarily in path. [ed.so]

* Fixed bug 1466582 - reduce unnecessary syscall with --exclude-if-
present - with   patch from Kuang-che Wu to make sure resulting path
is a directory. [Kenneth Loafman]

* Fixed bug 1466160 - pydrive backend is slow to remove old backup set -
with   patch from Kuang-che Wu to implement \_delete\_list(). [Kenneth Loafman]

* Fixed bug 1466582 - reduce unnecessary syscall with --exclude-if-
present - with   patch from Kuang-che Wu to make sure resulting path
is a directory. [Kenneth Loafman]

* Fixed bug 1466160 - pydrive backend is slow to remove old backup set -
with   patch from Kuang-che Wu to implement \_delete\_list(). [Kenneth Loafman]

* Fixed bug 1452263 - par2 option not working on small processors - with
patch   from Kuang-che Wu to ignore default 30 second timeout. [Kenneth Loafman]

* Fixed bug 1465335 - pydrive still use files in trash can - with patch
from Kuang-che Wu to ignore trashed files. [Kenneth Loafman]

* Fixed bug 791794 - description of --gpg-options is misleading, Simply
needed to add the '--' before the options as in "--opt1 --opt2=parm". [Kenneth Loafman]

* Fix a couple of PEP8 glitches. [Kenneth Loafman]

* Add full\_listing=True so that swiftclient returns more than 10000
objects. Default is False. [Remy van Elst relst@relst.nl]

* Manpage - some reordering, update "A NOTE ON SSH BACKENDS" to the new
prefix+ changes. [ede]

* Make pydrive new gdocs default backend keep gdata backend as
gdata+gdocs:// [ede]

* Support using PyDrive with a regular Google account, instead of a
service account. [Bruce Merry]

* Perform seek(0) on filelist before read(). [Scott McKenzie]

* Reset filelist position to beginning of file after calling read().
This allows file to be read again. [Scott McKenzie]

* Add proper error messages for OneDrive backend when python-requests or
python-requests-oauthlib is not installed (bug 1453355). [Sami Jaktholm]

* Added ability to get single file status from collection-status with
patch from jitao (bug 1044715), like so:   $ duplicity collection-
status --file-changed c1 file://./foo. [Kenneth Loafman]

* Enable --ignore-errors flag in rdiffdir. [Kenneth Loafman]

* Fixed bug 1448249 and bug 1449151 thanks to David Coppit.   - When
patching, close base file before renaming. [Kenneth Loafman]

* Fixed bug 1444404 with patch from Samu Nuutamo   - rdiffdir patch
crashes if a regular file is changed to a non-regular     file
(symlink, fifo, ...) [Kenneth Loafman]

* Fix bug 1432229 in Copy.com backend   - Reply header has no content-
type for JSON detection. Now, we also check     whether the content
starts with '{'. [Carlos Eduardo Moreira dos Santos]

* Move requirements section lower in manpage. [Kenneth Loafman]

* Logging cleanup. [Steve Tynor]

* Typo - missing quote. [Steve Tynor]

* Add doc. [Steve Tynor]

* Add doc. [Steve Tynor]

* Adjust delete to make unit tests pass. [Steve Tynor]

* Document json format. [Steve Tynor]

* Use json config in prep for supporting new pydrive backend that
requires env variables. [Steve Tynor]

* Improved logs; dont allow low level retry to kick in. [Steve Tynor]

* Initial working code - tested with gdocs and file backends. [Steve Tynor]

* Fix bug 1437789 with patch from pdf   - par2backend.py incorrect
syntax in get() [Kenneth Loafman]

* Fix bug 1434702 with help from Robin Nehls   - incorrect response
BackendException while downloading signatures file. [Kenneth Loafman]

* Fix bug 1432999 with hint from Antoine Afalo. [Kenneth Loafman]

* Updated duplicity.pot. [Aaron Whitehouse]

* Remove extraneous string format arg in previous scp fix. [Kenneth Loafman]

* Fix for --pydevd debug environment and location under Eclipse. * Fix
for bug where scp was actually working as scp and not working with
rsync.net because of using extraneous test command in restricted
shell.   Was trying "test -d 'foo' || mkdir -p 'foo'", now only "mkdir
-p foo". [Kenneth Loafman]

* Really fix bug 1416344 based on comment #5 by Roman Tereshonkov. [Kenneth Loafman]

* Fix \_librsyncmodule.c compilation, bug 1416344, thanks to Kari
Hautio. [Kenneth Loafman]

* Fix spelling error in manpage, bug 1419314. [Kenneth Loafman]

* Coalesce CHANGELOG. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E401   - see
http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E231, E241, E251, E261,
E262, E271, E272, E301, E302, E303, E502,     E701, E702, E703, E711,
E721, W291, W292, W293, W391   - see http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E231, E241, E251, E261,
E262, E271, E272   - see http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E231, E241   - see
http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E231, E241   - see
http://pep8.readthedocs.org * Fixes for 2to3 issues. [Kenneth Loafman]

* Changed tests to test filelist, rather than globbing filelist, except
for one functional globbing test of each type to ensure this continues
to work until it is deliberately removed. Changed naming of tests etc
accordingly. [Aaron Whitehouse]

* Removed unnecessary tests (post merging of non-globbing and globbing
filelists) and created a globbing version of the one test that was
only written for non-globbing filelists. [Aaron Whitehouse]

* Updated manual to remove references to globbing filelists and stdin
filelists and make consequential changes to the description of
include-filelist and exclude-filelist behaviour. [Aaron Whitehouse]

* Note Bug #1423367 was fixed in the previous commit. [Aaron Whitehouse]

* Mark --include-filelist-stdin and --exclude-fielist-stdin for
deprecation and hide from --help output. Add additional tests in
stdin\_test.sh to test --include-filelist-stdin and that /dev/stdin is
an adequate replacement. [Aaron Whitehouse]

* Added bash script (stdin\_test.sh) showing that filelists from stdin
were working as expected despite the changes. [Aaron Whitehouse]

* Added deprecation warning to the --exclude-globbing-filelist and
include-globbing-filelist options in commandline.py and hid them from
help output. Commented out functions relating to non-globbing
filelists. Commented out unit tests related to non-globbing filelists. [Aaron Whitehouse]

* Made non-globbing filelists use the globbing code path (ie made all
filelists globbing), as per:
http://lists.nongnu.org/archive/html/duplicity-
talk/2015-01/msg00011.html Fixed Bug #1408411 in the process, as this
issue was limited to the non-globbing code path. [Aaron Whitehouse]

* Added functional and unit tests to show Bug #932482 - that selection
does not work correctly when excludes (in a filelist or in a
commandline option) contain both a single or double asterisk and a
trailing slash. [Aaron Whitehouse]

* Added credit to Elifarley Cruz for one of the test cases. [Aaron Whitehouse]

* Added functional tests to functional/test\_selection.py to show Bug
#884371 (* and ** not working as expected) applies to commandline
--include. [Aaron Whitehouse]

* Added tests to unit/test\_selection.py and
funtional/test\_selection.py to show the behaviour reported in Bug
#884371, i.e. that selection is incorrect when there is a * or ** on
an include line. [Aaron Whitehouse]

* Add option --exclude-older-than to only include recently modified
files. [Angus Gratton]

* Ongoing pep8 corrections. [Kenneth Loafman]

* Applied patch from Adam Reichold to fix bug # 1413792. [Kenneth Loafman]

* Fixed bug # 1414418   - Aligned commandline.py options and help
display contents.   - Aligned commandline.py options and manpage
contents. * Changed --s3\_multipart\_max\_timeout to --s3-multipart-
max-timeout to be   consistent with commandline option naming
conventions. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - 201, 202, 203   - see
http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E127, E128   - see
http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E111, E121, E122, E124,
E125, E126   - see http://pep8.readthedocs.org. [Kenneth Loafman]

* Remove 'gs' and 's3+http' from uses\_netloc[].  Fixes Bug 1411803. [Kenneth Loafman]

* Fixed variable typo in commandline.py that was causing build fails. [Kenneth Loafman]

* Fixed some tabs/spaces problems that were causing install failures. [Kenneth Loafman]

* Changed passing keyfile via query in URL to passing the key by
environment variable. Fixed manpage accordingly. Restored Azure info
in manpage that was somehow mistakenly deleted. [Yigal Asnis yigalasnis@yahoo.com]

* Fixed URI parsing. [Yigal Asnis yigalasnis@yahoo.com]

* Added pydrive backend aimed to replace the deprecated gdocs backend. [Yigal Asnis yigalasnis@yahoo.com]

* Removed underscores from example Azure container names - added Azure
container name rules to man page - handle unicode messages correctly
in Azure Exceptions. [Scott McKenzie]

* Added test\_exclude\_globbing\_filelist\_progress\_option into
functional/test\_selection.py, which shows the error reported in Bug
#1264744 - that the --exclude-globbing-filelist does not backup the
correct files if the --progress option is used. Test is marked as an
expected failure so as not to cause the test suite to fail. [Aaron Whitehouse]

* Add SWIFT\_REGIONNAME parameter to select SWIFT REGION. See bug
#1376628. [Vincent Cassé]

* Fixed some recently added 2to3 and pep8 issues. [Kenneth Loafman]

* Modified:   duplicity/backends/azurebackend.py. [Scott McKenzie]

    Added _error_code method.

* Modified:   duplicity/backends/azurebackend.py. [Scott McKenzie]

    Added _query method.

* Modified:   bin/duplicity.1   duplicity/commandline.py. [Scott McKenzie]

    Added man page and help entry for Azure backend.

* Added:   duplicity/backends/azurebackend.py. [Scott McKenzie]

* Fix Bug #1408289. [Stephane Angot]

* Selection.py modified to pre-process lines for both globbing and non-
globbing filelists to: remove leading and trailing whitespace; process
quoted filenames correctly; remove blank lines; and ignore full-line
comments. Added tests to unit/test\_selection.py and
functional/test\_selection.py to cover these. Added a new folder
select2 to the testfiles.tar.gz for the new functional tests (clearer
names and a folder with trailing whitespace). [Aaron Whitehouse]

* Added functional test cases to show the issue reported in Bug #1408411
(Filelist (non-globbing) should include a folder if it contains higher
priority included files -
https://bugs.launchpad.net/duplicity/+bug/1408411). [Aaron Whitehouse]

* Add a backend for Microsoft OneDrive. [Michael Stapelberg]

* Fixed bug 1278529 by applying patch supplied in report   - Use
get\_bucket() rather than lookup() on S3 to get proper error msg. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:    - E211, E221, E222, E225,
E226, E228    - see http://pep8.readthedocs.org. [Kenneth Loafman]

* Fixed bug 1406173 by applying patch supplied in report   - Ignore
.par2 files in remote file list * Removed redundant shell test
testing/verify\_test.sh. [Kenneth Loafman]

* Add else to try-except in badupload functional test, to catch where
the test passes successfully instead of throwing an error (as it
should). [Aaron Whitehouse]

* Add comments to the verify\_test.sh script matching up the tests in
there to the tests implemented in test\_verify.py. All the tests in
the shell script have now been implemented, so the shell script should
perhaps be deleted. [Aaron Whitehouse]

* Add tests to test\_verify.py to test that verify fails if the archive
file is corrupted. Changed file objects to use the with keyword to
ensure that the file is properly closed. Small edit to find statement
in verify\_test.sh to make it work as expected (enclose string in
quotes). [Aaron Whitehouse]

* Simplify test\_verify.py to just do a simple backup and verify on a
single file in each test. Modify tests to correctly use --compare-data
option and to add tests for verify when the source files have the
atime/mtime manipulated. [Aaron Whitehouse]

* Make ssh an unsupported backend scheme * Temporarily disable
RsyncBackendTest and test\_verify\_changed\_source\_file. [Kenneth Loafman]

* Move netloc usage definitions into respective backends. [ed.so]

* Added in tests including compare\_data. [Aaron Whitehouse]

* Added test\_verify\_changed\_source\_file test to flag up the issue
mentioned in Bug #1354880. [Aaron Whitehouse]

* Allow --sign-key to use short format, long format alt. full
fingerprint. [Andreas Olsson]

* Source formatted, using PyDev, all source files to fix some easily
fixed   PEP8 issues. Use ignore space when comparing against previous
versions. [Kenneth Loafman]

* Fix identity file parsing of --ssh-options for paramiko manpage fixes. [ede]

* Modded .bzrignore to ignore *.egg test dependencies, normalized,
sorted. [Kenneth Loafman]

* Manually merged in lp:\~m4ktub/duplicity/0.6-reliability   - Per fix
proposed in Bug #1395341. [Kenneth Loafman]

* Fix changelogs comments. [Kenneth Loafman]

* Fixed bug 1255453 with changes by Gaudenz Steinlin, report backend
import   results, both normal and failed, at INFO log level. [Kenneth Loafman]

* Fixed bug 1236248 with changes by az, manpage warning about --extra-
clean. [Kenneth Loafman]

* Fixed bug 1385599 with changes by Yannick Molin. SSL settings are now
conditioned on protocol ftp or ftps. [Kenneth Loafman]

* Update man page. [Adrien Delhorme]

* Update man page Add hubic identity module. [Adrien Delhorme]

* Add Hubic backend. [Adrien Delhorme]

* In webdavbackend.py:   - Fixed bug 1396106 with change by Tim Ruffing,
mispelled member.   - Added missing 'self.' before member in error
message. [Kenneth Loafman]

* Undid move of testing/test\_code.py.  Instead I fixed it   so that it
would not run during PPA build.  It now needs   the setting
RUN\_CODE\_TESTS=1 in the environment which is   supplied in the
tox.ini file. [Kenneth Loafman]

* Moved testing/test\_code.py to testing/manual/code\_test.py   so PPA
builds would succeed.  Should be moved back later. [Kenneth Loafman]

* Remove valid\_extension() check from file\_naming.py.  It was
causing failed tests for short filenames.  Thanks edso. [Kenneth Loafman]

* Partial fix for PPA build failures, new backend name. [Kenneth Loafman]

* Fix dpbx import error import lazily. [ed.so]

* Fix for failing PPA builds.  FTP backend has variable class names. [Kenneth Loafman]

* Fix files list. [Kenneth Loafman]

* Fix typo ('hidding' to 'hiding') [Aaron Whitehouse]

* Escape filename before printing in unicode. [Michael Terry]

* Add https cert verification switches. [ed.so]

* More manpage fixes/reformatting retire parameters --ssh-backend,
--use-scp, functionality is achieved via scheme:// setting now add
lftp webdav support add lftp fish support fix assertionerror when
using par2+ backend. [ed.so]

* Manpage: document ftp changes/minor enhancements. [ed.so]

* Allow ftp backend selection via prefix. [ed.so]

* Rename lftp/ncftp backends. [ed.so]

* Restore ncftp backend. [ed.so]

* Support older versions of dpkg-parsechangelog. [Michael Terry]

* Some small testing fixes to work on older copies of mock and pylint. [Michael Terry]

* Minor tweaks to debian/control to fix building on older versions of
Ubuntu. [Michael Terry]

* Fix Edgar's name. [Michael Terry]

* Add debian packaging. [Michael Terry]

* Avoid super() on old-style class. [Michael Terry]

* Fix pylint/pep8 nits so that tests pass. [Michael Terry]

* Adjust unit tests to expect single FTP backend. [Kenneth Loafman]

* Use lftp for both FTP and FTPS. [Moritz Maisel]

* Minor accounting fix. [Kenneth Loafman]

* Merged in lp:\~johnleach/duplicity/1315437-swift-container-create   -
Check to see if the swift container exists before trying to create it,
in case we don't have permissions to create containers. Fixes #1315437. [Kenneth Loafman]

* Clean up imports. [Kenneth Loafman]

* Merged in lp:\~ed.so/duplicity/0.7-dpbx.importfix   - fix this
showstopper with the dropbox backend     "NameError: global name
'rest' is not defined" [Kenneth Loafman]

* Merged in lp:\~jflaker/duplicity/BugFix1325215   - The reference to "
--progress\_rate" in the man page as a parameter is     incorrect.
Should be "--progress-rate". [Kenneth Loafman]

* Change the branch for stable. lp:duplicity/stable doesn't exist and so
I've changed this to lp:\~duplicity-team/duplicity/0.6-releases as
this is the only non-Windows, non-dev branch. [Aaron Whitehouse]

* Corrected the extra dot in the stable branch line at step 1. [Aaron Whitehouse]

* Updated README-REPO to reflect restructuring of directories. See
https://answers.launchpad.net/duplicity/+question/252898. [Aaron Whitehouse]

* Fixed bug 1375304 with patch supplied by Aleksandar Ivanovic. [Kenneth Loafman]

* Fix two small typos in duplicity man page. [Jeffrey Rogers]

* Clarify verify's functionality as wished for by a user surprised with
a big bandwidth bill from rackspace. [ede]

* Added sxbacked.py, Skylable backend.  Waiting on man page updates. [Kenneth Loafman]

* Fixed bug 1327550: OverflowError: signed integer is greater than
maximum   - Major and minor device numbers are supposed to be one byte
each.  Someone     has crafted a special system image using OpenVZ
where the major and minor     device numbers are much larger (ploop
devices).  We treat them as (0,0). [Kenneth Loafman]

* Added user defined verbatim options for par2. [Anton Maklakov]

* Restore accidental deletion. [Kenneth Loafman]

* Fix setdata() not being called a better way. [Michael Terry]

* Use writefileobj instead of direct write, for less code and so that we
call setdata() [Michael Terry]

* More reliably reset webdav connection. [Michael Terry]

* Webdav backend fix "BackendException: Bad status code 200 reason OK. "
when restarting an interrupted backup and overwriting partially
uploaded volumes. [ede]

* README: add copy.com requirements. [Marco Trevisan (Treviño)]

* Add copy.com to man file. [Marco Trevisan (Treviño)]

* CopyComBackend: import non-main modules only when needed. [Marco Trevisan (Treviño)]

* CopyComBackend: remove unneded upload checks. [Marco Trevisan (Treviño)]

* CopyComBackend: implement \_query method. [Marco Trevisan (Treviño)]

    Now the backend should be pretty complete

* CopyComBackend: disable the \_delete\_list support, it won't work if a
file doesn't exist. [Marco Trevisan (Treviño)]

    If a file in list does not exist, the Copy server will stop deleting the subsequent stuff,
    raising an error and making test_delete_list to fail.

* CopyComBackend: add ability to delete list of files. [Marco Trevisan (Treviño)]

* Backends: Add Copy.com support, implement basic operations. [Marco Trevisan (Treviño)]

* Update shebang line to python2 instead of python to avoid confusion. [Kenneth Loafman]

* Support py2.6.0. [Michael Terry]

* Clean up indentation mismatches. [Kenneth Loafman]

* Misc format fixes. [Kenneth Loafman]

* Applied expat fix from edso.  See answer #12 in
https://answers.launchpad.net/duplicity/+question/248020   * Forward-
ported from r980 in 0.6-series. [Michael Terry]

* First cut of 0.7.00 Changelog. [Kenneth Loafman]

* Fix running ./testing/manual/backendtest to be able to find config.py
and fix the tests in testing/manual/ to not be picked up by ./setup.py
test. [Michael Terry]

* Convert exceptions to unicode. [Michael Terry]

* Further fixes. [Michael Terry]

* Fix map usage for py3 readiness. [Michael Terry]

* Fix filter usage for py3 readiness. [Michael Terry]

* Fixed bug #1312328 WebDAV backend can't understand 200 OK response to
DELETE   - Allow both 200 and 204 as valid response to delete. [Kenneth Loafman]

* Minor fixes. [Michael Terry]

* Add ftp backend test. [Michael Terry]

* Drop popen\_subprocess\_persist in favor of just the basic version;
add ftps backend test. [Michael Terry]

* And test hsi backend too. [Michael Terry]

* Add fake tahoe executable, so we can test the tahoe backend. [Michael Terry]

* Add support for backend prefixes, allow rsync backend to use local
paths, and add some more tests. [Michael Terry]

* Add some backend tests, clean up par2backend, and general fixes. [Michael Terry]

* Checkpoint. [Michael Terry]

* Add overrides dir. [Michael Terry]

* More minor fixes. [Michael Terry]

* Move rootfiles.tar.gz into manual directory. [Michael Terry]

* Add initial pep8 and pylint tests. [Michael Terry]

* Minor fixes. [Michael Terry]

* Make run-tests scripts go through tox, this makes all our standard
test-running modes ultimately go through ./setup test. [Michael Terry]

* Drop little-used misc.py. [Michael Terry]

* More reorg of testing/ [Michael Terry]

* Convert unicode to utf8 before passing to print. [Michael Terry]

* Drop static.py. [Michael Terry]

* Fix subprocess usage to work in py2.6 and fix a missing unicode. [Michael Terry]

* Solve has\_key 2to3 fix. [Michael Terry]

* Move imports fix to the 'don't care' section. [Michael Terry]

* Solve import 2to3 fix. [Michael Terry]

* Solve numliterals 2to3 fix. [Michael Terry]

* Solve long 2to3 fix. [Michael Terry]

* Move urllib fix to the 'don't care' section. [Michael Terry]

* Solve basestring 2to3 fix. [Michael Terry]

* Move long and raw\_input fixes to the 'don't care' section. [Michael Terry]

* Solve reduce 2to3 fix. [Michael Terry]

* Solve raise 2to3 fix. [Michael Terry]

* Mark callable and future fixes as things we explicitly don't care
about. [Michael Terry]

* Solve apply 2to3 fix. [Michael Terry]

* Solve idioms 2to3 fix. [Michael Terry]

* Solve ws\_comma 2to3 fix. [Michael Terry]

* Solve renames 2to3 fix. [Michael Terry]

* Solve except 2to3 fix. [Michael Terry]

* Add test\_python3.py to test readiness of source code to run under
python3 directly. [Michael Terry]

* Fix typo. [Michael Terry]

* Drop local copy of pexpect -- only used by one of our ssh backends and
our tests. [Michael Terry]

* Fix drop-u1 merge. [Michael Terry]

* Drop support for Ubuntu One, since it is closing. [Michael Terry]

* Drop support for Python 2.4 and 2.5. [Michael Terry]

* Add missing mock dep. [Michael Terry]

* Whoops, make dist dir first during sdist. [Michael Terry]

* Enable/use more mordern testing tools like nosetest and tox as well as
more common setup.py hooks like test and sdist. [Michael Terry]

* Consolidate all the duplicity-running code in the test framework. [Michael Terry]

* Added support for amazon s3 encryption by the use of --s3-use-server-
side-encryption. [Fredrik Loch fredrik.loch@gmail.com]

* Added support for serverside encryption in amazon s3. [Fredrik Loch fredrik.loch@gmail.com]

* Fixed boto import issues. [Prateek Malhotra]

* Fix dpbx backend "NameError: global name 'rest' is not defined" [ede]

* Fix boto import. [Kenneth Loafman]

* Make sure each process in a multipart upload get their own fresh
connection. [Prateek Malhotra]

* Updated manpage and tweaked boto backend connection reset. [Prateek Malhotra]

* Added max timeout for chunked uploads and debug lines to gauage upload
speed. [Prateek Malhotra]

* Fixes for merging multi boto backend. [Prateek Malhotra]

* Fixes https://bugs.launchpad.net/duplicity/+bug/1218425. [Prateek Malhotra]

* Fixed get\_connection for new generic storage. [Prateek Malhotra]

* Fixed merge conflicts after merging in changes from main branch,
mostly due to Google Storage class addition. [Prateek Malhotra]

* Trying fix to properly destroy S3 connections. [Prateek Malhotra]

* README update for BOTO version requirement. [Prateek Malhotra]

* Added support for AWS S3 Glacier. [Prateek Malhotra]

* Added commentS. [Prateek Malhotra]

* Added max proc rule for multipart S3 uploads. [Prateek Malhotra]

* Fix pexpect import. [Michael Terry]

* Add documentation to manpage rename \~par2wrapperbackend.py. [Germar]

* Add test that includes unicode characters to check the gpg prompt. [Michael Terry]

* Encode prompt phrase before passing to getpass. [Michael Terry]

* Applied two patches from mailing list message at:
https://lists.nongnu.org/archive/html/duplicity-
talk/2014-01/msg00030.html   "Added command line options to use
different prefixes for manifest/sig/archive files"   This resolves
https://bugs.launchpad.net/duplicity/+bug/1170161 and provides   a
workaround for https://bugs.launchpad.net/duplicity/+bug/1170113. [Kenneth Loafman]

* Update to translations. [Kenneth Loafman]

* Encode sys.argv using system filename encoding before printing. [Michael Terry]

* Remove --add-concurrency option and enhance the error message the case
where an existing lockfile is detected. [Louis Bouchard]

* Reformat --allow-concurrency text and add mention of stale lockfile. [Louis Bouchard]

* Update manpage with new --add-concurrency option. [Louis Bouchard]

* Add the --allow-concurrency option to disable the locking mechanism
that this patch implements. By default, only one instance of duplicity
will be allowed to run at once. When using this switch it disable the
locking mechanism to allow more than one instance to run
simultaneously (LP: #1266763) [Louis Bouchard]

* Raise exception if we can't connect to S3 rather than just silently
pretending there are no files. [Michael Terry]

* Restored patch of gdocsbackend.py from original author (thanks ede) *
Applied patch from bug 1266753: Boto backend removes local cache if
connection cannot be made. [Kenneth Loafman]

* Recommit: implement fix as suggested by original autor
http://lists.nongnu.org/archive/html/duplicity-
talk/2013-11/msg00017.html. [ede]

* Reformat to be more consistent.  Remove tabs. [Kenneth Loafman]

* Reverted changes to gdocsbackend.py. [Kenneth Loafman]

* Leftover from previous commit (thx Kostas for paying attention) [ede]

* Implement fix as suggested by original autor
http://lists.nongnu.org/archive/html/duplicity-
talk/2013-11/msg00017.html. [ede]

* Restored missing line from patch of gdocsbackend.py. [Kenneth Loafman]

* Fix help printing. [Michael Terry]

* Promote filenames to unicode when printing to console and ensure that
filenames from backend are bytes. [Michael Terry]

* Nuke tabs. [Kenneth Loafman]

* Upstream debian patch "webdav create folder recursively" http://patch-
tracker.debian.org/package/duplicity/0.6.22-2. [ede]

* Upstream debian patch "paramiko logging" http://patch-
tracker.debian.org/package/duplicity/0.6.22-2. [ede]

* Fix the fix for dropbox backend. [ede]

* Remove obsolete cfpyrax+http:// scheme from manpage. [ede]

* Update Changelog.GNU fix "Import of duplicity.backends.dpbxbackend
Failed: No module named dropbox" [ede]

* Add mega documentation. [ede]

* Some formatting fixes to rman issues on website display. [ede]

* Update boto minimum version requirements. [Lee Verberne]

* Changed to default to pyrax backend rather than cloudfiles backend.
To revert to the cloudfiles backend use '--cf-backend=cloudfiles' [Kenneth Loafman]

* Fixed cfpyrax entry in man page. [Jonathan Krauss]

* Added Pyrax backend for Rackspace Cloud. [Jonathan Krauss]

* Added Pyrax backend for Rackspace Cloud. [Jonathan Krauss]

* Applied patch to fix "Access GDrive through gdocs backend failing"   -
see https://lists.nongnu.org/archive/html/duplicity-
talk/2013-07/msg00007.html. [Kenneth Loafman]

* Avoid throwing exception because of None element in patch sequence. [Michael Terry]

* Handle a disappearing source file across restarts better. [Michael Terry]

* Fix test comments. [Michael Terry]

* Don't keep dangling volume info in manifest. [Michael Terry]

* Show path type in log when listing files. [Michael Terry]

* Better error message for chown fail. [Gábor Lipták]

* Merged in lp:\~verb/duplicity/bucket\_root\_fix   - Fix bug that
prevents backing up to the root of a bucket with boto backend. [Kenneth Loafman]

* Don't chop the first argument off when restarting (in an admittedly
difficult-to-reach bit of code) [Michael Terry]

* Fix some spacing. [Michael Terry]

* Wrap whole seq2ropath function in a general try/except rather than a
more focused approach -- any problem patching a file should be ignored
but logged before moving on. [Michael Terry]

* If a common exception happens when collapsing a non-file patch, just
log it and continue. [Michael Terry]

* Or better yet, just drop the stanza, it shouldn't be needed. [Michael Terry]

* Fix else: to be except Exception: [Michael Terry]

* Fix util.ignore\_missing; patch by Matthias Witte. [Michael Terry]

* Applied patch from bug 1216921 to fix ignore\_missing(). [ken]

* Changes for 0.6.22. [ken]

* Update paramiko links add command  parameters to synopsis add
--compare-data some polishing several improvements. [ede]

* Applied patch from Eric S Raymond to man page to fix markup problems. [ken]

* Fix requesting filename. [Christian Kornacker]

* Adapt to mega.py API changes. [Christian Kornacker]

* Cleanup copyright notice. [Christian Kornacker]

* Adding Mega backend for mega.co.nz. [Christian]

    this code is based on gdocsbackend.py

    it requires either
    https://github.com/ckornacker/mega.py.git
    or (changes not yet pulled)
    https://github.com/richardasaurus/mega.py.git

* Add documentation for GCS to duplicity.1. [Lee Verberne]

* Add config template for testing boto backend with GCS. [Lee Verberne]

* Add support for Google Cloud Storage to boto backend (single threaded
only) [Lee Verberne]

* Explicitly set umask in test\_tarfile.py. [Lee Verberne]

    tar honors umasks which causes the unittest to fail if a more restrictive mask
    (e.g. 027) is set.  This change sets umask explicitly.

* Adds doc. [Matthieu Huin]

* Better handling of authentication alternatives. [Matthieu Huin]

* Updates copyright. [Matthieu Huin]

* Fixes data size type. [Matthieu Huin]

* Fixes missing argument. [Matthieu Huin]

* Fixes wrong environment variable being used. [Matthieu Huin]

* Adds OpenStack Swift backend. [Matthieu Huin]

* Use FTP\_PASSWORD with pexpect backend without requiring --ssh-
askpass. [Nathan Scowcroft]

* Add par2 wrapper backend. [Germar]

* Applied duplicity-ftps.patch from
https://bugs.launchpad.net/duplicity/+bug/1104069   - Don't try to
delete an empty file list. [Kenneth Loafman]

* Applied blocksize.patch from
https://bugs.launchpad.net/duplicity/+bug/897423   - New option --max-
blocksize (default 2048) to allow increasing delta blocksize. [Kenneth Loafman]

* No more cleartext credentials in the code. [jno]

* Application Key & Secret get obfuscated to fit the rq of Dropbox. [jno]

* Crosser's patch applied. [jno]

* Propagate exceptions upward to facilitate retries. [jno]

* Typo fixed. [jno]

* Log.py had no Error() to supplement Info(), Warn(), and Debug() -
fixed. [jno]

* 1. usage note added (on separate Dropbox account). 2. extraneous and
useless mkdir call was removed in put() method. [jno]

* Even more logging for unhandled exceptions to catch Error connecting
to "api-content.dropbox.com" [jno]

* Traceback logging added for semi-unhandled exceptions to catch that
strange .encode() call error. [jno]

* Progress: Removed an unneeded if. [Juan A. Moya Vicén]

* Progress: Fixes for the previous commit after extensive testing:     -
Fixed the index computation for the rotating cache of Snapshots     -
Moved the start point for the Log progress thread after a proper
computation of the starting volume in case of restart, and adapted
code for it. [Juan A. Moya Vicén]

* Progress: Cover the sigtar and manifest upload with the progress
reporting. Now the last 1% will be dedicated to this upload and
properly report stallment when network goes off while this happens. [Juan A. Moya Vicén]

* Progress: Fixed a missing condition for when the progress flag is not
used. [Juan A. Moya Vicén]

* Progress: Cap data progress upload from 0..99% and show 100% only when
sigtar and manifest file has uploaded correctly. [Juan A. Moya Vicén]

* Progress: Avoid completed percentage to drops between backup retries
when backup fails and has to be restarted.           The current
progress is offset by the previous uncompleted backup from the last
volume that upload correctly.           To achieve it, the progress
tracker now snapshots the current progress to the cache each completed
volume, then           recovers this information later when retrying a
failed backup. [Juan A. Moya Vicén]

* Progress: The algorithm now will drop the confidence interval
adaptively when overpassing the 100%. This may happen when the sigma
is large due to a very heterogeneous distribution of the size of
deltas in files. In this case, the C.I. will be drop by half to adapt
to the variability. If it happens again, it will disregard the sigma
and trust the mean only. [Juan A. Moya Vicén]

* Progress: Simplified computation of progress to compute an upper
bound, fit to a smooth curve. This method embraces better more "change
distribution" scenarios and is much simpler to compute. And also, full
backups will assume 1:1 correspondence in change distribution, so
progress bars during full will be computed linearly, which is closer
to reality. [Juan A. Moya Vicén]

* Progress: Reporting speed in bps for log file. [Juan A. Moya Vicén]

* Progress: Changed verbosity to NOTICE, so progress messages appears by
default when --progress flag is on. [Juan A. Moya Vicén]

* Progress: Added average speed to the log file. [Juan A. Moya Vicén]

* Progress: Fixed a typo in if clause. [Juan A. Moya Vicén]

* Progress: Bugfixed a posible division by zero. [Juan A. Moya Vicén]

* Progress: New feature to compute progress of compress & upload files
The heuristics try to infer the ratio between the amount of data
collected     by the deltas and the total size of the changing files.
It also infers the     compression and encryption ration of the raw
deltas before sending them to     the backend.     With the inferred
ratios, the heuristics estimate the percentage of completion     and
the time left to transfer all the (yet unknown) amount of data to
send.     This is a forecast based on gathered evidence. [Juan A. Moya Vicén]

* Paramiko backend, delete(): Terminate when all files have been deleted
successfully. [Tilman Blumenbach]

    Previously, delete() would delete the entire list of files (as expected) and
    then *always* go into its "retry on error" loop, i. e. it would try to delete
    the (now non-existant) files _again_, which obviously always caused it to fail
    eventually.

* Make the Paramiko backend work with Paramiko 1.10.0. [Tilman Blumenbach]

* The fix in revno. 912 didn't take into account that the parameter
"body" passed into request is overloaded, so when it was NULL or of a
type other than file, it would fail.  This checks if "body" is of type
"file" before actually seek()'ing back to the beginning of the file. [Christopher Townsend]

* Fixes the case where the file pointer to the backup file was not being
set back to the beginning of the file when an error occurs.  This
causes subsequent retries to fail with 400 Bad Request errors from the
server.  This is due to a change in revno. 901 where a file handle is
used instead of a bytearray. * Fixes the removal of Content-Length
from the header in revno. 901.  Content-Length is required according
to the Ubuntu One API documentation. [Christopher Townsend]

* Renamed to --compare-data to make it reusable on other actions e.g.
force data comparision on backup runs where files were modified but
mtime was not set properly by buggy software. [ede]

* Add switch --verify-data, to selectively enable formerly always
disabled data comparison on verify runs. [ede]

* Note on first run was added to the man page. [jno]

* THE BACKEND ITSELF HAS BEEN FINALLY ADDED. [jno]

* Man page fixed to mention dpbx: backend. [jno]

* Dropbox backend (dpbx:) has been added. [jno]

* Applied patches from Laszlo Ersek to rdiffdir to "consume a chain of
sigtar   files in rdiffdir delta mode" which supports incremental
sigtar files. [Kenneth Loafman]

* Make \_librsync module compile under Python 3. [Michael Terry]

* Use PyGI instead of older pygobject style for gio backend. [Michael Terry]

* Webdav manpag updates. [ede]

* Add auto-ctrl-c-test.sh to help stress-test restart support. [Michael Terry]

* Move man page changes to a separate uptodate merge branch. [ede]

* Manpage - document ssl cert verification in man page backend.by -
retry\_fatal decorator accepts now premature fatal errors and supplys
a retry\_count instance variable webdavbackend.py - added ssl cert
verification - added http redirect support - added always create new
connection on retrys - much more debug output for problem pinpointing
commandline.py, globals.py - added ssl cert verification switches
errors.py - add FatalBackendError for signalling exactly that. [ede]

* Reconnect on errors as a precaution against ssl errors see
https://bugs.launchpad.net/duplicity/+bug/709973. [ede]

* Use a copy of file1 rather than writing out a new small file so that
it is clearer the first block is skipped rather than the whole file. [Michael Terry]

* Add test to confirm expected behavior if new files appear before we
restart a backup. [Michael Terry]

* Whoops, fix a test I broke with last commit because I didn't add
get\_read\_size to the mock writer. [Michael Terry]

* Fix block-loss when restarting inside a multi-block file due to block
sizes being variable. [Michael Terry]

* Fix block-loss when restarting after a volume ends with a multi-block
file; fixes test\_split\_after\_large() [Michael Terry]

* Fix block-loss when restarting after a volume ends with a small file;
fixes test\_split\_after\_small() [Michael Terry]

* Add more tests for various restart-over-volume-boundary scenarios. [Michael Terry]

* Move non-encryption-specific tests to the right class. [Michael Terry]

* Tests: add a WithoutEncryption class to restarttest.py. [Michael Terry]

* Fixed 1091269 Data corruption when resuming with --no-encryption   -
Patches from Pascual Abellan that make block size consistent and
that add no-encryption option to manual-ctrl-c-test.sh.   - Modified
gpg.py patch to use 64k block size so unit test passes. [Kenneth Loafman]

* Python3 fix reuse normalized url from oauth. [ede]

* Why bother reading when we can deliver a filehandler alltogether. [ede]

* Fix "not bytearray" prevents PUT with python 2.6. [ede]

    conn.request(method, request_uri, body, headers)
      File "/usr/lib/python2.6/httplib.py", line 914, in request
        self._send_request(method, url, body, headers)
      File "/usr/lib/python2.6/httplib.py", line 954, in _send_request
        self.send(body)
      File "/usr/lib/python2.6/httplib.py", line 759, in send
        self.sock.sendall(str)
      File "/usr/lib/python2.6/ssl.py", line 203, in sendall
        v = self.send(data[count:])
      File "/usr/lib/python2.6/ssl.py", line 174, in send
        v = self._sslobj.write(data)

* Don't hang after putting in credentials (cause it silently retries in
background) but go through with backup. [ede]

* Fix imports not being global. [ede]

* Manpage - document Ubuntu One required libs - added continous
contributors and backend author notes. [ede]

    U1backend
    - lazily import non standard python libs

* Clear up PASSPHRASE reusage as sign passphrase minor fixes. [ede]

* Now files are directly uploaded to destination folder/collection. This
also fixes bug that created a copy of all files in the root
folder/collection in Google Drive. [Carlos Abalde]

* Make sure u1backend returns filenames as utf8. [Michael Terry]

* Added --hidden-encrypt-key testcases. [Marcos Lenharo]

* Added more details in man page. [Marcos Lenharo]

* Fixed a typo in man mage. [Marcos Lenharo]

* Allows duplicity to encrypt backups with hidden key ids. See --hidden-
recipient in man gpg(1) [Marcos Lenharo]

* Add correct error code catch only exceptions again. [ede]

* Catch exceptions only. [ede]

* Show error value instead of class. [ede]

* Bugfix: webdav retrying broke on ERRORS like "error: [Errno 32] Broken
pipe" in socket.pyas reported here
https://answers.launchpad.net/duplicity/+question/212966. [ede]

    added a more generalized 'retry_fatal' decorator which makes retrying backend methods even easier

* Avoid using TestCase.addCleanup, which isn't in older python versions. [Michael Terry]

* Nuke tabs. [Kenneth Loafman]

* Don't duplicate a test for whether we should get passphrase in two
places -- one of them will be out of sync. [Michael Terry]

* Allow .netrc auth for lftp backend. [ede]

* More formatting fixes, clarifications in sections EXAMPLES, FILE
SELECTION. [ede]

* Add a cache for password and group lookups.  This significantly
improves runtime with very large password and group configurations. [Steve Atwell]

* Merged in lp:\~mterry/duplicity/u1-ascii-error   - Fix for u1backend
unicode error.  Patch by Paul Barker. [Kenneth Loafman]

* We no longer need to preserve new-sigs in the cache, since we fixed
the bug keeping them on the remote side. [Michael Terry]

* Port u1backend to oauthlib. [Michael Terry]

* Fix U1 backend's ascii error.  Patch by Paul Barker. [Michael Terry]

* Fix python 2.4 vs 2.5 syntax error. [ede]

    File "/usr/lib64/python2.4/site-packages/duplicity/commandline.py", line 188
        return encoding if encoding else 'utf-8'
                         ^
    SyntaxError: invalid syntax

    see
    http://lists.nongnu.org/archive/html/duplicity-talk/2012-10/msg00027.html

* Update CHANGELOG to reflect all bugs fixed. [Kenneth Loafman]

* Remove dist/mkGNUchangelog script.     * Prep files for 0.6.20
release. [Kenneth Loafman]

* Applied patch from az for bug #1066625 u1backend   + add delay between
retries. [Kenneth Loafman]

* Update Changelog.GNU. [Kenneth Loafman]

* U1backend: interpret http code 402 as no-space-left rather than 507. [Michael Terry]

* Update CHANGELOG and Changelog.GNU. [Kenneth Loafman]

* 1039001 --exclude-if-present and --exclude-other-filesystems causes
crash with inaccessible other fs. [Kenneth Loafman]

* 995851 doc improvement for --encrypt-key, --sign-key. [Kenneth Loafman]

* Update Changelog.GNU. [Kenneth Loafman]

* 1066625 ubuntu one backend does not work without gnome/dbus/x11
session. [Kenneth Loafman]

* Updated Changelog.GNU. [Kenneth Loafman]

* Added gdocs, rsync REQUIREMENTS. [ede]

* Some refinements add cloudfiles documentation. [ede]

* Sort urls alphabetically add abs vs. relative file urls. [ede]

* Typo. [ede]

* Minor fix. [ede]

* Some clarifications mostly for ssh pexpect backend. [ede]

* Update Changelog.GNU. [Kenneth Loafman]

* Some clarifications in README. [ede]

* Refactor GnuPGInterface to gpginterface.py reasoning can be found in
README. [ede]

* Update Changelog.GNU. [Kenneth Loafman]

* Place gpg.py tempfiles in duplicity's tmp subfolder which is cleaned
whatever happens. [ede]

* Tests: apparently on hardy chroots, /bin can be smaller than 3MB
compressed, so instead of using /bin in test\_multi\_volume\_failure,
use largefiles. [Michael Terry]

* Tests: whoops, I had accidentally disabled one of the new tests for
ignoring double entries in a tarball. [Michael Terry]

* Tests: don't use subprocess.check\_output, which was only added in
Python 2.7. [Michael Terry]

* Don't use unittest.TestCase.assertSetEqual, which isn't supported in
older Python versions. [Michael Terry]

* Update Changelog.GNU. [Kenneth Loafman]

* Probably fix. [ede]

    File "/usr/local/lib/python2.7/dist-packages/duplicity/backends/_ssh_pexpect.py", line 223, in run_sftp_command
        log.Warn("Running '%s' with commands:\n %s\n failed (attempt #%d): %s" % (commandline, "\n ".join(commands), n, msg))

* Wrap CHANGELOG to col 80. [Kenneth Loafman]

* Update Changelog.GNU. [Kenneth Loafman]

* Gracefully handle multiple duplicate base dir entries in the sigtar;
avoid writing such entries out. [Michael Terry]

* Retry cloudfiles deletes. [Greg Retkowski]

    This will retry cloudfile delete commands with large numbers of
    archive files over mediocre links deletes occasionally fail
    and should be retried.

* Missing space. [ede]

* Disabled hyphenation and block justification for better readablility
of command line examples. - reformatted REQUIREMENTS section for
hopefully better online rendering - minor clarifications. [ede]

* Delete signature files when doing remove-all-but. [Michael Terry]

* Ssh: actually delete all the requested files, not just the first one. [Michael Terry]

* Update Changelog.GNU and CHANGELOG. [Kenneth Loafman]

* Make sure translations are in utf-8. [Michael Terry]

* Fix dates. [Kenneth Loafman]

* Update CHANGELOG and Changelog.GNU to reflect recent changes. Update
location path in mkGNUChangelog.sh. [Kenneth Loafman]

* Use tempfile.TemporaryFile() so unused temp files are deleted
automagically. [edso]

* Propbably solve bug 'Out of space error while restoring a file' see
bug tracker/mailing list
https://bugs.launchpad.net/duplicity/+bug/1005901
http://lists.gnu.org/archive/html/duplicity-talk/2012-09/msg00000.html. [edso]

* Fix rare 'TypeError: encode() argument 1 must be string, not None'
read here http://lists.nongnu.org/archive/html/duplicity-
talk/2012-09/msg00016.html. [edso]

* Log.py: add a couple comments to reserve error codes 126 and 127
because they conflict with running duplicity under pkexec (very
similar to how 255 is reserved because gksu uses it) [Michael Terry]

* Add note on GnuPGInterface and multiple GPG processes. [Kenneth Loafman]

* Fixed ssh/gio backend import warnings  + ssh paramiko backend imports
paramiko lazily now  + gio backend is not imported automatically but
on request when --gio option is used - added a warning when --ssh-
backend is used with an incorrect value. [edso]

* Ssh paramiko backend respects --num-retries now - set retry delay for
ssh backends to 10s - ssh pexpect backend  + sftp part does not claim
'Invalid SSH password' although it's only 'Permission denied' now  +
sftp errors are now more talkative - gpg.py  + commented assert which
broke otherwise working verify run. [edso]

* Add a couple more warning codes for machine consumption of warnings. [Michael Terry]

* Allow answering gio mount questions (albeit naively) [Michael Terry]

* Add missing files. [edso]

* Readd ssh pexpect backend as alternative - added --ssh-backend
parameter to switch between paramiko,pexpect - manpage -- update to
reflect above changes -- added more backend requirements -
Changelog.GNU removed double entries. [edso]

* Update Changelog.GNU. [Kenneth Loafman]

* Changelog entry. [edso]

* Add missing\_host\_key prompt similar to ssh procedure. [edso]

* Fixing most basic stuff. Pending all testing. [Carlos Abalde]

* Changelog entry. [edso]

* Add ssh\_config support (/etc/ssh/ssh\_config + \~/.ssh/config) to
paramiko sshbackend. [edso]

* Empty listbody for enhanced webdav compatibility - bugfix: initial
folder creation on backend does not result in a ResponseNotReady
anymore. [edso]

* Added REQUIREMENTS section - restructure SYNOPSIS/ACTIONS to have
commands sorted by backup lifecycle - added restore and some more
hints when --time or --file-to-restore are supported - replaced scp://
with sftp:// in examples as this is the suggested protocol anyway -
added an intro text to ACTIONS section - adapted --ssh-askpass
description to latest functionality. [edso]

* Changes for 0.6.18. [kenneth@loafman.com]

* Use correct dir name for cleanup. [kenneth@loafman.com]

* Adjust roottest.py to new test dir structure. [kenneth@loafman.com]

* Changes for 0.6.18. [kenneth@loafman.com]

* Some code/import changes to make the ssh and boto backends compatible
with Python 2.4. [kenneth@loafman.com]

* Changes for 0.6.18. [kenneth@loafman.com]

* Changes for 0.6.18. [kenneth@loafman.com]

* Fix for bug 931175 'duplicity crashes when PYTHONOPTIMIZE is set' [kenneth@loafman.com]

* Remove duplicate line. [kenneth@loafman.com]

* File /etc/motd may not exist in test environment.  Use \_\_file\_\_
instead to point to a known plaintext source file. [kenneth@loafman.com]

* Remove tests for 884371.  Can't test that yet. [kenneth@loafman.com]

* Raise log level on backend import failure so it will be visible under
default conditions. [kenneth@loafman.com]

* Fix for bug 929465 -- UnsupportedBackendScheme: scheme not supported
in url: scp://u123@u123.example.com/foo/ [kenneth@loafman.com]

* Applied patch from 930727. [kenneth@loafman.com]

    ftpsbackend should respect num_retries for ftp commands

* Drop unused pexpect.py. [Michael Terry]

* A couple small code fixes to help tests pass. [Michael Terry]

* Applied patch by Alexander Zangerl from bug 909031, "SSH-Backend:
Creating dirs separately causes a permissons-problems". [Kenneth Loafman]

* Change the way the file\_naming regular expressions are created to
support --file-prefix option. [nguyenqmai]

* Don't have TarFile objects cache member TarInfo objects; it takes too
much space. [Michael Terry]

* Always delay a little bit when a backend gives us errors. [Michael Terry]

* Changelog update - fixed comment. [Tobias Genannt]

* Added option to not compress the backup, when no encryption is
selected. [Tobias Genannt]

* Added patch for testing of bug 884371, 'Globbing patterns fail to
include some files if prefix is "**"' [kenneth@loafman.com]

* Applied patch from 916689 "multipart upload fails on python 2.7.2" [kenneth@loafman.com]

* Applied patch from 884638 and fixed version check to allow Python 2.5
and above. [kenneth@loafman.com]

* Resuming an incremental results in a 'Restarting backup, but current
encryption settings do not match original settings' error because
curtime is incorrectly set away from previous incremental value. [Michael Terry]

* Tests: make other-filesystem check more robust against certain
directories being mounts or not. [Michael Terry]

* Tests: use backup source that is more likely to be larger than 1M
compressed. [Michael Terry]

* Tests: add delay between backups to avoid assertion error. [Michael Terry]

* Fix extraneous '.py' that keeps import from working. [Kenneth Loafman]

* Changes for 0.6.17. [Kenneth Loafman]

* Not used. [Kenneth Loafman]

* Run tests using virtualenv for each. [Kenneth Loafman]

* Make adjustments for the new structure. - Adjust boto requirements to
be 1.6a or higher. - Cleanup install scripts. [Kenneth Loafman]

* Some doc changes including new requirements. [Kenneth Loafman]

* Don't assume dir location for Python. [Kenneth Loafman]

* Adds --rsync-options to command line Allows uer to pass additional
options to the rsync backend Commit include paragraph in man page, new
global variable, and the small changes needed to the backend itself. [Eliot Moss]

* Check that we have the right passphrase when restarting a backup. [Michael Terry]

* 411145  Misleading error message: "Invalid SSH password" [Kenneth Loafman]

* Split botobackend.py into two parts, \_boto\_single.py which is the
older single-processing version and \_boto\_multi.py which is the
newer multi-processing version.  The default is single processing and
can be overridden with --s3-use-multiprocessing. [Kenneth Loafman]

* The function add\_filename was rejecting anything non-encrypted as a
legit file.  This fixes that problem and the bug. [Kenneth Loafman]

* Fix to allow debugging from pydev.  The check for --pydevd must be
done after command line is parsed. [Kenneth Loafman]

* Changed functions working with UTC time file format from localtime()
to gmtime() and timegm() [Ivan Gromov]

* Fixed time\_separator global attribute usage in some tests. [ivan.gromov]

* Made proper setUp method for tests in dup\_timetest.py. [Ivan Gromov]

* Remove random\_seed from VCS, adjust .bzrignore. [Kenneth Loafman]

* Remove localbackend.testing\_in\_progress since all it accomplished
was to make the local backend test fail. [ken]

* Make tarball layout match bzr layout much more closely; ship tests in
tarballs and adjust things so that they can work. [Michael Terry]

* Rename auto/ to tests/ [Michael Terry]

* Undo accidental changes to run-tests and convert pathtest and
rdiffdirtest (for both of which, I uncommented a failing test I didn't
understand) [Michael Terry]

* Move some more custom scripts to manual/ [Michael Terry]

* Move some things around; converge on one script for running any kind
of test or list of tests. [Michael Terry]

* Convert patchdirtest to auto; rip out its root-requiring tests and
move them to roottest script; fix roottest script to work now with the
new rootfiles.tar.gz, whoops. [Michael Terry]

* Convert finaltest to auto; workaround an ecryptfs bug with long
filenames in the test. [Michael Terry]

* Drop state file random\_seed from test gnupg home. [Michael Terry]

* Convert gpgtest to auto; add testing keys to the suite, so testers
don't have to make their own; delete gpgtest2, as it didn't do
anything. [Michael Terry]

* Drop unused darwin tarball and util file. [Michael Terry]

* Convert GnuPGInterfacetest and dup\_timetest to auto. [Michael Terry]

* Convert file\_namingtest, parsedurltest, and restarttest to auto. [Michael Terry]

* Convert manifesttest, selectiontest, and test\_tarfile to auto. [Michael Terry]

* Convert cleanuptest, dup\_temptest, and misctest to auto. [Michael Terry]

* Convert statisticstest to auto; make sure tests are run in English and
in US/Central timezone. [Michael Terry]

* Convert statictest to auto. [Michael Terry]

* Convert tempdirtest to auto. [Michael Terry]

* Convert logtest to auto. [Michael Terry]

* Convert lazytest to auto. [Michael Terry]

* Clean up run scripts a little bit, rename testfiles.tgz to
rootfiles.tgz. [Michael Terry]

* Make diffdirtest auto. [Michael Terry]

* Make badupload auto. [Michael Terry]

* Make collectionstest auto. [Michael Terry]

* Move all manual tets into their own subdirectory. [Michael Terry]

* -- Applied patch 0616.diff from bug 881070. -- Fixed compile issues in
reset\_connection. -- Changed 'url' to 'parsed\_url' to make
consistent with backends. [ken]

* Changes for 0.6.16. [ken]

* Changes for 0.6.16. [ken]

* Merge in lp:\~duplicity-team/duplicity/po-updates. [Kenneth Loafman]

* Remove Eclipse stuff from bzr. [Kenneth Loafman]

* Update .pot and add all languages to LINGUAS list file. [kenneth@loafman.com]

* Some links for UnicodeDecodeError. [edso]

* Fix UnicodeDecodeError: 'ascii' codec can't decode byte on command
usage. [edso]

* Remove evil tab characters causing indent errors. [kenneth@loafman.com]

* 838162  Duplicity URL Parser is not parsing IPv6 properly. [kenneth@loafman.com]

* 676109 Amazon S3 backend multipart upload support. [kenneth@loafman.com]

* 739438 Local backend should always try renaming instead of copying. [kenneth@loafman.com]

* Updated --verbosity symmetric and signing. [edso]

    minor fixes

* Checkpoint. [kenneth@loafman.com]

* Make sure sig\_path is a regular file before opening it. [Michael Terry]

* Gpg2 will not get the passphrase from gpg-agent if --passphrase-fd is
specified. Added tests to disable passphrase FD if use\_agent option
is true. [Ross Williams]

* Use cached size of original upload file rather than grabbing it after
put() call.  Some backends invalidate the stat information after put
(like local backend after a rename) [Michael Terry]

* Allow upgrading partial chain encryption status. [Michael Terry]

* Make tarfile.py 2.4-compatible. [Michael Terry]

* Use python2.7's tarfile instead of whichever version comes with user's
python. [Michael Terry]

* Use a proper fake TarFile object when reading an empty tar. [Michael Terry]

* Handle empty headers better than passing ignore\_zeros -- instead
handle ReadErrors. [Michael Terry]

* And update trailing slashes in test too. [Michael Terry]

* Fix how trailing slashes are used to be cross-python-version
compatible. [Michael Terry]

* Whoops, forgot an import. [Michael Terry]

* Handle different versions of tarfile. [Michael Terry]

* First pass at dropping tarfile. [Michael Terry]

* Make query\_info a little easier to use by guaranteeing a well-
formated return dictionary. [Michael Terry]

* Add rackspace query support. [Michael Terry]

* Add query support to boto backend. [Michael Terry]

* Make clear the difference between sizes from errors and backends that
don't support querying. [Michael Terry]

* Add query\_info support to u1 backend. [Michael Terry]

* First pass at checking volume upload success. [Michael Terry]

* Cloudfiles: allow listing more than 10k files. [Michael Terry]

* Drop sign passphrase verification prompt. [edso]

* Bugfix of rev767 on using sign key duplicity claimed 'PASSPHRASE
variable not set' [edso]

* Sync with master. [Kenneth Loafman]

* Remove another non-2.4-ism I introduced. [Michael Terry]

* Changes for 0.6.15. [Kenneth Loafman]

* Fixes to unit tests to support SIGN\_PASSPHRASE. [Kenneth Loafman]

* Typo fix. [edso]

* Numowner & hash mismatch verbosity. [edso]

* Remove use of virtualenv. [Kenneth Loafman]

* Ignore ENOENT (file missing) errors where it is safe. - Set minimum
Python version to 2.4 in README. [Kenneth Loafman]

* 824678     0.6.14 Fails to install on 8.04 LTS (Hardy) [Kenneth Loafman]

* 823556     sftp errors after rev 740 change. [Kenneth Loafman]

* Fixed indentation: 2 to 4 spaces. [Carlos Abalde]

* Fetching user password correctly (i.e. not using directly
self.parsed\_url.password) [Carlos Abalde]

* Now using backend.retry(fn) decorator to handle API retries. [Carlos Abalde]

* Added subfolders support + several minor improvements and fixes. [Carlos Abalde]

* Added support for captcha challenges. [Carlos Abalde]

* Replacing get\_doclist by get\_everything in put & delete methods.
Raisng BackendException's in constructor. [Carlos Abalde]

* Replaces get\_doclist by get\_everything when retrieving remote list
of files in backup destination folder. [Carlos Abalde]

* Added authentication instruction for accounts with 2-step verification
enabled. [Carlos Abalde]

* A couple of assert + missing local\_path.setdata on remote file get. [Carlos Abalde]

* Better error logging + retries for each API op. [Carlos Abalde]

* Improved upload: check duplicated file names on destination folder +
better error handling. [Carlos Abalde]

* Improved API error handling. [Carlos Abalde]

* Checking Google Data APIs Python libraries are present. [Carlos Abalde]

* Fixed URI format. [Carlos Abalde]

* First usable prototype. [Carlos Abalde]

* Some u1 backend fixes: handle errors 507 and 503; add oops-id to
message user sees so U1 folks can help. [Michael Terry]

* Merged in lp:\~ed.so/duplicity/encr-sign-key2. [Kenneth Loafman]

* Introduce --encrypt-sign-key parameter  - duplicity-
bin::get\_passphrase          skip passphrase asking and reuse
passphrase if          sign-key is also an encrypt key and     a
passphrase for either one is already set    - add \_() gettext to text
in duplicity-bin::get\_passphrase    - document changes and minor
additions in manpage. [ede]

* Don't try to delete partial manifests from backends. [Michael Terry]

* Retry operations on u1 backend. [Michael Terry]

* When copying metadata from remote to local archive, first copy to a
temporary file then move over to archive. [Michael Terry]

* Report whether a chain is encrypted or not. [Michael Terry]

* Be more careful about what we try to synchronize. [Michael Terry]

* Pay attention to local partials when sync'ing metadata and make sure
we don't end up with three copies of a metadata file. [Michael Terry]

* Ignore ENOTCONN when scanning files. [Michael Terry]

* Really restore threaded\_waitpid(). [Kenneth Loafman]

* Also guard the recursive call. [Michael Terry]

* Guard tarinfo object from being None. [Michael Terry]

* Detabify.  Tabs are evil. [Kenneth Loafman]

* Restore previous version with threaded\_waitpid(). [Kenneth Loafman]

* U1backend: ignore file-not-found errors on delete. [Michael Terry]

* Update to duplicity messages. [Kenneth Loafman]

* 777377     collection-status asking for passphrase. [Kenneth Loafman]

    Various fixes to unit tests to comprehend changes made.

* Duplicity.1: move information about the PASSPHRASE and
SIGN\_PASSPHRASE   environment variables to the Environment Variables
section - duplicity.1: add information about the limitation on using
symmetric+sign to the bugs section - In the passphrase retrieval
function get\_passphrase, do not switch from   "ask password without
verifying" to ask+verify if the passphrase was   empty - Allow an
empty passphrase for signing key - Make clear in the verification
prompt whether the encryption passphrase   or the signing passphrase
is being confirmed - Fix passphrase retrieval for sym+sign (duplicity-
bin and gpg.py) - Allow sym+sign with limitation (see comments and
manual page) [Lekensteyn]

* Invalid function description fixed for get\_passphrase in duplicity-
bin - function get\_passphrase in duplicity-bin accepts argument
"for\_signing"   which indicates that a passphrase for a signing key
is requested - introduces the SIGN\_PASSPHRASE environment variable
for passing a   different passphrase to the signing key - commandline
option --encrypt-secret-keyring=path introduced to set a   custom
location for the secret keyring used by the encryption key - manual
page updated with SIGN\_PASSPHRASE and --encrypt-secret-keyring - ask
for a new passphrase if the passphrase confirmation failed to
prevent an endless retype - improved some comments in the code - due
to the difference in the handling of the signing and encryption
passphrase, the passphrase is asked later in the duplicity-bin. [Lekensteyn]

* Always catch Exceptions, not BaseExceptions. [Michael Terry]

* Checkpoint. [Kenneth Loafman]

* 794123     Timeout on sftp command 'ls -1' [Kenneth Loafman]

* Checkpoint. [Kenneth Loafman]

* 487720     Restore fails with "Invalid data - SHA1 hash mismatch" [Kenneth Loafman]

* Fixed boolean swap made when correcting syntax. [Kenneth Loafman]

* Fix syntax for Python 2.4 and 2.5. [Kenneth Loafman]

* Fix syntax for Python 2.4 and 2.5. [Kenneth Loafman]

* Fix CHANGELOG. [Kenneth Loafman]

* 782337     sftp backend cannot create new subdirs on new backup. [Kenneth Loafman]

* 782294     create tomporary files with sftp. [Kenneth Loafman]

* Move logging code up to retry decorator; fixes use of 'n' variable
where it doesn't belong. [Michael Terry]

* Add retry decorator for backend functions; use it for giobackend; add
retry to giobackend's list and delete operations. [Michael Terry]

* U1: allow any success status, not just 200. [Michael Terry]

* Checkpoint. [Kenneth Loafman]

* Giobackend: use name, not display name to list files. [Michael Terry]

* Fix MachineFilter logic to match new level name code. [Michael Terry]

* Cautiously avoid using levelname directly in log module.  It can be
adjusted by libraries. [Michael Terry]

* Update man page. [Michael Terry]

* Drop test file. [Michael Terry]

* Further fixups. [Michael Terry]

* Further upload work. [Michael Terry]

* Start of u1 support. [Michael Terry]

* 792704     Webdav(s) url scheme lacks port support. [Kenneth Loafman]

* 782321     duplicity sftp backend should ignore removing a file which
is not there. [Kenneth Loafman]

* 778215     ncftpls file delete fails in ftpbackend.py. [Kenneth Loafman]

* 507904     Cygwin: Full Backup fails with "IOError: [Errno 13]
Permission denied" [Kenneth Loafman]

* 761688     Difference found: File X has permissions 666, expected 666. [Kenneth Loafman]

* 739438     [PATCH] Local backend should always try renaming instead of
copying. [Kenneth Loafman]

* 705499     "include-filelist-stdin" not implemented on version 0.6.11. [Kenneth Loafman]

* As restoring is non-destructive by default (overideable with --force)
there is no need to raie fata errors if not supported in/exclude
parameters are given as parameters. see also:
http://lists.gnu.org/archive/html/duplicity-talk/2011-04/msg00010.html. [ed]

* 512628     --exclude-filelist-stdin and gpg error with/without
PASSPHRASE. [Kenneth Loafman]

* 512628     --exclude-filelist-stdin and gpg error with/without
PASSPHRASE. [Kenneth Loafman]

* Insure Python 2.4 compatible. [Kenneth Loafman]

* 433591  AttributeError: FileobjHooked instance has no attribute 'name' [Kenneth Loafman]

* Link sftp to ssh backend, thus enabling sftp:// urls modified
explanation in manpage minor changes in manpage. [ed]

* Boto has refactored too many times, so back off and just use Exception
rather than searching. [Kenneth Loafman]

* Boto moved S3ResponseError, so allow for different imports. [Kenneth Loafman]

* Changes for 0.6.13. [Kenneth Loafman]

* Changes for 0.6.13. [Kenneth Loafman]

* Changes for 0.6.13. [Kenneth Loafman]

* Check for presence of bucket before trying to create. [Kenneth Loafman]

* 579958  Assertion error "time not moving forward at appropriate pace" [Kenneth Loafman]

* Add in ftpsbackend.py.  Missed it. [Kenneth Loafman]

* 613244     silent data corruption with checkpoint/restore. [Kenneth Loafman]

* Add a manual test for Ctrl-C interrupts.  This could be automated, but
I find that the old hairy eyeball works quite well as is. [Kenneth Loafman]

* Use python-virtualenv to provide a well-defined environment for
testing multiple versions of Python. [Kenneth Loafman]

* Add (undocumented) option --pydevd to allow easier debugging when
executing long chains of duplicity executions. [Kenneth Loafman]

* Remove threaded\_waitpid().  We still need GnuPGInterface because of
the shift bug in the return code and the ugly mix of tabs and spaces.
All has been reported to the author. [Kenneth Loafman]

* Replace 2.5 'except...as' syntax. [Kenneth Loafman]

* Changes for 0.6.12. [Kenneth Loafman]

* Various fixes for testing.  All tests pass completely. [Kenneth Loafman]

* Add test for new ftps backend using lftp. [Kenneth Loafman]

* Some FTP sites return 'total NN' in true ls fashion, so ignore line
during listing of files. [Kenneth Loafman]

* Fix typo on fix for 700390. [Kenneth Loafman]

* Miscellaneous fixes for testing. [Kenneth Loafman]

* 700390  Backup fails silently when target is full (sftp, verbosity=4) [Kenneth Loafman]

* 581054  Inverted "Current directory" "Previous directory" in error
message. [Kenneth Loafman]

* 626915     ftps support using lftp (ftpsbackend) [Kenneth Loafman]

* 629984  boto backend uses Python 2.5 conditional. [Kenneth Loafman]

* 670891  Cygwin: TypeError: basis\_file must be a (true) file, while
restoring inremental backup. [Kenneth Loafman]

* 655797     symbolic link ownership not preserved. [Kenneth Loafman]

* Lp:\~blueyed/duplicity/path-enodev-bugfix. [Kenneth Loafman]

* Merged: lp:\~blueyed/duplicity/path-enodev-bugfix. [Kenneth Loafman]

* 629136     sslerror: The read operation timed out with cf. [Kenneth Loafman]

* 704314     Exception in log module. [Kenneth Loafman]

* 486489  Only full backups done on webdav. [Kenneth Loafman]

* 620163  OSError: [Errno 2] No such file or directory. [Kenneth Loafman]

* Use log error codes for common backend errors. [Michael Terry]

* 681980     Duplicity 0.6.11 aborts if RSYNC\_RSH not set. [Kenneth Loafman]

* Changes for 0.6.11. [Kenneth Loafman]

* Changes for 0.6.11. [Kenneth Loafman]

* Add --s3-unencrypted-connection (bug 433970) [Martin Pool]

* Solve bug 631275 rsync 3.0.7 persists on either rsync:// \_or\_ ::
module notation both together and it interpretes it as a dest for rsh. [ed]

* Protect rsync from possibly conflicting remote shell environment
setting. [ed]

* Restored backend:subprocess\_popen\_* methods moved ncftpls workaround
into ftpbackend introduced new backend:popen\_persist\_breaks setting
for such workarounds enhanced backend:munge\_password rsyncbackend:
rsync over ssh does not ask for password (only keyauth supported) [ed]

* Survive spaces in path on local copying with encryption enabled. [ed]

* Allow signing of symmetric encryption. [ed]

* Catch "Couldn't delete file" response in sftp commands. [Daniel Hahler]

* When using listmatch filenames are now unqouted so colons and other
special characters don't cause problems. [Tomaž Muraus]

    Also all the tests now pass.

* Added test for SpiderOak backend (it should probably just fail in most
cases since the API is still very unstable). [Tomaž Muraus]

* Add ability to retry failed commands. [Tomaž Muraus]

* Handle exceptions when listing files and display coresponding HTTP
status code on HTTPError exception. [Tomaž Muraus]

* First version of SpiderOak DIY backend. [Tomaž Muraus]

    Still very rough and needs tests.

* Support new backend-error log codes. [Michael Terry]

* Adding conftest.py for py.test configuration hooks (right now just
setting up temporary directories) [Larry Gilbert]

* Use py.path to simplify a little. [Larry Gilbert]

* Don't try to change dirs in cleanup\_test\_files for now. Actually,
this file probably won't be here much longer. [Larry Gilbert]

* Fix non-root-based test skipping. [Larry Gilbert]

* Expose test files' root directory as config.test\_root. [Larry Gilbert]

* New helper module for tests; have backendtest.py make use of it. [Larry Gilbert]

* Refactored.  Put in py.test.skip to skip tests when tarfile can't be
used. [Larry Gilbert]

* Commit.py already adjusts sys.path, so anything that imports commit
doesn't need to. [Larry Gilbert]

* Allow testing/config.py to find duplicity even when run outside
testing/. Added a missing import. [Larry Gilbert]

* 637556     os.execve should get passed program as first argument. [Kenneth Loafman]

* Changes for 0.6.10. [Kenneth Loafman]

* Replace ternary operator with simple if statement.  Python 2.4 does
not support the ternary operator. [Kenneth Loafman]

* Upgrade setup dependency to Python 2.4 or later. [Kenneth Loafman]

* Changes for 0.6.10. [Kenneth Loafman]

* 612714     NameError: global name 'parsed\_url' is not defined. [Kenneth Loafman]

* 589495     duplicity --short-filenames crashes with TypeError. [Kenneth Loafman]

* 589495     duplicity --short-filenames crashes with TypeError. [Kenneth Loafman]

* Fix remove-older-than which would no longer work Differentiate the
function name from global option name for remove\_all\_but\_n\_full. [olivier]

* Added bits of manpage. [olivier]

* Adding the remove-all-inc-of-but-n-full variant to
remove\_all\_but\_n\_full() : remove only incremental sets from a
backup chain selected as older than the n last full. [olivier]

* Adding the 2 new remove-all-but commands as global markers. [olivier]

* Adding new remove-all-inc-of-but-n-full command as a variant of
remove-all-but-n-full. [olivier]

* Fix small typo in comments. [olivier]

* 613448     ftpbackend fails if target directory doesn't exist. [Kenneth Loafman]

* 615449     Command-line verbosity parsing crash. [Kenneth Loafman]

* Man page improvements and clarification. [Kenneth Loafman]

* Final changes for 0.6.09. [Kenneth Loafman]

* 582962     Diminishing performance on large files. [Kenneth Loafman]

* Fix to warning message in sshbackend. [Kenneth Loafman]

* Upgraded tahoebackend to new parse\_url. [Kenneth Loafman]

* Merged in lp:\~duplicity-team/duplicity/po-updates. [Kenneth Loafman]

* 502609     Unknown error while uploading duplicity-full-signatures. [Kenneth Loafman]

* Support new backend-error log codes. [Michael Terry]

* Don't crash when asked to encrypt, but not passed any gpg\_options.
my bad. [Michael Terry]

* #532051 rdiffdir attempts to reference undefined variables with some
command arguments. [Kenneth Loafman]

* #519110 Need accurate man page info on use of scp/sftp usage. [Kenneth Loafman]

* Use global gpg options. [Michael Terry]

* Fix time command line handling. [Michael Terry]

* And handle initial, empty value for extend commandline actions. [Michael Terry]

* Fix crash on empty gpg-options argument. [Michael Terry]

* #520470 - Don't Warn when there's old backup to delete. [ken]

* Patch #505739 - "sslerror: The read operation timed out" with S3. [ken]

* Patch 522544 -- OSError: [Errno 40] Too many levels of symbolic links. [ken]

* Patched #497243 archive dir: cache desynchronization caused by remove* [ken]

* Logging: fix logging to files by opening them with default of 'a' not
'w' [Michael Terry]

* Merge lp:\~mterry/duplicity/rename. [Michael Terry]

* Make a comment reserving 255 as an error code (used by gksu) [Michael Terry]

* Merge lp:\~mterry/duplicity/optparse. [Michael Terry]

* Remove antiquated file. [ken]

* Remove requirement for GnuPGInterface, we have our own. [ken]

* 576564     username not url decoded in backend (at least rsync) [ken]

* 579958     Assertion error "time not moving forward at appropriate
pace" [Kenneth Loafman]

    setcurtime() must change with time changes.

* 550455           duplicity doesn't handle with large files well
(change librsync.SigGenerator.sig\_string to a list) [ken]

* Changes for 0.6.08b. [Kenneth Loafman]

* Manually apply patch from http://bazaar.launchpad.net/\~duplicity-
team/duplicity/0.7-series/revision/637 which did not make it into 0.6. [Kenneth Loafman]

* Changes for 0.6.08a. [Kenneth Loafman]

* Changes for 0.6.08. [Kenneth Loafman]

* #532051 rdiffdir attempts to reference undefined variables with some
command arguments. [Kenneth Loafman]

* #519110 Need accurate man page info on use of scp/sftp usage. [Kenneth Loafman]

* Use global gpg options. [Michael Terry]

* Fix time command line handling. [Michael Terry]

* And handle initial, empty value for extend commandline actions. [Michael Terry]

* Fix crash on empty gpg-options argument. [Michael Terry]

* Changes for 0.6.07. [ken]

* #520470 - Don't Warn when there's old backup to delete. [ken]

* Patch #505739 - "sslerror: The read operation timed out" with S3. [ken]

* Patch 522544 -- OSError: [Errno 40] Too many levels of symbolic links. [ken]

* Patched #497243 archive dir: cache desynchronization caused by remove* [ken]

* Logging: fix logging to files by opening them with default of 'a' not
'w' [Michael Terry]

* Make a comment reserving 255 as an error code (used by gksu) [Michael Terry]

* Patch 501093 SSHBackend doesn't handle spaces in path. [ken]

* Try again -- remove Eclipse/PyDev control files from bzr. [ken]

* Eclipse settings should not be in bzr. [ken]

* No longer needed. [ken]

* Fix real errors found by PyLint.  Remove unneeded includes.  Tag
spurious errors so they don't annoy. [ken]

* Fix problem in put() where destination filename was not being passed
properly. [ken]

* Add --rename argument. [Michael Terry]

* Add back accidentally-dropped --use-scp option from commandline merge. [Michael Terry]

* Fix CHANGELOG. [ken]

* Merged in lp:\~mterry/duplicity/typos. [ken]

* Whoops, and this typo. [Michael Terry]

* Fix some typos found when using pydev+eclipse. [Michael Terry]

* 459511 --tempdir option doesn't override TMPDIR. [ken]

* 487686 re-add scp backend and make available via command line option
Option --use-scp will use scp, not sftp, for get/put operations. [ken]

* Applied patch 467391 to close connection on a 401 and retry with
authentication credentials. [ken]

* CVS no longer used, so no longer needed. [ken]

* Checkpoint. [Kenneth Loafman]

* I18nized a few error messages in duplicity.selection. [Larry Gilbert]

* More strings internationalized in asyncscheduler and commandline. [Larry Gilbert]

* Warn if we don't have signatures for the given date period. [Michael Terry]

* Allow deleting old signatures with cleanup --extra-clean. [Michael Terry]

* Don't delete signature chains for old backups; allow listing old
backup chain files. [Michael Terry]

* Add missing par2\_utils.py to dist tarball. [Michael Terry]

* Remove unused \_\_future\_\_ imports. [Kenneth Loafman]

* Add entry for patches from Stéphane Lesimple for par2. [Kenneth Loafman]

* Applied patch from Stéphane Lesimple found at:
https://bugs.launchpad.net/duplicity/+bug/426282/comments/5 patch
skips the par2 files when building up the sets and chains of backups. [Kenneth Loafman]

* Applied patch from Stéphane Lesimple found at:
https://bugs.launchpad.net/duplicity/+bug/426282/comments/4 patch
avoids storing all the par2 files into the local cache. [Kenneth Loafman]

* Fixed 435975 gpg asks for password in 0.6.05, but not in 0.5.18. [Kenneth Loafman]

* Ugh, I'm the worst; add missing import. [Michael Terry]

* Add extra information to the 'hostname changed' log message, split it
from the 'source dir changed' message. [Michael Terry]

* Fix problems with unittests under Jaunty.  It appears that redirection
in os.system() has changed for the worse, so a workaround for now. [Kenneth Loafman]

    Fix problem in restart where there were no manifest entries and no
    remote volumes stored.  We clean out the partial and restart.

* Applied "426282 [PATCH] par2 creating support", corrected some coding
format issues and made sure all unit tests passed. [Kenneth Loafman]

* Clean up testing run scripts. [Kenneth Loafman]

* * 422477 [PATCH] IMAP Backend Error in delete() [Kenneth Loafman]

* Whoops, remove debug code. [Michael Terry]

* Don't set xdg dirs in duplicity-bin now that globals.py is restored. [Michael Terry]

* Use defaults from globals.py for commandline options. [Michael Terry]

* Fix an undefined variable usage. [Michael Terry]

* Fix a few typos. [Michael Terry]

* Whoops, and this typo. [Michael Terry]

* Fix some typos found when using pydev+eclipse (backported from 0.7
line) [Michael Terry]

* Fix typo with log-fd support. [Michael Terry]

* First pass at getopt->optparse conversion. [Michael Terry]

* Remove antiquated file. [ken]

* Remove requirement for GnuPGInterface, we have our own. [ken]

* 459511 --tempdir option doesn't override TMPDIR. [ken]

* 487686 re-add scp backend and make available via command line option
Option --use-scp will use scp, not sftp, for get/put operations. [ken]

* Applied patch 467391 to close connection on a 401 and retry with
authentication credentials. [ken]

* Checkpoint. [Kenneth Loafman]

* Changes for 0.6.06. [Kenneth Loafman]

* Merge old-chain signature work from 0.7 branch; keep old sigs around,
allow listing them, warn if a too-old listing is requested. [Michael Terry]

* Remove .cvsignore. [kenneth@loafman.com]

* Remove unused \_\_future\_\_ imports. [Kenneth Loafman]

* Fixed 435975 gpg asks for password in 0.6.05, but not in 0.5.18. [Kenneth Loafman]

* Ugh, I'm the worst; add missing import. [Michael Terry]

* Whoops, use error code 42, not 41 -- that's for par2. [Michael Terry]

* Add extra information to the 'hostname changed' log message, split it
from the 'source dir changed' message. [Michael Terry]

* Fix problems with unittests under Jaunty.  It appears that redirection
in os.system() has changed for the worse, so a workaround for now. [Kenneth Loafman]

    Fix problem in restart where there were no manifest entries and no
    remote volumes stored.  We clean out the partial and restart.

* Add some machine codes to various warnings when iterating over source
files. [Michael Terry]

* Additional Portuguese and brand-new Bulgarian translations. [Larry Gilbert]

* Clean up testing run scripts. [Kenneth Loafman]

* * 422477  [PATCH] IMAP Backend Error in delete() [Kenneth Loafman]

* Change message "--cleanup option" to "'cleanup' command" [Larry Gilbert]

* Translation of Spanish and Portuguese has begun. [Larry Gilbert]

* Updated existing PO files with Rosetta translations. [Larry Gilbert]

* When generating PO[T] files, only use code comments starting with
"TRANSL:" for notes to the translators.  "TRANSL:" is filtered out of
the POT file with sed after it's generated. [Larry Gilbert]

* Applied patches from Kasper Brand that fixed device file handling.
http://lists.gnu.org/archive/html/duplicity-talk/2009-09/msg00001.html. [Kenneth Loafman]

* Changes for 0.6.05. [Kenneth Loafman]

* Test separate filesystems using /dev instead of /proc (more widely
used) [Larry Gilbert]

* Dd on Darwin (and FreeBSD?) doesn't like e.g. "bs=1K", so changed it
to "bs=1024" [Larry Gilbert]

* "cp -pR" seems to be a better analogue to "cp -a".  This may not be
perfect but it won't hang on a fifo copy like "cp -pr". [Larry Gilbert]

* Got test\_get\_extraneous working in collectionstests.py. [Larry Gilbert]


## rel.1.2.3 (2023-05-09)

### New

* Xorriso backend for optical media. [T. K]

* Onedrive for Business Support. [Tobias Simetsreiter]

### Changes

* Fix tools release-prep & makechangelog. [Kenneth Loafman]

* Fix tools/release-prep. [Kenneth Loafman]

* Run po/update-pot. [Kenneth Loafman]

* Update readthedocs.yaml. [Kenneth Loafman]

* More ReadTheDocs changes. [Kenneth Loafman]

* More ReadTheDocs changes. [Kenneth Loafman]

* More ReadTheDocs changes. [Kenneth Loafman]

* More ReadTheDocs changes. [Kenneth Loafman]

* More ReadTheDocs changes. [Kenneth Loafman]

* More ReadTheDocs changes. [Kenneth Loafman]

* More ReadTheDocs changes. [Kenneth Loafman]

* Change readthedocs.yaml. [Kenneth Loafman]

* Change readthedocs.yaml. [Kenneth Loafman]

* Update CHANGELOG.md. [Kenneth Loafman]

* Fix spelling errors. [Barak A. Pearlmutter]

* Chg:pkg:  Cleanup.  Add 'unsquashfs -l' test from @ede. [Kenneth Loafman]

* Update Makefile 'make clean' list. [Kenneth Loafman]

* Fix run website ci call after pushes/releases. [ede]

    [skip_tests]

* Update version for Launchpad. [Kenneth Loafman]

### Fix

* Use cryptography == 3.4.8. [Kenneth Loafman]

    Fixes #703 - use same version as python3-cryptography in apt.

* Warn rather than fail on op-not-supported restore errors. [Michael Terry]

* Fixes #701 - unable to resume full backup to B2. [Kenneth Loafman]

    Now tries .name and .uc_name before failing.

* Fixes #698 - backups without GPG decryption key. [Kenneth Loafman]

    Added option --no-check-remote to skip checking the
    remote manifest.  The default is to check.

* Fixes #698 - backups without GPG decryption key. [Kenneth Loafman]

    Added option --no-check-remote to skip checking the
    remote manifest.  The default is to check.

* Fixes #686 - PCA backend does not unseal volumes. [Kenneth Loafman]

    Patch supplied by Bertrand Marc, user @bmarc.

* Skip test\_path::test\_compare on non-native. [Kenneth Loafman]

    Skip on GitLab and Launchpad build systems.
    Works fine on Linux and macOS.

* Skip test\_path::test\_compare on non-native. [Kenneth Loafman]

    Skip on GitLab and Launchpad build systems.
    Works fine on Linux and macOS.

* Skip test\_path::test\_compare on non-native. [Kenneth Loafman]

    Skip on GitLab and Launchpad build systems.
    Works fine on Linux and macOS.

* Skip test\_path::test\_compare on non-native. [Kenneth Loafman]

    Skip on GitLab and Launchpad build systems.
    Works fine on Linux and macOS.

* Skip test\_path::test\_compare on non-native. [Kenneth Loafman]

    Skip on GitLab and Launchpad build systems.
    Works fine on Linux and macOS.

* Skip test\_path::test\_compare on non-native. [Kenneth Loafman]

    Skip on GitLab and Launchpad build systems.
    Works fine on Linux and macOS.

* Skip test\_path::test\_compare on non-native. [Kenneth Loafman]

    Skip on GitLab and Launchpad build systems.
    Works fine on Linux and macOS.

* Skip test\_path::test\_compare on non-native. [Kenneth Loafman]

    Skip on GitLab and Launchpad build systems.
    Works fine on Linux and macOS.

* Revert to medieval string formatting. [Kenneth Loafman]

* Revert to medieval string formatting. [Kenneth Loafman]

* Revert to medieval string formatting. [Kenneth Loafman]

* Revert to medieval string formatting. [Kenneth Loafman]

* Remove dependency scanner. [Kenneth Loafman]

* Fix PEP8 and todo issues. [Kenneth Loafman]

* Misc fixes to testing/build environ. [Kenneth Loafman]

    start_debugger now supports multiprocess debug.
    restore testing.unit.test_path.test_compare

* Encoding errors when logging.  Fixes #693. [Kenneth Loafman]

    Use os.fsdecode/os.fsencode when in py3.

* Onedrive may hang indefinitely.  Fixes #695. [Kenneth Loafman]

### Other

* Fix typo. [ede]

* Try to fix. [ede]

    Executing "step_script" stage of the job script
    00:00
    Using docker image sha256:3148ec916ea71d90f1beae623b3c5eb4a2db5a585db3178d9619bc2feb8f5f49 for curlimages/curl:latest with digest curlimages/curl@sha256:f7f265d5c64eb4463a43a99b6bf773f9e61a50aaa7cefaf564f43e42549a01dd ...
    /bin/sh: eval: line 136: apt-get: not found


## rel.1.2.2 (2023-01-26)

### Changes

* \_runtest\_dir on Darwin may use TMPDIR for testing. [Kenneth Loafman]

* Update duplicity.pot. [Kenneth Loafman]

* More changes to get release process working. [Kenneth Loafman]

### Fix

* Fix to work with b2sdk 1.19.0. [Adam Jacobs]

* Fix #692.  Redundant --encrypt option added in gpg.py. [Kenneth Loafman]

    Been around forever.  GPG 2.2.x is the first to detect.  Added
    only when both recipients and hidden_recipients present.

* Fix super() call in test\_selection.py. [Kenneth Loafman]

* Regression on issue #147, change password for incremental. [Kenneth Loafman]

    Changed testcase issue147.sh to need incremental.

    Fixed dup_collections.py to bail with fatal error.

* Crash if a socket is listed with --files-from.  Fixes #689. [Kenneth Loafman]

    Patch supplied by Jethro Donaldson (@jeth-ro).

### Other

* Add detailed step-by-step instructions. [ede]


## rel.1.2.1 (2022-12-02)

### Changes

* Fix for setuptools changes.  Add testing data files to mix. [Kenneth Loafman]


## rel.1.2.0 (2022-12-01)

### New

* Add rsync style --files-from=FILE. Fixes #151. [Kenneth Loafman]

* Add literal include/excludes. Fixes #138. [Kenneth Loafman]

### Changes

* Update duplicity.pot. [Kenneth Loafman]

* Add test case for issue #683. [Kenneth Loafman]

* Don't run start\_debugger till after logging started. [Kenneth Loafman]

* Always run pipeline after MR approval. [Kenneth Loafman]

* Remove gpg\_error\_codes.py / update duplicity.pot. [Kenneth Loafman]

* Fix name in .gitlab-ci.yml. [Kenneth Loafman]

* Go back to standard tests, no master image. [Kenneth Loafman]

* Go back to standard tests, no master image. [Kenneth Loafman]

* Go back to standard tests, no master image. [Kenneth Loafman]

* Go back to standard tests, no master image. [Kenneth Loafman]

* Go back to standard tests, no master image. [Kenneth Loafman]

* Go back to standard tests, no master image. [Kenneth Loafman]

* Add testing for Python 3.11. [Kenneth Loafman]

* Update deprecation messages.  Cleanup. [Kenneth Loafman]

* Reformat / cleanup Makefile. [Kenneth Loafman]

* Fixup help entries in Makefile. [Kenneth Loafman]

* Remove targets xlate-*.  Add target pot. [Kenneth Loafman]

* Change Crowdin commit message. [Kenneth Loafman]

* Update po/duplicity.pot. [Kenneth Loafman]

* Cleanup and make sure setup cleans po dir. [Kenneth Loafman]

* Fix version, oversight in previious commit. [ede]

    [ci_skip]

* Fix snap build for non-amd64 archs. [ede]

    [ci_skip]

* Add filter mode to log line.  #138. [Kenneth Loafman]

* Fix emacs mode line. [Kenneth Loafman]

### Fix

* Fix for issue #683. [Kenneth Loafman]

    - ngettext() is returning empty string on plural and zero counts.
    - go back to plain gettext() and use just a single translation.
    - modify test to run backup using all translations we have.

* Azure Blob Storage backend fails to resume.  Fixes #149. [Kenneth Loafman]

* Went to aggressive on cleanup(). [Kenneth Loafman]

* Fix about 20 pep8 issues. [Kenneth Loafman]

* More fixes to po/update-po. [Kenneth Loafman]

* Fix po/update-pot to leave po/LINGUAS in po. [Kenneth Loafman]

* Run po/update-pot. [Kenneth Loafman]


## rel.1.0.1 (2022-10-03)

### Changes

* Various cleanups to code and tests. [Kenneth Loafman]

* Accept all .po files for update-pot. [Kenneth Loafman]

* Build control files for update-pot. [Kenneth Loafman]

* Accept all .po files for LINGUAS gen. [Kenneth Loafman]

* Build control files for update-pot. [Kenneth Loafman]

* Add tags to commit message. [Kenneth Loafman]

### Fix

* Revert changes to gpg\_failed(). [Kenneth Loafman]

    - fixes #147 - Regression: change of encryption password.
    - note - GPG only returns 0,1,2.  Not sufficient for errors.
    - also added testing/manual/issue147.sh.

### Other

* Update Crowdin configuration file. [Kenneth Loafman]

* Update Crowdin configuration file. [Kenneth Loafman]

* Update Crowdin configuration file. [Kenneth Loafman]

* Update Crowdin configuration file. [Kenneth Loafman]

    Update Crowdin configuration file

    Update Crowdin configuration file


## rel.1.0.0 (2022-09-23)

### Changes

* Update README-SNAP.md to show options. [Kenneth Loafman]

* Add instructions for building snaps. [Kenneth Loafman]

* Add missing license metadata. [ede]

    [ci_skip]

* More docker cleanup. [Kenneth Loafman]

    - Add rclone to package installs.



* Trigger website rebuild on pushes/tags. [ede]

* More docker cleanup. [Kenneth Loafman]

    - remove copy of setup.py, not used
    - add testit.py for basic testing

* More docker cleanup. [Kenneth Loafman]

    - use 'docker compose' not docker-compose
    - remove more unused items

* Optimize build of duplicity\_test image. [Kenneth Loafman]

    - use buildkit to speed up build,
    - split huge layers into smaller ones
    - changes in testing dir trigger pipeline

* Fold requirements.dev into requirements.txt.  Del requirements.dev. [Kenneth Loafman]

* Fold requirements.dev into requirements.txt.  Del requirements.dev. [Kenneth Loafman]

* Fold requirements.dev into requirements.txt.  Del requirements.dev. [Kenneth Loafman]

* Extend code\_test to testing directory. [Kenneth Loafman]

    - Fix or mark issues found.
    - Will not run under py27.

* Fix .md formatting. [Kenneth Loafman]

* Mark slow tests > 10sec.  Use -m "not slow". [Kenneth Loafman]

* Ref requirements.dev in install. [Kenneth Loafman]

* Ref requirements files instead of listing in duplicate. [Kenneth Loafman]

* Action and Audience must be lowercased. [Kenneth Loafman]

* Nuke skip tests and skip ci in CHANGELOG.md. [Kenneth Loafman]

* New os\_options for SWIFT backend. [Florian Perrot]

* Clarify when --s3-endpoint-url,-region-name are needed. [ede]

* Change from master to main branch naming. [Kenneth Loafman]

* Better defaults for S3 mac procs and chunk sizing. [Josh Goebel]

* --s3\_multipart\_max\_procs applies to BOTO3 backend also. [Josh Goebel]

* Migrate to unittest.mock. [Gwyn Ciesla]

* Fix modeline, change utf8 to utf-8 to make emacs happy. [Kenneth Loafman]

* Replace pexpect.run with subprocess\_popen in par2backend. [Kenneth Loafman]

* Fix PEP8 issue. [Kenneth Loafman]

* Add py310 to list of versions supported. [Kenneth Loafman]

* Fix script pushsnap to handle errors. [Kenneth Loafman]

* Add returncode to BackendException for rclonebackend. [Kenneth Loafman]

* Snap use core20 coreutils if none in PATH env var. [ede]

    add "/snap/core20/current/usr/bin" to PATH

* Need to install python3 for pages. [Kenneth Loafman]

* Don't push to savannah any more. [Kenneth Loafman]

* Fix version for builds. [Kenneth Loafman]

### Fix

* Replace pydrive with pydrive2. Fixes #62. [Kenneth Loafman]

* GDrive backend: Add environment args for configuring oauth flow. [Patrick Riley]

* GDrive backend: For Google OAuth, switch to loopback flow. [Patrick Riley]

* Reduce number of GPG file descriptors, add GPG translatable errors. [Kenneth Loafman]

* Remove sign-build step.  Does not work. [Kenneth Loafman]

* Add back overzealous removal of 'import re'. [Kenneth Loafman]

* Webdav listing failed on responses with namespace 'ns0' [Felix Prüter]

* Fix build of apsw/sqlite3 bundle.  Don't store apsw in repo. [Kenneth Loafman]

* Make sure that FileChunkIO#name is a string, not a bytes-like object. [Josh Goebel]

* Fix possible memory leaks.  Fixes #128.  Fixes #129. [Kenneth Loafman]

* Additional fixes/checks for pexpect version.  Fixes #125. [Kenneth Loafman]

    - Add check to ssh_pexpect_backend, par2backend, for version < 4.5.0
    - Skip test for par2backend instance if version < 4.5.0

* Fixes #125.  Add use\_poll=True to pexpect.run in par2backend. [Kenneth Loafman]

    - allows way too many incrementals to operate.
    - regression test, issue125.sh, added to manual.

* Fix issue #78 - Retry on SHA1 mismatch. [Kenneth Loafman]

* Add missing double quote. [ede]

* Install requirements.dev. [Kenneth Loafman]

### Other

* Doc: some reformatting for better readability. [ede]

* Doc: clarify when --s3-endpoint-url,-region-name are need. [ede]


## rel.0.8.23 (2022-05-15)

### New

* Add --webdav-headers to webdavbackend.  Fixes #94. [Kenneth Loafman]

* Add tests for Python 3.10. [Kenneth Loafman]

* Make sdist only provide necessary items for build. [Kenneth Loafman]

* Add changelog to deploy stage to build CHANGELOG.md. [Kenneth Loafman]

    - make job changelog to run tools/makechangelog in CI/CD.
    - make jobs build_pip and build_snap require changelog.



* Document rclone option setting via env vars. [edeso]

* Enable CI snapcraft amd64 builds with docker. [edeso]

    .gitlab-ci.yml
    job build_snap based on a working docker image
    commented 'only:' limitiation, it's manual anyway
    used split out tools/installsnap step
    upload artifact (duplicity-*.snap) regardless
    - so it can be downloaded and debugged
    - keep it for 30 deays by default

    snap/snapcraft.yaml
    - fixup PYTHONPATH

    new 'tools/installsnap' that detects and works with docker

    tools/testsnap
    remove installation step
    remove double test entries
    change testing to use gpg and compression

* Document rclone option setting via env vars. [edeso]

* Fix other archs, expose rdiffdir. [edeso]

    fix remote build of armhf, arm64, ppc64el
    arm64 was tested on Debian 11 arm64
    rdiffdir now avail as /snap/bin/duplicity.rdiffdir
    remove obsolete folder /usr/lib/python3.9/ in snap

* Demote boto backend to legacy ... [ede]

    usable via boto+s3:// or boto+gs:// now only
    removed s3+http:// scheme
    added --s3-endpoint-url option as replacement
    added --s3-use-deep-archive option
    changes are document in man page commit of the same patch set

* Promote boto3 backend to default s3:// backend ... [ede]

    add --s3-unencrypted-connection support

* Man page, major sorting, reformatting, S3/GCS documentation update. [ede]

    some updates, added s3 options, clarifications
    updated Notes on S3 and Google Cloud Storage usage
    sort Options, Url Formats, Notes on alphabetically
    consistently use "NOTE:"
    indent properly all over

### Changes

* Use cicd image hosted on GitLab. [Kenneth Loafman]

* Create singular container for testing. [Kenneth Loafman]

* Fix PEP8 issue. [Kenneth Loafman]

* Remove build on merge request and unused variables. [Kenneth Loafman]

* Cosmetic changes only. [Kenneth Loafman]

* Make pages manual deploy. [Kenneth Loafman]

* Changelog removed, remove needs. [Kenneth Loafman]

* Only build pip and snap, don't push. [Kenneth Loafman]

* Fix misspelled stage name. [Kenneth Loafman]

* Fix deps format. [Kenneth Loafman]

* Fix deps format. [Kenneth Loafman]

* Add requirements.dev to tox.ini. [Kenneth Loafman]

* Include pydevd in requirements.txt. [Kenneth Loafman]

* Go back to ubuntudesktop/gnome-3-38-2004. [Kenneth Loafman]

* Add tools dir to changes list in deploy-template. [Kenneth Loafman]

* Try snap with utuntu:20.04. Fix artifacts loc. [Kenneth Loafman]

* Some debugging statements. [Kenneth Loafman]

* Some debugging statements. [Kenneth Loafman]

* Set up the SSH key and the known\_hosts file. [Kenneth Loafman]

* Set up config for git. [Kenneth Loafman]

* Clone repo so setuptools-scm works properly. [Kenneth Loafman]

* Move setuptools* to .dev.  Nuke report.xml artifact. [Kenneth Loafman]

* Add some more requirements. [Kenneth Loafman]

* Install git and intltool for changelog. [Kenneth Loafman]

* Add changes: to deploy-template. [Kenneth Loafman]

* Fix syntax. [Kenneth Loafman]

* Minimize CI/CD overhead. [Kenneth Loafman]

* Split requirements into .txt and .dev. [Kenneth Loafman]

    .txt - normal user
    .dev - developer

* Standardize startup sequence. [Kenneth Loafman]

* Remove deploy jobs needing secret keys. [Kenneth Loafman]

* Do not supply user/password to twine, just access token. [Kenneth Loafman]

* Do not supply user/password to twine, just access token. [Kenneth Loafman]

* Add default never to .test-template. [Kenneth Loafman]

* Change PYPI\_ACCESS\_TOKEN back to variable and just echo it. [Kenneth Loafman]

* Just cp PYPI\_ACCESS\_TOKEN to \~/.pypirc. [Kenneth Loafman]

* Fix usage of PYPI\_ACCESS\_TOKEN. [Kenneth Loafman]

* Set to run deploy only after a push event. [Kenneth Loafman]

* Whoops, can't run deploy on source branch to merge. [Kenneth Loafman]

* Use rules in templates.  Always run on merge requests. [Kenneth Loafman]

* Always run pipeline on merge request event. [Kenneth Loafman]

* Make sure we run all during merge requests. [Kenneth Loafman]

* Add deploy-template to only run when source changes. [Kenneth Loafman]

* Fix to only run tests if source code changes. [Kenneth Loafman]

* If no changes, exit 0 to allow pip and snap builds. [Kenneth Loafman]

* Set up pypi access token for uploading. [Kenneth Loafman]

* Keep pip build artifacts for 30 days as pipeline artifacts. [ede]

* Skip tests, not ci, so we can build snaps, pips, pages, etc. [Kenneth Loafman]

* Allow non-Docker environs to sign snaps. [Kenneth Loafman]

* Allow GitLab CI to upload snaps to the store. [Kenneth Loafman]

    still have not figured out how to store sign key on GitLab



* Update or add copyright and some cosmetic changes. [Kenneth Loafman]

* Remove install of snapcraft, snap, snapd. [Kenneth Loafman]

* Add grpcio-tools to top to get latest version. [Kenneth Loafman]

    This leaves two unresolvable problems (upper version conflicts):
    ERROR: mediafire 0.6.0 has requirement requests<=2.11.1,>=2.4.1, but
    you'll have requests 2.27.1 which is incompatible.
    ERROR: python-novaclient 2.27.0 has requirement pbr<2.0,>=1.6, but
    you'll have pbr 5.8.1 which is incompatible.



* Remove conflicting build env variable.  Nuke evil tabs. [Kenneth Loafman]

* Allow duplicity-core20 to run deploy steps, for now. [Kenneth Loafman]

* Install snapcraft snap snapd. [Kenneth Loafman]

* Allow pip and snap builds from branches for now. [Kenneth Loafman]

* Add build\_snap and build\_pip back. [Kenneth Loafman]

* More tests for tools/testsnap. [Kenneth Loafman]

    add backup/verify runs to check major pathways
    add multi-lib check to avoid SnapCraft bug 1965814

* More snapcraft.yaml fixups. [Kenneth Loafman]

    break up long strings for better readability
    preload pbr and requests to avoid most version warnings
    pbr and requests are now at latest version, not ancient

* Add further checks to testing for backup and multi-lib. [Kenneth Loafman]

* Remove SNAPCRAFT\_PYTHON\_INTERPRETER per edso, no change on U20. [Kenneth Loafman]

* Try to force Python 3.8 only. [Kenneth Loafman]

* More detailed error message. [Kenneth Loafman]

* Divide makesnap into makesnap, testsnap, and pushsnap. [Kenneth Loafman]

* Revert to core18.  core20 is still unusable. [Kenneth Loafman]

### Fix

* Fix LP bug #1970124 - obscure error message. [Kenneth Loafman]

    Fixes handling of error message with real path, not temp path.

* Nuke a couple of false pylint errors, use inline disable. [Kenneth Loafman]

* Nuke a couple of false pylint errors, fix spelling. [Kenneth Loafman]

* Nuke a couple of false pylint errors. [Kenneth Loafman]

* Minor formatting fix. [ede]

    /builds/duplicity/duplicity/duplicity/backends/s3_boto3_backend.py:93:81: W291 trailing whitespace

* Fixup some minor formatting issues. [ede]

    /builds/duplicity/duplicity/duplicity/backends/s3_boto3_backend.py:92:121: E501 line too long (159 > 120 characters)
    /builds/duplicity/duplicity/duplicity/backends/s3_boto3_backend.py:227:58: W292 no newline at end of file
    /builds/duplicity/duplicity/duplicity/backends/s3_boto_backend.py:34:1: W391 blank line at end of file

### Other

* Pkg:fix: make extra sure correct python binary is used. [edeso]

    remove unmaintained changelog
    add shell wrapper(launcher.sh)
    add debug script
    use shell wrapper as snap binary ignores PATH for python binary on debian

* Optimize CI/CD to only run when needed. [Kenneth Loafman]

* Upgrade to base core20. [Kenneth Loafman]

* Switch website to gitlab.io, promote duplicity.us. [ede]

* Fix website link. [ede]


## rel.0.8.22 (2022-03-04)

### New

* Minimize testing/manual/issue98.sh for issue #98. [Kenneth Loafman]

* Add testing/manual/issue98.sh to test issue #98. [Kenneth Loafman]

* Add Getting Versioned Source to README-REPO.md. [Kenneth Loafman]

    [no ci]

* Test case for issue 103 multi-backend prefix affinity. [Kenneth Loafman]

* Add --use-glacier-ir option for instant retrieval.  Fixes #102. [Kenneth Loafman]

* Add --par2-volumes entry to man page. [Kenneth Loafman]

* Add manual test for issue 100. [Kenneth Loafman]

* Add option --show-changes-in-set <index> to collection-status. [Kenneth Loafman]

    Patches provided by Peter Canning (@pcanning).  Closes #99.

### Changes

* Changes to run on Focal with core20. [Kenneth Loafman]

* Use multiple -m options on commit to split comment. [Kenneth Loafman]

* Remove build-pip and build-snap.  Build locally for now. [Kenneth Loafman]

* Remove build-pip and build-snap.  Build locally for now. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Remove sudo. [Kenneth Loafman]

* Swap over to image 'cibuilds/snapcraft:core20`. [Kenneth Loafman]

* Core20 usess py38, not py36. [Kenneth Loafman]

* Core20 usess py38, not py36. [Kenneth Loafman]

* Attempt core20 again. [Kenneth Loafman]

* Fix syntax. [Kenneth Loafman]

* Remove unneeded Dockerfiles.  Rename. [Kenneth Loafman]

* Try remote snap build. [Kenneth Loafman]

* Remove unneeded Dockerfiles.  Rename. [Kenneth Loafman]

* Cosmetic fixes. [Kenneth Loafman]

* Try forcing snaps to use python3.6 in 18.04. [Kenneth Loafman]

* Add check for correct platform. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Use snapcraft snap instead of deb.  See LP bug 1948597. [Kenneth Loafman]

* Add warning for replicate command.  See issue #98. [Kenneth Loafman]

* Minor tweaks. [Kenneth Loafman]

* Add wheels to .gitignore. [Kenneth Loafman]

* Cosmetic changes. [Kenneth Loafman]

* Add collection-status at end of test. [Kenneth Loafman]

* Remove gpg socket files during clean. [Kenneth Loafman]

* Back off to default image. [Kenneth Loafman]

    [skip-tests]

* Try adding apt-get upgrade. [Kenneth Loafman]

    [skip-tests]

* Add .test-template to allow skipping qual and tests. [Kenneth Loafman]

    [skip-tests]

* Try build with apt-get update. [Kenneth Loafman]

* Try building snap on 20.04. [Kenneth Loafman]

* Add targets to manually import/export translations. [Kenneth Loafman]

* Update duplicity.pot for LP translation. [Kenneth Loafman]

* Revert "Put out first 'post' release to fix pypi issue". [Kenneth Loafman]

* Put out first 'post' release to fix pypi issue. [Kenneth Loafman]

* Rename AUTHORS to CONTRIBUTING.md. [Kenneth Loafman]

* Rename dist dir to tools to avoid collision with setuptools. [Kenneth Loafman]

* Add line wrap to changelog process, body and subject. [Kenneth Loafman]

### Fix

* Add --no-files-changed option.  Fixes issue #110. [Kenneth Loafman]

* Fix use of sorted() builtin (does not sort in place). [Kenneth Loafman]

* Revert snapcraft.yaml to build on core18.  core20 was flakey. [Kenneth Loafman]

* Fix #107 - TypeError in restart\_position\_iterator. [Kenneth Loafman]

* Need to pass kwargs to BaseIdentitu. [Kenneth Loafman]

* Fix \_\_init\_\_ in hubic.py.  Fixes #106. [Kenneth Loafman]

* Try building snap on core20. [Kenneth Loafman]

* Try building snap on core20. [Kenneth Loafman]

* Somehow missed boto when doing #102.  Now supported. [Kenneth Loafman]

* Fix logic of skipIf test. [Kenneth Loafman]

* Fix data\_files AUTHORS to CONTRIBUTING.md. [Kenneth Loafman]

### Other

* Revert "chg:dev:core20 usess py38, not py36." [Kenneth Loafman]

    This reverts commit 05eda5828c7bdde1003357439cfcb4d93124a377.

* Slate Backend. [Shr1ftyy]

* Skip tests for ppc64le also. [Mikel Olasagasti Uranga]


## rel.0.8.21 (2021-11-09)

### New

* Add release-prep.sh for release preparation. [Kenneth Loafman]

* Add py310 to envlist to test against python 3.10. [Kenneth Loafman]

* Add update of API docs to deploy step. [Kenneth Loafman]

### Changes

* When buiilding for amd64 build snap locally, else remote. [Kenneth Loafman]

* Fix build of pages. [Kenneth Loafman]

* Switch over to sphinx-rtd-theme. [Kenneth Loafman]

* Fix command line warning messages. [Kenneth Loafman]

* Fix clean command to include module doc .rst files. [Kenneth Loafman]

* Nuke generated .rst files. [Kenneth Loafman]

* Nuke before\_script.  [ci skip] [Kenneth Loafman]

* Move html to public dir. [Kenneth Loafman]

* Forgot to add myst-parser.  Comment out tests for now. [Kenneth Loafman]

* Back to alabaster theme.  Port changes from sqlite branch. [Kenneth Loafman]

* Remove Dockerfiles for .10 versions. [Kenneth Loafman]

* Fix some rst errors in docstrings.  Add doctest module. [Kenneth Loafman]

* Fixes to make API docs work right. [Kenneth Loafman]

* Whoops, left out import sys. [Kenneth Loafman]

* Skip test to allow py27 and py35 to pass. [Kenneth Loafman]

* Some tweaks to run cleaner. [Kenneth Loafman]

* Fix typo in test selection. [Kenneth Loafman]

* Remove redundant call to pre\_process\_download\_batch. [Kenneth Loafman]

* Fix mismatch between pre\_process\_download[\_batch] calls. [Kenneth Loafman]

    Implement both in backend and multibackend if hasattr True.

### Fix

* Fix #93 - dupliicity wants private encryption key. [Kenneth Loafman]

* PAR2 backend failes to create par2 file with spaces in name. [Kenneth Loafman]

* Fix bug 930151 - Restore symlink changes target attributes (2) [Kenneth Loafman]

* Fix LP bug 930151 - Restore a symlink changes target attributes. [Kenneth Loafman]

* Fix #89 part 2 - handle small input files where par2 fails. [Kenneth Loafman]

* Fix theme name, sphinx\_rtd\_theme. [Kenneth Loafman]

* Fix PEP8 issue. [Kenneth Loafman]

* Fix #90 - rclone backend fails with spaces in pathnames. [Kenneth Loafman]

* Fix #89 - Add PAR2 number volumes option. [Kenneth Loafman]

* Fix #88 - Add PAR2 creation failure error message. [Kenneth Loafman]

* Fix bug #87, Restore fails and stops on corrupted backup volume. [Kenneth Loafman]

* Fix bug #86, PAR2 backend fails on restore, with patch supplied. [Kenneth Loafman]

* Fixed Catch-22 in pyrax\_identity.hubic.  Debian bug #996577. [Kenneth Loafman]

    Name error on backend HubiC (Baseidentity).  Cannot avoid importing
    pyrax since HubicIdentity requires pyrax.base_identity.BaseIdentity.

* Fix PEP8 style errors. [Kenneth Loafman]

* Fix issue #81 - Assertion fail when par2 prefix forgotten. [Kenneth Loafman]

* Test with mirror and stripe modes. [Kenneth Loafman]

* Fix issue #79 - Multibackend degradation. [Kenneth Loafman]

* Add verbose exception on progress file failure. [Kenneth Loafman]

### Other

* Resolve os option key naming mismatch. [Johannes Winter]

* Set up gdrive client credentials scope correctly. [Christopher Haglund]

* Don't query for filesize. [Johannes Winter]

* Upgrade docker test environment. [Johannes Winter]

* Merge branch 'master' of gitlab.com:duplicity/duplicity. [Kenneth Loafman]

* Fix TypeError. [Clemens Fuchslocher]

* SSHPExpectBackend: Implement \_delete\_list method. [Clemens Fuchslocher]

* MultiBackend: Don't log username and password. [Clemens Fuchslocher]

* Fix NameError. [Clemens Fuchslocher]

* Onedrive: Support using an external client id / refresh token. [Michael Terry]

* Fix functional tests when \_runtestdir is not /tmp. [Guillaume Girol]

* Allow to override manpage date with SOURCE\_DATE\_EPOCH. [Bernhard M. Wiedemann]

    in order to make builds reproducible.
    See https://reproducible-builds.org/ for why this is good
    and https://reproducible-builds.org/specs/source-date-epoch/
    for the definition of this variable.

    Also use UTC/gmtime to be independent of timezone.

* Improved management of volumes unsealing for PCA backend For PCA
backend, unseal all volumes at once when restoring them instead of
unsealing once at a time. Use pre\_process\_download method already
available in dup\_main. Need to implement it on BackendWrapper and
Multibackend as well. [Erwan B]


## rel.0.8.20 (2021-06-26)

### New

* Better looping.  Increase to 100 loops. [Kenneth Loafman]

* Repeating test for LP bug 487720. [Kenneth Loafman]

    Restore fails with "Invalid data - SHA1 hash mismatch"

### Changes

* Build\_ext now builds inplace for development ease. [Kenneth Loafman]

* Log difftar filename where kill happened. [Kenneth Loafman]

* Remove lockfile to avoid user confusion. [Kenneth Loafman]

* Allow customization. [Kenneth Loafman]

* Fix Support DynamicLargeObjects inside swift backend. [Mathieu Le Marec - Pasquet]

    Use high levels APIS to both:

    - correctly delete multipart uploads
    - correctly handle multipart uploads

    This fixes [launchpad #557374](https://answers.launchpad.net/duplicity/+question/557374)

* Fix makechangelog to output actual problems. [Kenneth Loafman]

* Add dependency scanning. [Kenneth Loafman]

* Make sure changelog is only change to commit. [Kenneth Loafman]

* Fix indentation. [Kenneth Loafman]

* Add support for --s3-multipart-chunk-size, default 25MB. [Kenneth Loafman]

    Fixes issue #61

* Add interruptable:true as default. [Kenneth Loafman]

* Fix snapcraft commands. [Kenneth Loafman]

* Fix snaplogin file use. [Kenneth Loafman]

* Add deployment for pip and snap builds. [Kenneth Loafman]

* Add build\_pip job. [Kenneth Loafman]

* Fix PEP8 issue. [Kenneth Loafman]

* More cleanup for snap builds. [Kenneth Loafman]

* Move arch selection to dist/makesnap. [Kenneth Loafman]

* Try snap build on all architectures. [Kenneth Loafman]

* Build for i386, amd64, armhf. [Kenneth Loafman]

* Move to remote build of armfh and amd64. [Kenneth Loafman]

* Attempt remote build of armfh. [Kenneth Loafman]

* More cleanup on requirements. [Kenneth Loafman]

* Megatools no longer supports py35. [Kenneth Loafman]

* Get more stuff from pypi than repo.  Some cleanup. [Kenneth Loafman]

* Fix spaces before inline comments. [Kenneth Loafman]

* Enable access-member-before-definition in pylintrc. [Kenneth Loafman]

* Fix indentation. [Kenneth Loafman]

* Fix formatting in A NOTE ON GDRIVE BACKEND.  Minor. [Kenneth Loafman]

* Module gdata still does not work on py3. [Kenneth Loafman]

* Tweak requirements for gdrivebackend.  Cosmetic changes. [Kenneth Loafman]

### Fix

* Fix test file count after deleting lockfile. [Kenneth Loafman]

* Release lockfile only once. [Kenneth Loafman]

* Release lockfile only once. [Kenneth Loafman]

* Support -o{Global,User}KnownHostsFile in --ssh-options. [Kenneth Loafman]

    Fixes issue #60

* Add pydrive2 to requirements.txt. [Kenneth Loafman]

    Fixes #62.  pydrivebackend was updated to pydrive 2 over a year ago, but
    the requirements.txt file was not updated to reflect this.

* Fix error message on gdrivebackend. [Kenneth Loafman]

* Fix issue #57 SSH backends - IndexError: list index out of range. [Kenneth Loafman]

### Other

* Remove backup file. [kenneth@loafman.com]

* Don't skip CI. [Kenneth Loafman]

* Add support for new b2sdk V2 API. [Adam Jacobs]

* Have duplicity retry validate\_block so object storage can report
correct size. [Doug Thompson]

* Replace b2sdk private API references in b2backend with public API. [Adam Jacobs]

* Update b2 backend to use *public* b2sdk API. [Adam Jacobs]

* B2sdk 1.8.0 refactored minimum\_part\_size to recommended\_part\_size
(the value used stays the same) [Adam Jacobs]

    It's a breaking change that makes duplicity fail with the new SDK.

    This fix makes duplicity compatible with both pre- and post- 1.8.0 SDKs.

* Added Google MyDrive support updated man pages and --help text. [Anthony Uphof]


## rel.0.8.19 (2021-04-29)

### Changes

* Display merge comments.  Better formatting. [Kenneth Loafman]

* Clean up readability.  Minor changes. [Kenneth Loafman]

* Cosmetic chnges. [Kenneth Loafman]

* Make testing/manual/bug1893481 into a tarball, not directory. [Kenneth Loafman]

* Add Makefile and update docs. [Kenneth Loafman]

* Remove installs common between before\_script: and script: [Kenneth Loafman]

* Remove installs common between before\_script: and script: [Kenneth Loafman]

### Fix

* Gdata module passes on py27 only. [Kenneth Loafman]

* Restore pylintrc, add requirement. [Kenneth Loafman]

* Fix unadorned string in restored pylint test. [Kenneth Loafman]

* Restored pylint test.  Fixed one issue found. [Kenneth Loafman]

* More py27 packages bit the dust. [Kenneth Loafman]

* Util.uexec() will return u'' if no err msg in e.args. [Kenneth Loafman]

* Util.uexec() should check for e==None on entry. [Kenneth Loafman]

* Mark skip those not usable on py27. Fix version. [Kenneth Loafman]

* Uncomment backends.  Mark skip those not usable on py27. [Kenneth Loafman]

* Lock in some module versions to last supporting py27. [Kenneth Loafman]

* Allow py27 to fail CI.  Restrict mock pkg to 3.05. [Kenneth Loafman]

* Fix bug #1547458 - more consistent passphrase prompt. [Kenneth Loafman]

* Fixes bug #1454136 - SX backend issues. [Kenneth Loafman]

* Fixes bug 1918981 - option to skip trash on delete on mediafire. [Kenneth Loafman]

    Added --mf-purge option to bypass trash

* Fix bug 1919017 - MultiBackend reports failure on file deletion. [Kenneth Loafman]

* Recomment, py2 does not support all backends. [Kenneth Loafman]

* Add azure-storage module requirement.  Uncomment all. [Kenneth Loafman]

* Remove requirement for python3-pytest-runner.  Not used. [Kenneth Loafman]

* Install older version of pip before py35 deprecation. [Kenneth Loafman]

* Add py27 and py35 back to CI. [Kenneth Loafman]

* Fix setup.py to handle Python 2 properly. [Kenneth Loafman]

* Fixes #41 - par2+rsync (non-ssh) fails. [Kenneth Loafman]

### Other

* Fix "Giving up after 5 attempts. timeout: The read operation timed
out" [Christian Perreault]

* Don't sync when removing old backups. [Matthew Marting]

* Fix util.uexc: do not return None. [Michael Kopp]

* Implement Box backend. [Jason Wu]

* Implement megav3 backend to to cater for change in MEGACmd. [Jason Wu]

* Fix documentation for azure backend. [Michael Kopp]

* Fix typo. [Moses Miller]

* Add IDrive backend. [SmilingM]

* Progress bar improvements. [Moses Miller]

* Fix;usr:Fixes bug #1652953 - seek(0) on /dev/stdin crashes. [Kenneth Loafman]

* Add a new Google Drive backend (gdrive:) [Jindřich Makovička]

    - Removes the PyDrive/PyDrive2 dependencies, and depends only on the
      Google API client libraries commonly available in distributions.

    - Uses unchanged JSON secret files as downloaded from GCP

    - Updates the Google Drive API to V3

* Replaced original azure implementation. [Erwin Bovendeur]

* Fixed code smells. [Erwin Bovendeur]

* Azure v12 support. [Erwin Bovendeur]

* Revert "fix:pkg:Remove requirement for python3-pytest-runner.  Not
used." [Kenneth Loafman]

    This reverts commit 90e7e2acb6d158437cab3210114da46df72a7c85.

* List required volumes when called with 'restore --dry-run' [Matthias Blankertz]

    When restoring in dry-run mode, and with the manifest available, list
    the volumes that would be gotten from the backend when actually
    performing the operation.
    This is intended to aid users of e.g. the S3 backend with (deep) glacier
    storage, allowing the following workflow to recover files, optionally at
    a certain time, from a long-term archive:
    1. duplicity restore --dry-run [--file-to-restore <file/dir>] [--time <time>] boto3+s3://...
    2. Start a Glacier restore process for all the listed volumes
    3. duplicity restore [--file-to-restore <file/dir>] [--time <time>] boto3+s3://...

* Fix sorting of BackupSets by avoiding direct comparison. [Stefan Wehrmeyer]

    Sorting should only compare their time/end_time, not BackupSets directly
    Closes #42

* Update mailing list link. [Chris Coutinho]

* Fixes #16 - Move from boto to boto3. [Kenneth Loafman]

* Py27 EOL 01/2020, py35 EOL 01/2021, remove tests. [Kenneth Loafman]

* Remove 2to3 from ub16 builds. [Kenneth Loafman]

* Move py35 back to ub16, try 2. [Kenneth Loafman]

* Move py35 back to ub16. [Kenneth Loafman]

* Move py27 tests to ub16 and py35 tests to ub18. [Kenneth Loafman]

* Fixes #16 - Move from boto to boto3. [Kenneth Loafman]

* Py27 EOL 01/2020, py35 EOL 01/2021, remove tests. [Kenneth Loafman]

* Move py27 tests to ub16 and py35 tests to ub18. [Kenneth Loafman]

    Move py35 back to ub16.

    Move py35 back to ub16, try 2.

    Remove 2to3 from ub16 builds.

* Fixes #33, remove quotes from identity filename option. [Kenneth Loafman]

* Fix to correctly build \_librsync.so. [Kenneth Loafman]

* Fix to add --inplace option to build\_ext. [Kenneth Loafman]

* Rename pylintrc to .pylintrc. [Kenneth Loafman]

* Multibackend: fix indentation error that was preventing from
registering more than one affinity prefix per backend. [KheOps]

* Move testfiles dir to a temp location. [Kenneth Loafman]

    - was crashing LiClipse/Eclipse when present in project.
    - so far only Darwin and Linux are supported, default Linux.
    - Darwin uses 'getconf DARWIN_USER_TEMP_DIR' for temp dir.
    - Linux uses TMPDIR, TEMP, or defaults to /tmp.

* Update .gitlab-ci.yml to need code test to pass. [Kenneth Loafman]

* Remove basepython in code and coverage tests. [Kenneth Loafman]

* Add report.xml. [Kenneth Loafman]

* Bulk replace testfiles with /tmp/testfiles. [Kenneth Loafman]

* Skip unicode tests that fail on non-Linux systems like macOS. [Kenneth Loafman]


## rel.0.8.18 (2021-01-09)

### Other

* Onedrive: Support using an external client id / refresh token. [Michael Terry]

* Update .gitlab-ci.yml to need code test to pass. [Kenneth Loafman]

* Fix issue #26 Backend b2 backblaze fails with nameprefix restrictions. [Kenneth Loafman]

* Fix issue #29 Backend b2 backblaze fails with nameprefix restrictions. [Kenneth Loafman]

* Fix unadorned strings. [Kenneth Loafman]

* Report errors if B2 backend does exist but otherwise fails to import. [Phil Ruffwind]

    Sometimes import can fail because one of B2's dependencies is broken.

    The trick here is to query the "name" attribute of ModuleNotFoundError
    to see if B2 is the module that failed. Unfortunately this only works on
    Python 3.6+. In older versions, the original behavior is retained.

    This partially mitigates the issue described in
    https://github.com/henrysher/duplicity/issues/14.

* Add report.xml. [Kenneth Loafman]

* Remove basepython in code and coverage tests. [Kenneth Loafman]

* Fix pep8 warning. [Kenneth Loafman]

* Added option --log-timestamp to prepend timestamp to log entry. [Kenneth Loafman]

    The default is off so not to break anything, and is set to on when the
    option is present.  A Catch-22 hack was made since we had to get options
    for the log before adding a formatter, yet the commandline parser needs
    the logger.  Went old school on it.

* Improve. [Gwyn Ciesla]

* Improve patch for Python 3.10. [Gwyn Ciesla]

* Conditionalize for Python version. [Gwyn Ciesla]

* Patch for Python 3.10. [Gwyn Ciesla]


## rel.0.8.17 (2020-11-11)

### Other

* Fixup ignore\_regexps for optional text. [Kenneth Loafman]

* Fix issue #26 (again) - duplicity does not clean up par2 files. [Kenneth Loafman]

* Fix issue #26 - duplicity does not clean up par2 files. [Kenneth Loafman]

* Fix issue #25 - Multibackend not deleting files. [Kenneth Loafman]

* Adjust setup.py for changelog changes. [Kenneth Loafman]

* Delete previous manual changelogs. [Kenneth Loafman]

* Tools to make a CHANGELOG.md from git commits. [Kenneth Loafman]

    $ [sudo] pip install gitchangelog

* Make exclude-if-present more robust. [Michael Terry]

    Specifically, handle all the "common errors" when listing a directory
    to see if the mentioned file is in it. Previously, we had done a
    check for read access before listing. But it's safe to try to list
    and just catch the errors that happen.

* Drop default umask of 0077. [Michael Terry]

    For most backends, it doesn't actually take effect. And it can be
    confusing for people that back up to a drive that is ext4-formatted
    but then try to restore on a new system.

    If folks are worried about others accessing the backup files,
    encryption is the recommended path for that.

    https://gitlab.com/duplicity/duplicity/-/issues/24

* Comment out RsyncBackendTest, again. [Kenneth Loafman]

* Fix some unadorned strings. [Kenneth Loafman]

* Fixed RsyncBackendTeest with proper URL. [Kenneth Loafman]

* Fix issue #23. [Yump]

    Fix unicode crash on verify under python3, when symlinks have changed targets since the backup was taken.

* Rclonebackend now logs at the same logging level as duplicity. [Kenneth Loafman]

* Allow sign-build to fail on walk away.  Need passwordless option. [Kenneth Loafman]

* Fix --rename typo. [Michael Terry]

* Move back to VM build, not remote.  Too many issues with remote. [Kenneth Loafman]

* Escape single quotes in machine-readable log messages. [Michael Terry]

    https://gitlab.com/duplicity/duplicity/-/issues/21

* Uncomment review-tools for snap. [Kenneth Loafman]

* Whoops, missing wildcard '*'. [Kenneth Loafman]

* Changes to allow remote build of snap on LP. [Kenneth Loafman]

* Changes to allow remote build of snap on LP. [Kenneth Loafman]

* Add a pylint disable-import-error flag. [Kenneth Loafman]

* Change urllib2 to urllib.request in parse\_digest\_challenge(). [Kenneth Loafman]

* Fix Python 3.9 test in .gitlab-ci.yaml. [Kenneth Loafman]

* Fix Python 3.9 test in .gitlab-ci.yaml. [Kenneth Loafman]

* Add Python 3.9 to .gitlab-ci.yaml. [Kenneth Loafman]

* Add Python 3.9 to the test suite.  It tests sucessfuly. [Kenneth Loafman]

* Fix bug #1893481 again for Python2.  Missed include. [Kenneth Loafman]

* Fix bug #1893481 Error when logging improperly encoded filenames. [Kenneth Loafman]

    - Reconfigure stdout/stderr to use errors='surrogateescape' in Python3
    	and errors='replace' in Python2.
      - Add a manual test case to check for regression.


## rel.0.8.16 (2020-09-29)

### Other

* Merged in s3-unfreeze-all. [Kenneth Loafman]

* Wait for Glacier batch unfreeze to finish. [Marco Herrn]

    The ThreadPoolExecutor starts the unfreezing of volumes in parallel.
    However we can wait until it finishes its work for all volumes.

    This currently does _not_ wait until the unfreezing process has
    finished, but only until the S3 'restore()' operations have finished
    (which can take a bit time).

    The actual (sequential) pre_processing of the volumes to restore then
    waits for the actual unfreezing to finish by regularly checking the
    state of the unfreezing.

* Adorn string as unicode. [Marco Herrn]

* Utilize ThreadPoolExecutor for S3 glacier unfreeze. [Marco Herrn]

    Starting one thread per file to unfreeze from Glacier can start a huge
    amounts of threads in large backups.
    Using a thread pool should cut this down to a more appropriate number of
    threads.

* Refine codestyle according to PEP-8. [Marco Herrn]

* Adorn strings as unicode. [Marco Herrn]

* S3 unfreeze all files at once. [Marco Herrn]

    When starting a restore from S3 Glacier, start the unfreezing of all
    volumes at once by calling botos 'restore()' method for each volume in a
    separate thread.

    This is only implemented in the boto backend, not in the boto3 backend.

* Add boto3 to list of requirements. [Kenneth Loafman]

* Remove ancient CVS Id macro. [Kenneth Loafman]

* Merged in OutlawPlz:paramiko-progress. [Kenneth Loafman]

* Fixes paramiko backend progress bar. [Matteo Palazzo]

* Merged in lazy init for Boto3 network connections. [Kenneth Loafman]

* Initial crack at lazy init for Boto3. [Carl Alexander Adams]

* Record the hostname, not the fqdn, in manifest files. [Michael Terry]

    We continue to check the fqdn as well, to keep backward
    compatibility.

    https://bugs.launchpad.net/duplicity/+bug/667885

* Avoid calling stat when checking for exclude-if-present files. [Michael Terry]

    If a folder with rw- permissions (i.e. read and write, but no exec)
    is examined for the presence of an exclude-if-present file, we would
    previously throw an exception when trying to stat the file during
    Path object construction.

    But we don't need to stat in this case. This patch just calls
    listdir() and checks if the file is in that result.

* Fix build control files after markdown conversion. [Kenneth Loafman]

* Recover some changes lost after using web-ide. [Kenneth Loafman]

* Paperwork. [Kenneth Loafman]

* Set default values for s3\_region\_name and s3\_endpoint\_url. [Marco Herrn]

    Fixes #12

* Allow setting s3 region and endpoint. [Marco Herrn]

    This commit introduces the new commandline options
      --s3-region-name
      --s3-endpoint-url
    to specify these parameters. This allows using s3 compatible providers
    like Scaleway or OVH.

    It is probably useful for Amazon accounts, too, to have more fine
    grained influence on the region to use.

* Update README-REPO.md. [Kenneth Loafman]

* Make code view consistent. [Kenneth Loafman]

* Update setup.py. [Kenneth Loafman]

* Update README.md. [Kenneth Loafman]

* Paperwork. [Kenneth Loafman]

* Revert "Merge branch 's3-boto3-region-and-endpoint' into 'master'" [Kenneth Loafman]

    This reverts commit f25e9740e17d24cf309aee136953d8fd51a7bf9b, reversing
    changes made to 2890326dfd7a5bf9ea340aca76d96ebcd25aa8b6.

* Bump version for LP dev build. [Kenneth Loafman]


## rel.0.8.15 (2020-07-27)

### Other

* Always paperwork. [Kenneth Loafman]

* Allow setting s3 region and endpoint. [Marco Herrn]

    This commit introduces the new commandline options
      --s3-region-name
      --s3-endpoint-url
    to specify these parameters. This allows using s3 compatible providers
    like Scaleway or OVH.

    It is probably useful for Amazon accounts, too, to have more fine
    grained influence on the region to use.

* Fix missing FileNotUploadedError in pydrive backend. [Martin Sucha]

    Since dadbe2d2c22751f68f179833d36c94f2777ba425, FileNotUploadedError
    is not imported anymore, resulting in an exception in case
    some of the files failed to upload. Adding the import back.

* Fixed indentation. [Joshua Chan]

* Added shared drive support to existing `pydrive` backend instead of a
new backend. [Joshua Chan]

* PydriveShared backend is identical to Pydrive backend, except that it
works on shared drives rather than personal drives. [Joshua Chan]

* Include the query when parsing the backend URL string, so users can
use it to pass supplementary info to the backend. [Joshua Chan]

* Fix caps on X-Python-Version. [Kenneth Loafman]

* Fix issue #10 - ppa:duplicity-*-git fails to install on Focal Fossa. [Kenneth Loafman]

    - Set correct version requirements in debian/control.

* Remove python-cloudfiles from suggestions. [Jairo Llopis]

    This dependency cannot be installed on Python 3:

    ```
    #12 19.82   Downloading python-cloudfiles-1.7.11.tar.gz (330 kB)
    #12 20.00     ERROR: Command errored out with exit status 1:
    #12 20.00      command: /usr/local/bin/python -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-2iwvh4bp/python-cloudfiles/setup.py'"'"'; __file__='"'"'/tmp/pip-install-2iwvh4bp/python-cloudfiles/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base /tmp/pip-pip-egg-info-b1gvstfs
    #12 20.00          cwd: /tmp/pip-install-2iwvh4bp/python-cloudfiles/
    #12 20.00     Complete output (9 lines):
    #12 20.00     Traceback (most recent call last):
    #12 20.00       File "<string>", line 1, in <module>
    #12 20.00       File "/tmp/pip-install-2iwvh4bp/python-cloudfiles/setup.py", line 6, in <module>
    #12 20.00         from cloudfiles.consts import __version__
    #12 20.00       File "/tmp/pip-install-2iwvh4bp/python-cloudfiles/cloudfiles/__init__.py", line 82, in <module>
    #12 20.00         from cloudfiles.connection     import Connection, ConnectionPool
    #12 20.00       File "/tmp/pip-install-2iwvh4bp/python-cloudfiles/cloudfiles/connection.py", line 13, in <module>
    #12 20.00         from    urllib    import urlencode
    #12 20.00     ImportError: cannot import name 'urlencode' from 'urllib' (/usr/local/lib/python3.8/urllib/__init__.py)
    #12 20.00     ----------------------------------------
    #12 20.00 ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.
    ```

    Also, it is no longer supported. Rackspace uses `pyrax` nowadays. Removing to avoid confusions.

* Update azure requirement. [Jairo Llopis]

    Trying to install `azure` today prints this error:

    ```
    Collecting azure
      Downloading azure-5.0.0.zip (4.6 kB)
        ERROR: Command errored out with exit status 1:
         command: /usr/local/bin/python -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-gzzfb6dp/azure/setup.py'"'"'; __file__='"'"'/tmp/pip-install-gzzfb6dp/azure/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base /tmp/pip-pip-egg-info-1xop0k3_
             cwd: /tmp/pip-install-gzzfb6dp/azure/
        Complete output (24 lines):
        Traceback (most recent call last):
          File "<string>", line 1, in <module>
          File "/tmp/pip-install-gzzfb6dp/azure/setup.py", line 60, in <module>
            raise RuntimeError(message)
        RuntimeError:

        Starting with v5.0.0, the 'azure' meta-package is deprecated and cannot be installed anymore.
        Please install the service specific packages prefixed by `azure` needed for your application.

        The complete list of available packages can be found at:
        https://aka.ms/azsdk/python/all

        Here's a non-exhaustive list of common packages:

        -  azure-mgmt-compute (https://pypi.python.org/pypi/azure-mgmt-compute) : Management of Virtual Machines, etc.
        -  azure-mgmt-storage (https://pypi.python.org/pypi/azure-mgmt-storage) : Management of storage accounts.
        -  azure-mgmt-resource (https://pypi.python.org/pypi/azure-mgmt-resource) : Generic package about Azure Resource Management (ARM)
        -  azure-keyvault-secrets (https://pypi.python.org/pypi/azure-keyvault-secrets) : Access to secrets in Key Vault
        -  azure-storage-blob (https://pypi.python.org/pypi/azure-storage-blob) : Access to blobs in storage accounts

        A more comprehensive discussion of the rationale for this decision can be found in the following issue:
        https://github.com/Azure/azure-sdk-for-python/issues/10646


        ----------------------------------------
    ```

    So it's better to update this suggestion to `azure-mgmt-storage` instead.

* Fix bug #1211481 with merge from Raffaele Di Campli. [Kenneth Loafman]

    - Ignores the uid/gid from the archive and keeps the current user's
    one.
      - Recommended for restoring data to mounted filesystem which do not
        support Unix ownership or when root privileges are not available.

* Added `--do-not-restore-ownership` option. [Jacotsu]

    Ignores the uid/gid from the archive and keeps the current user's one.
    Recommended for restoring data to mounted filesystem which do not
    support Unix ownership or when root privileges are not available.

    Solves launchpad bug #1211481

* Fix bug #1887689 with patch from Matthew Barry. [Kenneth Loafman]

    - Cleanup with Paramiko backend does not remove files due to missing
        filename byte decoding

* Bump version for LP build. [Kenneth Loafman]

* Fix check for s3 glacier/deep. [Michael Terry]

    This allows encryption validation to continue to work outside of
    those s3 glacier/deep scenarios.

* Change from push to upload. [Kenneth Loafman]

* Add specific version for six. [Kenneth Loafman]


## rel.0.8.14 (2020-07-04)

### Other

* Set deprecation version to 0.9.0 for short filenames. [Kenneth Loafman]

* Fixes for issue #7, par2backend produces badly encoded filenames. [Kenneth Loafman]

* Added a couple of fsdecode calls for issue #7. [Kenneth Loafman]

* Generalize exception for failed get\_version() on LaunchPad. [Kenneth Loafman]

* Ignore *.so files. [Kenneth Loafman]

* Update docs. [Kenneth Loafman]

* Catch up on paperwork. [Kenneth Loafman]

* Fix --rename encoding. [Michael Terry]

* Skip tests failing on py27 under 18.04 (timing error). [Kenneth Loafman]

* Fix code style issue. [Kenneth Loafman]

* Add PATHS\_FROM\_ECLIPSE\_TO\_PYTHON to environ whan starting pydevd. [Kenneth Loafman]

* Add *.pyc to .gitignore. [Kenneth Loafman]

* Replace compilec.py with 'setup.py build\_ext', del compilec.py. [Kenneth Loafman]

* Fix unadorned string. [Kenneth Loafman]

* Fix usage of TOXPYTHON and overrides/bin shebangs. [Kenneth Loafman]

* Use default 'before\_script' for py27. [Kenneth Loafman]

* Don't collect coverage unless needed. [Kenneth Loafman]

* Support PyDrive2 library in the pydrive backend. [Jindrich Makovicka]

    Unlike PyDrive, the PyDrive2 fork is actively maintained.

* Tidy .gitlab-ci.yml, fix py3.5 test, add py2.7 test (allowed to fail) [Aaron Whitehouse]

* Test code instead of py27 since py27 is tested elsewhere. [Kenneth Loafman]

* Fix RdiffdirTest to use TOXPYTHON as well. [Kenneth Loafman]

* Set TOXPYTHON before tests. [Kenneth Loafman]

* Put TOXPYTHON in passed environment. [Kenneth Loafman]

* More fixes for bug #1877885 - Catch quota overflow on Mega upload. [Kenneth Loafman]

* More fixes for bug #1877885 - Catch quota overflow on Mega upload. [Kenneth Loafman]

* Undo: Try forcing python version to match tox testing version. [Kenneth Loafman]

* Always upgrade pip. [Kenneth Loafman]

* Try forcing python version to match tox testing version. [Kenneth Loafman]

* Uncomment all tests. [Kenneth Loafman]

* Test just py27 for now. [Kenneth Loafman]

* Replace bzr with git. [Kenneth Loafman]

* Don't load repo version of future, let pip do it. [Kenneth Loafman]

* Hmmm, Gitlab yaml does not like continuation lines.  Fix it. [Kenneth Loafman]

* Fix typo. [Kenneth Loafman]

* Update to use pip as module and add py35 test. [Kenneth Loafman]

* Add py35 to CI tests. [Kenneth Loafman]

* More changes to support Xenial. [Kenneth Loafman]

* Fix typo. [Kenneth Loafman]

* Fix duplicity to run under Python 3.5. [Kenneth Loafman]

* Fix duplicity to run under Python 3.5. [Kenneth Loafman]

* Update .gitlab-ci.yml to update pip before installing other pip
packages (to try to fix more-itertools issue:
https://github.com/pytest-dev/pytest/issues/4770 ) [Aaron Whitehouse]

* Don't include .git dir when building docker images. [Kenneth Loafman]

* Upgrade pip before installing requirements with it. Fixes more-
itertools error as newer versions of pip identify that the latest
more-itertools are incompatible with python 2. [Aaron Whitehouse]

* Patched in a megav2backend.py to update to MEGAcmd tools. [Kenneth Loafman]

    - Author: Jose L. Domingo Lopez <github@24x7linux.com>
      - Man pages, docs, etc. were included.

* Change log.Warning to log.Warn.  Whoops! [Kenneth Loafman]

* Fixed bug #1875937 - validate\_encryption\_settings() fails w/S3
glacier. [Kenneth Loafman]

    - Skip validation with a warning if S3 glacier or deep storage
    specified

* Restore commented our backend requirements. [Kenneth Loafman]

* Fixes for rclonebackend from Francesco Magno (original author) [Kenneth Loafman]

    - copy command has been replaced with copyto, that is a specialized
        version for single file operation. Performance-wise, we don't have
        to include a single file in the local side directory, and we don't
        have to list all the files in the remote to check what to
    syncronize.
        Additionally, we don't have to mess up with renaming because the
        copy command didn't support changing filename during transfer
        (because was oriented to transfer whole directories).
      - delete command has been replaced with deletefile. Same here, we
        have a specialized command for single file operation. Much more
    efficient.
      - ls command has been replaced with lsf, that is a specialized version
        that returns only filenames. Since duplicity needs only those, less
        bytes to transfer, and less parsing to do.
      - lastly, I have reintroduced a custom subprocess function because the
    one
        inherithed from base class is checked, and throws an exception in
    case of
        non zero return code. The ls command family returns a non zero value
    if
        the directory does not exist in the remote, so starting a new backup
        in a non existent directory is impossible at the moment because ls
    fails
        repeatedly until duplicity gives up. This is a bug in the current
    implementation.
        There is the same problem (but less severe) in _get method, using
    the default
        self.subprocess_popen a non zero return code will throw an exception
    before we
        can cleanup the partially downloaded file, if any.

* Version man pages during setup.py install. [Kenneth Loafman]

* More fixes for Launchpad build limitations. [Kenneth Loafman]

* More fixes for Launchpad build limitations. [Kenneth Loafman]

* Move setuptools\_scm to setup\_requires. [Kenneth Loafman]

* Back off requirements for fallback\_version in setup.py. [Kenneth Loafman]

* Add some requirements for LP build. [Kenneth Loafman]

* Make sure we get six from pip to support dropbox. [Kenneth Loafman]

* Provide fallback\_version for Launchpad builder. [Kenneth Loafman]

* Remove python3-setuptools-scm from setup.py. [Kenneth Loafman]

* Add python3-setuptools-scm to debian/control. [Kenneth Loafman]

* Try variation with hyphen seperator. [Kenneth Loafman]

* Try python3\_setuptools\_scm (apt repo name).  Probably too old. [Kenneth Loafman]

* Add setuptools\_scm to install\_requires. [Kenneth Loafman]


## rel.0.8.13 (2020-05-05)

### Other

* Fixed release date. [Kenneth Loafman]

* Fixed bug #1876446 - WebDAV backend creates only tiny or 0 Byte files. [Kenneth Loafman]

* Fix to run with --dist-dir command. [Kenneth Loafman]

* Fixed bug #1876778 - byte/str issues in megabackend.py. [Kenneth Loafman]

* Fix to use 'setup.py develop' instead of sdist. [Kenneth Loafman]

* Fix to run with --dist-dir command. [Kenneth Loafman]

* Fixed bug #1875529 - Support hiding instead of deletin on B2. [Kenneth Loafman]

* Uncomment upload and sign. [Kenneth Loafman]

* Reworked versioning to be git tag based. [Kenneth Loafman]

* Migrate bzr to git. [Kenneth Loafman]

* Fixed bug #1872332 - NameError in ssh\_paramiko\_backend.py. [ken]

* Fix spelling error. [ken]

* Fixed bug #1869921 - B2 backup resume fails for TypeError. [ken]

* More changes for pylint. * Resolved conflict between duplicity.config
and testing.manual.config * Normalized emacs mode line to have
encoding:utf8 on all *.py files. [Kenneth Loafman]

* More changes for pylint. * Remove copy.com refs. [Kenneth Loafman]

* More changes for pylint. [Kenneth Loafman]

* More changes for pylint. [Kenneth Loafman]

* Enable additional pylint warnings.  Make 1st pass at correction.   -
unused-argument,     unused-wildcard-import,     redefined-builtin,
bad-indentation,     mixed-indentation. [Kenneth Loafman]

* Fixed bug #1868414 - timeout parameter not passed to   BlobService for
Azure backend. [Kenneth Loafman]


## rel.0.8.12 (2020-03-19)

### Other

* Fixed bug #1867742 - TypeError: fsdecode()   takes 1 positional
argument but 2 were given   with PCA backend. [Kenneth Loafman]

* Fixed bug #1867529 - UnicodeDecodeError: 'ascii'   codec can't decode
byte 0x85 in position 0:   ordinal not in range(128) with PCA. [Kenneth Loafman]

* Fixed bug #1867468 - UnboundLocalError (local   variable 'ch\_err'
referenced before assignment)   in ssh\_paramiko\_backend.py. [Kenneth Loafman]

* Fixed bug #1867444 - UnicodeDecodeError: 'ascii'   codec can't decode
byte 0x85 in position 0:   ordinal not in range(128) using PCA backend. [Kenneth Loafman]

* Fixed bug #1867435 - TypeError: must be str,   not bytes using PCA
backend. [Kenneth Loafman]

* Move pylint config from test\_code to pylintrc. [Kenneth Loafman]

* Cleaned up some setup issues where the man pages   and snapcraft.yaml
were not getting versioned. [Kenneth Loafman]

* Fixed bug #1769267 - [enhancement] please consider   using rclone as
backend. [Kenneth Loafman]

* Fixed bug #1755955 - best order is unclear,   of exclude-if-present
and exclude-device-files   - Removed warning and will now allow these
two to     be in any order.  If encountered outside of the     first
two slots, duplicity will silently move     them to be in the first
two slots.  Within those     two slots the order does not matter. [ken]

* Fixed a couple of file history bugs:   - #1044715 Provide a file
history feature     + removed neutering done between series   -
#1526557 --file-changed does not work     + fixed str/bytes issue
finding filename. [ken]

* Fixed bug #1865648 - module 'multiprocessing.dummy' has   no attribute
'cpu\_count'.   - replaced with module psutil for cpu\_count() only
- appears Arch Linux does not support multiprocessing. [ken]

* Mod to get focal build on LP working. [ken]

* Mod to get focal build on LP working. [ken]

* Mod to get focal build on LP working. [ken]


## rel.0.8.11 (2020-02-24)

### Other

* Fixed to work around par2 0.8.1 core dump on short name   -
https://github.com/Parchive/par2cmdline/issues/145. [ken]

* Fixed bug #1857818 - startswith first arg must be bytes   - use
util.fsdecode on filename. [ken]

* Fixed bug #1863018 - mediafire backend fails on py3   - Fixed handling
of bytes filename in url. [ken]

* Add rclone requirement to snapcraft.yaml. [ken]

* Fixed bug #1236248 - --extra-clean clobbers old backups   - Removed
--extra-clean, code, and docs. [ken]

* Fixed bug #1862672 - test\_log does not respect TMPDIR   - Patch
supplied by Jan Tojnar. [ken]

* Fixed bug #1860405 - Auth mechanism not supported   - Added
python3-boto3 requirement to snapcraft.yaml. [ken]

* More readthedocs munges. [ken]

* Don't format the po files for readthedocs. [ken]

* Add readthedocs.yaml config file, try 3. [ken]

* Add readthedocs.yaml config file, try 2. [ken]

* Add readthedocs.yaml config file. [ken]

* Remove intltool for readthedocs builder. [ken]

* Add python-gettext for readthedocs builder. [ken]

* Add gettext/intltool for readthedocs builder. [ken]

* Add gettext for readthedocs builder. [ken]

* Add intltool for readthedocs builder. [ken]

* Add intltools for readthedocs builder. [ken]

* Add intltools for readthedocs builder. [ken]

* Point readthedocs.io to this repo. [ken]

* Renamed botobackend.py to s3\_boto\_backend.py. [ken]

* Renamed MulitGzipFile to GzipFile to avoid future problems with
upstream author of mgzip fixing the Mulit -> Multi typo. [Byron Hammond]

* Adding missed mgzip import and adjusting untouched unit tests. [Byron Hammond]

* Adding multi-core support by using mgzip instead of gzip. [Byron Hammond]

* Missing comma. [ken]

* Some code cleanup and play with docs. [ken]

* Uncomment snapcraft sign-build.  Seems it's fixed now. [ken]

* Fix argument order on review-tools. [ken]

* Reworked setup.py to build a pip-compatible   distribution tarball of
duplicity. * Added dist/makepip for convenience. [ken]

* Adjust Dockerfiles to new requirements. [ken]

* Fix bug #1861287 - Removing old backup chains   fails using
pexpect+sftp. [ken]

* Adjust Dockerfiles to new requirements. [ken]

* Enhance setup.py/cfg to allow install by pip. [ken]

* Enhance setup.py/cfg to allow install by pip. [ken]

* Enhance setup.py/cfg to allow install by pip. [ken]

* Bump version. [Kenneth Loafman]

* Gave up fighting the fascist version control   munging on
snapcraft.io.  Duplicity now has the   form 0.8.10.1558, where the
last number is the   bzr revno.  Can't do something nice like having
a dev/fin indicator like 0.8.10dev1558 for dev   versions and a fin
for release or final. [Kenneth Loafman]


## rel.0.8.10 (2020-01-23)

### Other

* Fixed bug #1858207 missing targets in multibackend   - Made it
possible to return default value instead     of taking a fatal
exception on an operation by     operation approach.  The only use
case now is for     multibackend to be able to list all targets and
report back on the ones that don't work. [Kenneth Loafman]

* Fixed bug #1858204 - ENODEV should be added to   list of recognized
error stringa. [Kenneth Loafman]

* Comment out test\_compare, again. [Kenneth Loafman]

* Clean up deprecation errors in Python 3.8. [Kenneth Loafman]

* Clean up some TODO tasks in testing code. [kenneth@loafman.com]

* Skip functional/test\_selection::TestUnicode if   python version is
less than 3.7. [kenneth@loafman.com]

* Fixed bug #1859877 - syntax warning on python 3.8. [kenneth@loafman.com]

* Move to single-sourceing the package version   - Rework setup.py,
dist/makedist, dist/makesnap,     etc., to get version from
duplicity/\_\_init\_\_.py   - Drop dist/relfiles.  It was problematic. [kenneth@loafman.com]

* Fixed bug #1859304 with patch from Arduous   - Backup and restore do
not work on SCP backend. [kenneth@loafman.com]

* Revert last change to duplicity.\_\_init\_\_.py. [kenneth@loafman.com]

* Py27 supports unicode returns for translations   - remove install that
does not incude unicode   - Removed some unneeded includes of gettext. [kenneth@loafman.com]

* Fixed bug #1858713 - paramiko socket.timeout   - chan.recv() can
return bytes or str based on     the phase of the moon.  Make
allowances. [kenneth@loafman.com]

* Switched to python3 for snaps. [kenneth@loafman.com]

* Fix unadorned string. [kenneth@loafman.com]


## rel.0.8.09 (2020-01-07)

### Other

* Change of plans.  Skip test if rclone not present. [kenneth@loafman.com]

* Add rclone to setup testing requirements. [kenneth@loafman.com]

* Revert to testing after build. [kenneth@loafman.com]

* Fixed bug #1855736 again - Duplicity fails to start   - remove decode
from unicode string. [kenneth@loafman.com]

* Fixed bug #1858295 - Unicode error in source filename   - decode arg
if it comes in as bytes. [kenneth@loafman.com]

* Add snapcraft login to makesnap. [kenneth@loafman.com]

* Fix bug #1858153 with patch from az   - mega backend: fails to create
directory. [kenneth@loafman.com]

* Fix bug #1857734 - TypeError in ssh\_paramiko\_backend   - conn.recv()
can return bytes or string, make string. [kenneth@loafman.com]

* Fix bytes/string differences in subprocess\_popen()   - Now returns
unicode string not bytes, like python2. [kenneth@loafman.com]

* Convert all shebangs to python3 for bug #1855736. [kenneth@loafman.com]

* Fixed bug #1857554 name 'file' is not defined   - file() calls
replaced by open() in 3 places. [kenneth@loafman.com]

* Original rclonebackend.py from Francesco Magno for Python 2.7. [kenneth@loafman.com]

* Fix manpage indention clarify difference between boto backends add
boto+s3:// for future use when boto3+s3:// will become default s3
backend. [ed.so]

* Renamed testing/infrastructure to testing/docker. [kenneth@loafman.com]

* Fixed a mess I made.  setup.py was shebanged to   Py3, duplicity was
shebanged to Py2.  This meant   that duplicity ran as Py2 but could
not find its   modules because they were under Py3.  AArgh! [kenneth@loafman.com]

* Fixed bug #1855736 - duplicity fails to start   - Made imports
absolute in dup\_main.py. [kenneth@loafman.com]

* Fixed bug #1856447 with hint from Enno L   - Replaced with formatted
string. [kenneth@loafman.com]

* Fixed bug #1855736 with help from Michael Terry   - Decode Popen
output to utf8. [kenneth@loafman.com]

* Fixed bug #1855636 with patch from Filip Slunecko   - Wrong buf type
returned on error.  Make bytes. [kenneth@loafman.com]


## rel.0.8.08 (2019-12-08)

### Other

* Merged in translation updates. [kenneth@loafman.com]

* Removed abandoned ref in README * Comment out signing in makesnap. [kenneth@loafman.com]

* Fixed bug #1854554 with help from Tommy Nguyen   - Fixed a typo made
during Python 3 conversion. [kenneth@loafman.com]

* Fixed bug #1855379 with patch from Daniel González Gasull   - Issue
warning on temporary connection loss. * Fixed misc coding style
errors. [kenneth@loafman.com]

* Disabling autotest for LP build.  I have run tests on all Ubuntu
releases since 18.04, so the code works.  To run tests manually, run
tox from the main directory.  Maybe LP build will work again soon. [kenneth@loafman.com]

* Update to manpage. [Carl A. Adams]

* BUGFIX: list should retun byte strings, not unicode strings. [Carl A. Adams]

* Updating comments. [Carl A. Adams]

* Select boto3/s3 backend via url scheme rather than by CLI option.  Doc
changes to support this. [Carl A. Adams]

* Renaming boto3 backend file. [Carl A. Adams]

* Adding support for AWS Glacier Deep Archive.  Fixing some typos. [Carl A. Adams]

* Manpage updates.  Cleaning up the comments to reflect my current
plans. Some minor clean-ups. [Carl A. Adams]

* Updating comments. [Carl A. Adams]

* SSE options comitted. AES tested, KMS not tested. [Carl A. Adams]

* Handling storage class on backup. [Carl A. Adams]

* Handling storage class on backup. [Carl A. Adams]

* Minor clean-ups. [Carl A. Adams]

* Rename boto3 backend py file. [Carl A. Adams]

* Removing 'todo' comment for multi support.  Defaults in Boto3 chunk
the upload and attempt to use multiple threads.  See https://boto3.ama
zonaws.com/v1/documentation/api/latest/reference/customizations/s3.htm
l#boto3.s3.transfer.TransferConfig. [Carl A. Adams]

* Format fix. [Carl A. Adams]

* Fixing status reporting.  Cleanup. [Carl A. Adams]

* Better exception handling. Return -1 for unknwon objects in \_query. [Carl A. Adams]

* Updating comment. [Carl A. Adams]

* Making note of a bug. [Carl A. Adams]

* Removing unused imports. [Carl A. Adams]

* Implementing \_query for boto3. [Carl A. Adams]

* Minor clean-up. [Carl A. Adams]

* Some initial work on a boto3 back end. [Carl A. Adams]

* Convert debian build to Python 3. [kenneth@loafman.com]

* Replace python with python3 in shebang. [kenneth@loafman.com]

* Convert debian build to Python 3. [kenneth@loafman.com]

* Fixed bug #1853809 - Tests failing with Python 3.8 / Deprecation
warnings   - Fixed the deprecation warnings with patch from Sebastien
Bacher   - Fixed test\_globmatch to handle python 3.8 same as 3.7   -
Fixed tox.ini to include python 3.8 in future tests. [kenneth@loafman.com]

* Fixed bug #1853655 - duplicity crashes with --exclude-older-than   -
The exclusion setup checked for valid string only.  Made     the code
comprehend datetime (int) as well. [kenneth@loafman.com]

* Just some cosmetic changes. [kenneth@loafman.com]

* Fixed bug #1851668 with help from Wolfgang Rohdewald   - Applied
patches to handle translations. [kenneth@loafman.com]

* Fixed bug #1852876 '\_io.BufferedReader' object has no attribute
'uc\_name'   - Fixed a couple of instances where str() was used in
place of util.uexc()   - The file was opened with builtins, so use
name, not uc\_name. [kenneth@loafman.com]

* Added build signing to dist/makesnap. [kenneth@loafman.com]

* Fixed bug #1852848 with patch from Tomas Krizek   - B2 moved the API
from "b2" package into a separate "b2sdk" package.     Using the old
"b2" package is now deprecated. See link:     https://github.com/Backb
laze/B2\_Command\_Line\_Tool/blob/master/b2/\_sdk\_deprecation.py   -
b2backend.py currently depends on both "b2" and "b2sdk", but use of
"b2"     is enforced and "b2sdk" isn't used at all.   - The attached
patch uses "b2sdk" as the primary dependency. If the new     "b2sdk"
module isn't available, it falls back to using the old "b2" in
order to keep backward compatibility with older installations. [kenneth@loafman.com]


## rel.0.8.07 (2019-11-14)

### Other

* Fixed bug #1851727 - InvalidBackendURL for multi backend   - Encode to
utf8 only on Python2, otherwise leave as unicode. [kenneth@loafman.com]

* Fix resuming without a passphrase when using just an encryption key. [Michael Terry]

* Fix bytes/string issue in pydrive backend upload. [Michael Terry]

* Fixed bug #1851167 with help from Aspen Barnes   - Had Popen() to
return strings not bytes. [kenneth@loafman.com]

* Added dist/makesnap to make spaps automagically. [kenneth@loafman.com]

* Fixed bug #1850990 with suggestion from Jon Wilson   - --s3-use-
glacier and --no-encryption cause slow backups. [kenneth@loafman.com]

* Fix header in CHANGELOG. [kenneth@loafman.com]

* Added b2sdk to snapcraft.yaml * Fixed bug #1850440 - Can't mix strings
and bytes. [kenneth@loafman.com]


## rel.0.8.06 (2019-11-05)

### Other

* Updated snapcraft.yaml to remove python-lockfile and fix spelling. [kenneth@loafman.com]

* Updated snapcraft.yaml to remove rdiffdir and add libaft1 to stage. [kenneth@loafman.com]

* Updated snapcraft.yaml to include rdiffdir and did some reformatting. [kenneth@loafman.com]

* Updated snapcraft.yaml to include rdiffdir and did some reformatting. [kenneth@loafman.com]

* Removed file() call in swiftbackend.  It's been deprecated since py2. [kenneth@loafman.com]

* Revisited bug #1848783 - par2+webdav raises TypeError on Python 3   -
Fixed so bytes filenames were compared as unicode in re.match() [kenneth@loafman.com]

* Removed a couple of disables from pylint code test.   - E1103 - Maybe
has no member   - E0712 - Catching an exception which doesn't inherit
from BaseException. [kenneth@loafman.com]

* Added additional fsdecode's to uses of local\_path.name and
source\_path.name in b2backend's \_get() and \_put.  See bug
#1847885 for more details. [kenneth@loafman.com]

* Fixed bug #1849661 with patch from Graham Cobb   - The problem is that
b2backend uses 'quote\_plus' on the     destination URL without
specifying the 'safe' argument as     '/'. Note that 'quote' defaults
'safe' to '/', but     'quote\_plus' does not! [kenneth@loafman.com]

* Fixed bug #1848166 - Swift backend fails on string concat   - added
util.fsdecode() where needed. [kenneth@loafman.com]

* Fixed bug #1848783 with patch from Jacob Middag   - Don't use b''
strings in re.* [kenneth@loafman.com]

* Fixed bug #1848783 with patch from Jacob Middag   - Don't use b''
strings in re.* [kenneth@loafman.com]

* Fixed bug #1626061 with patch from Michael Apozyan   - While doing
multipart upload to s3 we need to report the     total size of
uploaded data, and not the size of each part     individually.  So we
need to keep track of all parts     uploaded so far and sum it up on
the fly. [kenneth@loafman.com]

* Removed revision 1480 until patch is validated. [kenneth@loafman.com]

* Fixed bug #1626061 with patch from Michael Apozyan   - While doing
multipart upload to s3 we need to report the     total size of
uploaded data, and not the size of each part     individually.  So we
need to keep track of all parts     uploaded so far and sum it up on
the fly. [kenneth@loafman.com]

* Fixed bug #1848203 with patch from Michael Apozyan   - convert to
integer division. [kenneth@loafman.com]

* Fix unadorned string. [kenneth@loafman.com]

* Fix unadorned string. [kenneth@loafman.com]

* Update changelogs. [Adam Jacobs]

* In version 1 of the B2sdk, the list\_file\_names method is removed
from the B2Bucket class. [Adam Jacobs]

    This change makes the b2 backend backwards-compatible with the old version 0 AND forward-compatible with the new version 1.

* Complete fix for string concatenation in b2 backend. [Adam Jacobs]

* Fixed Resouce warnings when using paramiko.  It turns out   that
duplicity's ssh\_paramiko\_backend.py was not handling   warning
suppression and ended up clearing all warnings,   including those that
default to off. [kenneth@loafman.com]

* Fixed Resouce warnings when using paramiko.  It turns out   that
duplicity's ssh\_paramiko\_backend.py was not handling   warning
suppression and ended up clearing all warnings,   including those that
default to off. [kenneth@loafman.com]


## rel.0.8.05 (2019-10-07)

### Other

* Removed a setting in tox.ini that causes coverage to   be activated
during testing duplicity. [kenneth@loafman.com]

* Fixed bug #1846678 - --exclude-device-files and -other-filesystems
crashes   - assuming all options had arguments was fixed. [kenneth@loafman.com]

* Fixed bug #1844950 - ssh-pexpect backend syntax error   - put the
global before the import. [kenneth@loafman.com]

* Fixed bug #1846167 - webdavbackend.py: expected bytes-like object, not
str   - base64 now returns bytes where it used to be strings, so just
decode(). [kenneth@loafman.com]

* Fixed bug reported on maillist - Python error in Webdav backend.  See:
https://lists.nongnu.org/archive/html/duplicity-
talk/2019-09/msg00026.html. [kenneth@loafman.com]

* Fix bug #1844750 - RsyncBackend fails if used with multi-backend.   -
used patch provided by KDM to fix. [kenneth@loafman.com]

* Fix bug #1843995 - B2 fails on string concatenation.   - use
util.fsdecode() to get a string not bytes. [kenneth@loafman.com]

* Clean up some pylint warnings. [kenneth@loafman.com]

* Add testenv:coverage and took it out of defaults.  Some cleanup. [kenneth@loafman.com]

* Fix MacOS tempfile selection to avoid /tmp and /var/tmp.  See thread:
https://lists.nongnu.org/archive/html/duplicity-
talk/2019-09/msg00000.html. [kenneth@loafman.com]

* Sort of fix bugs #1836887 and #1836888 by skipping the   tests under
question when running on ppc64el machines. [kenneth@loafman.com]

* Added more python future includes to support using   python3 code
mixed with python2. [kenneth@loafman.com]

* Fix exc.args handling.  Sometimes it's (message, int),   other times
its (int, message).  We look for the   message and use that for the
exception report. [kenneth@loafman.com]

* Adjust exclusion list for rsync into duplicity\_test. [kenneth@loafman.com]

* Set to allow pydevd usage during tox testing. [kenneth@loafman.com]

* Don't add extra newline when building dist/relfiles.txt. [kenneth@loafman.com]

* Changed dist/makedist to fall back to dist/relfiles.txt   in case bzr
or git is not available to get files list.   Tox sdist needs setup.py
which needs dist/makedist. * Updatated LINGUAS file to add four new
translations. [kenneth@loafman.com]


## rel.0.8.04 (2019-08-31)

### Other

* Made some changes to the Docker infrastructure:   - All scripts run
from any directory, assuming directory     structure remains the same.
- Changed from Docker's COPY internal command which is slow to
using external rsync which is faster and allows excludes.   - Removed
a couple of unused files. [kenneth@loafman.com]

* Run compilec.py for code tests, it needs the import. [kenneth@loafman.com]

* Simplify README-TESTING and change this to recommend using the Docker
images to test local branches in a known-good environment. [Aaron A Whitehouse]

* Convert Dockerfile-19.10 to new approach (using local folder instead
of remote repo) * run-tests passes on 19.10 Docker (clean: commands
succeeded; py27: commands succeeded; SKIPPED: py36:
InterpreterNotFound: python3.6; py37: commands succeeded; report:
commands succeeded) [Aaron A Whitehouse]

* Convert Dockerfile-19.04 to new approach (using local folder instead
of remote repo) * run-tests passes on 19.04 Docker (clean: commands
succeeded; py27: commands succeeded; SKIPPED:  py36:
InterpreterNotFound: python3.6;  py37: commands succeeded; report:
commands succeeded) [Aaron A Whitehouse]

* Edit Dockerfile-18.10 to use the local folder. * Tests all pass on
18.10 except for the same failures as trunk (4 failures on python 3.6:
TestUnicode.test\_unicode\_filelist;
TestUnicode.test\_unicode\_paths\_asterisks;
TestUnicode.test\_unicode\_paths\_non\_globbing;
TestUnicode.test\_unicode\_paths\_square\_brackets) [Aaron A Whitehouse]

* Use local folder instead of bzr revision, so remove the revision
arguments in the setup script. * Modify Dockerfile and
Dockerfile-18.04 to copy the local folder rather than the remote
repository. * Tests all pass on 18.04 except for the same failures as
trunk (4 failures on python 3.6: TestUnicode.test\_unicode\_filelist;
TestUnicode.test\_unicode\_paths\_asterisks;
TestUnicode.test\_unicode\_paths\_non\_globbing;
TestUnicode.test\_unicode\_paths\_square\_brackets) [Aaron A Whitehouse]

* Fix .bzrignore. [kenneth@loafman.com]

* Encode Azure backend file names. [Frank Fischer]

* Change README-TESTING to be correct for running individual tests now
that we have moved to Pytest. [Aaron A Whitehouse]

* Fix debian/rules file. [kenneth@loafman.com]

* Fix setup.py shebang. [kenneth@loafman.com]

* Fix debian/rules file. [kenneth@loafman.com]

* Fix debian/rules file. [kenneth@loafman.com]

* Fix debian/rules file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Ran futurize selectively filter-by-filter to find the ones that work. [kenneth@loafman.com]

* Fixed build on Launchpad for 0.8.x, so now there is a new PPA at
https://launchpad.net/\~duplicity-team/+archive/ubuntu/daily-dev-trunk. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Fix debian/control file. [kenneth@loafman.com]

* Add snap package creation files * Modify dist/makedist to version the
snapcraft.yaml. [Aaron A Whitehouse]

* Remove a mess I made. [Kenneth Loafman]

* Fixed bug #1839886 with hint from denick   - Duplicity crashes when
using --file-prefix * Removed socket.settimeout from backend.py.   It
was already set in commandline.py. * Removed pycryptopp from README
requirements. [kenneth@loafman.com]

* Fixed bug #1839728 with info from Avleen Vig   - b2 backend requires
additional import. [kenneth@loafman.com]

* Convert the docker duplicity\_test image to pull the local branch into
the container, rather than lp:duplicity. This allows the use of the
duplicity Docker testing containers to test local changes in a known-
good environment before they are merged into trunk. The equivalent of
the old behaviour can be achieved by starting with a clean branch from
lp:duplicity. * Expand Docker context to parent branch folder and use
-f in the docker build command to point to the Dockerfile. * Simplify
build-duplicity\_test.sh now that the whole folder is copied
(individual files no longer need to be copied) [Aaron A Whitehouse]


## rel.0.8.03 (2019-08-09)

### Other

* More changes to provide Python test coverage:   - Moved bulk of code
from bin/duplicity to     duplicity/dup\_main.py for coverage. * Fixed
some 2to3 issues in dup\_main.py * Fixed division differences with
futurize. [kenneth@loafman.com]

* More changes to provide Python test coverage:   - Moved bulk of code
from bin/duplicity to     duplicity/dup\_main.py for coverage. * Fixed
some 2to3 issues in dup\_main.py * Fixed division differences with
futurize. [kenneth@loafman.com]

* More changes to provide Python test coverage:   - Moved bulk of code
from bin/duplicity to     duplicity/dup\_main.py for coverage. * Fixed
some 2to3 issues in dup\_main.py. [kenneth@loafman.com]

* More changes to provide Python test coverage:   - Now covers
functional tests spawning duplicity   - Does not cover bin/duplicity
for some reason. [kenneth@loafman.com]

* Fixed bugs #1838427 and #1838702 with a fix   suggested by Stephen
Miller.  The fix was to   supply tarfile with a unicode grpid, not
bytes. [kenneth@loafman.com]

* Some changes to provide Python test coverage:   - Coverage runs with
every test cycle   - Does not cover functional tests that spawn
duplicity itself.  Next pass.   - After a run use 'coverage report
html' to see     an overview list and links to drill down.  It
shows up in htmlcov/index.html. [kenneth@loafman.com]


## rel.0.8.02 (2019-07-31)

### Other

* Fix dist/makedist to run on python2/3. [kenneth@loafman.com]

* Fix dist/makedist to run on python3. [kenneth@loafman.com]

* Fix dist/makedist to run on python3. [kenneth@loafman.com]

* One last change for bug #1829416 from charlie4096. [kenneth@loafman.com]

* Enhanced build\_duplicity\_test.sh   - Use -h to get help and defaults
- Takes arguments for distro, revno, help   - Distros supported are
18.04, 18.10, 19.04, 19.10   - Revnos are passed to bzr -r option. [kenneth@loafman.com]

* Fix so Docker image duplicity\_test will update and pull   new bzr
revisions if changed since last build. [kenneth@loafman.com]

* Remove speedup in testing backup.  The math was correct,   but it's
failing on Docker and Launchpad testing. [kenneth@loafman.com]

* Move pytest-runner setup requirement to a test requirement. [Michael Terry]

* Removed python-gettext from setup.py.  Whoops! [kenneth@loafman.com]

* Optimize loading backup chains; reduce file\_naming.parse calls. [Matthew Glazar]

    For each filename in filename_list,
    CollectionsStatus.get_backup_chains calls file_naming.parse
    (through BackupSet.add_filename) between 0 and len(sets)*2
    times. In the worst case, this leads to a *ton* of redundant
    calls to file_naming.parse.

    For example, when running 'duplicity collection-status' on
    one of my backup directories:

    * filename_list contains 7545 files
    * get_backup_chains creates 2515 BackupSet-s
    * get_backup_chains calls file_naming.parse 12650450 times!

    This command took 9 minutes and 32 seconds. Similar
    commands, like no-op incremental backups, also take a long
    time. (The directory being backed up contains only 9 MiB
    across 30 files.)

    Avoid many redundant calls to file_naming.parse by hoisting
    the call outside the loop over BackupSet-s. This
    optimization makes 'duplicity collection-status' *20 times
    faster* for me (572 seconds -> 29 seconds).

    Aside from improving performance, this commit should not
    change behavior.

* Correct types for os.join in Dropbox backend. [Gwyn Ciesla]

* Fixed bug #1836829 progress.py: old\_div not defined   - also fixed
old\_div in \_boto\_multi.py. [kenneth@loafman.com]

* Fixed bug #1836829 progress.py: old\_div not defined   - also fixed
old\_div in \_boto\_multi.py. [kenneth@loafman.com]

* Remove python-gettext from requirements.txt.  Normal   Python
installation includes gettext. * Mod README to include Python 3.6 and
3.7. [kenneth@loafman.com]


## rel.0.8.01 (2019-07-14)

### Other

* Comment out HSIBackendTest since shim is not up-to-date. [kenneth@loafman.com]

* Install python3.6 and 3.7 explicitly in Dockerfile.  Tox and Docker
now support testing Python 2,7, 3.6, and 3.7. [kenneth@loafman.com]

* Make sure test filenames are bytes not unicode. * Fix
test\_glob\_to\_regex to work on Python 3.7. [kenneth@loafman.com]

* Going back to original.  No portable way to ignore warning. [kenneth@loafman.com]

* Another unadorned string. [kenneth@loafman.com]

* Cleanup some trailing spaces/lines in Docker files. [kenneth@loafman.com]

* Fix so we start duplicity with the base python we run under. [kenneth@loafman.com]

* Adjust POTFILES.in for compilec.py move. [kenneth@loafman.com]

* Ensure \_librsync.so is regenned before toc testing. [kenneth@loafman.com]

* Add encoding to logging.FileHandler call to make log file utf8. [kenneth@loafman.com]

* Fix warning in \_librsync.c module. [kenneth@loafman.com]

* Fix some issues found by test\_code.py (try 2) [kenneth@loafman.com]

* Fix some issues found by test\_code.py. [kenneth@loafman.com]

* Fix reversed port assignments (FTP & SSH) in docker-compose.yml. [kenneth@loafman.com]

* Fix reimport problem where "from future.builtins" was being treated
the differently than "from builtins".  They are both the same, so
converted to shorter form "from builtins" and removed duplicates. [kenneth@loafman.com]

* Fix s3 backups by encoding remote filenames. [Michael Terry]

* Add 2to3 as a dependency to dockerfile. [Aaron A. Whitehouse]

* Add tzdata back in as a dependency and set
DEBIAN\_FRONTEND=noninteractive so no tzdata prompt. [Aaron A. Whitehouse]

* Set docker container locale to prevent UTF-8 errors. [Aaron A. Whitehouse]

* Change dockerfile to use 18.04 instead of 16.04 and other fixes. [Aaron A. Whitehouse]

* Fix s3 backups by importing the boto module. [Michael Terry]

* Normalize shebang to just python, no version number * Fix so most
testing/*.py files have the future suggested lines   - from
\_\_future\_\_ import print\_function     from future import
standard\_library     standard\_library.install\_aliases() [kenneth@loafman.com]

* Fixed failing test in testing/unit/test\_globmatch.py   - Someone is
messing with regex.  Fix same.   - See
https://bugs.python.org/issue29995 for details. [kenneth@loafman.com]

* Fixed bug #1833559 0.8 test fails with 'duplicity not found' errors
- Fixed assumption that duplicity/rdiffdir were in $PATH. [kenneth@loafman.com]

* Fixed bug #1833573 0.8.00 does not work on Python 2   - Fixed shebang
to use /usr/bin/python instead of python2. [kenneth@loafman.com]

* Fix some test\_code errors that slipped by. [kenneth@loafman.com]

* Fix Azure backend for python 3. [Frank Fischer]

    By definition, the list of keys from "list" is byte-formatted.
    As such we have to decode the parameter offered to "get"

* Fixed bug #1831178 sequence item 0: expected str instance, int found
- Simply converted int to str when making list. [kenneth@loafman.com]

* Fix some import conflicts with the "past" module   - Rename
collections.py to dup\_collections.py   - Remove all "from
future.utils import old\_div"   - Replace old\_div() with "//" (in
py27 for a while).   - All tests run for py3, unit tests run for py3.
The new     import fail is "from future import standard\_library" [kenneth@loafman.com]

* Spaces to tabs for makefile. [Kenneth Loafman]

* Change to python3 for build. [kenneth@loafman.com]

* Have uexc to always return a string. [Michael Terry]

    This fixes unhandled exception reporting

* Add requirements for python-gettext. [kenneth@loafman.com]

* Fix gio and pydrive backends to use fsdecode. [Michael Terry]


## rel.0.8.00 (2019-05-29)

### Other

* Remove unnecessary sleeping after running backups in tests. [Matthew Glazar]

    ptyprocess' 'PtyProcess.close' function [1] closes the
    terminal, then terminates the process if it's still alive.
    Before checking if the process is alive, ptyprocess
    unconditionally sleeps for 100 milliseconds [2][3].

    In 'run_duplicity', after we call 'child.wait()', we know
    that the process is no longer alive. ptyprocess' 100 ms
    sleep just slows down tests. Tell ptyprocess to not sleep.

    [1] pexpect uses ptyprocess. 'PtyProcess.close' is called by
        'PtyProcess.__del__', so 'PtyProcess.close' is called
        when 'run_duplicity' returns.
    [1] https://github.com/pexpect/ptyprocess/blob/3931cd45db50ee8533b8b0fef424b8d75f7ba1c2/ptyprocess/ptyprocess.py#L403
    [2] https://github.com/pexpect/ptyprocess/blob/3931cd45db50ee8533b8b0fef424b8d75f7ba1c2/ptyprocess/ptyprocess.py#L173

* Minimize time spent sleeping between backups. [Matthew Glazar]

    During testing, if a backup completes at time 10:49:30.621,
    the next call to 'backup' sleeps to ensure the new backup
    has a different integer time stamp (10:49:31). Currently,
    'backup' sleeps for an entire second, even though the next
    integer time stamp is less than half a second away (0.379
    seconds). This extra sleeping causes tests to take longer
    than they need to.

    Make tests run faster by sleeping only enough to reach the
    next integer time stamp.

* Ensure all duplicity output is captured in tests. [Matthew Glazar]

    The loop in 'run_duplicity' which captures output has a race
    condition. If duplicity writes output then exits before
    'child.isalive()' is called, then 'run_duplicity' exits the
    loop before calling 'child.readline()'. This means that some
    output is not read into the 'lines' list.

    Fix this race condition by reading all output until EOF,
    then waiting for the child to exit.

* Fix TestGlobToRegex.test\_glob\_to\_regex for py3.6 and above   - see
https://bugs.python.org/issue29995 for details. [kenneth@loafman.com]

* Some more work on unadorned strings   - Fixed
test\_unadorned\_string\_literals to list all strings found   - Added
bin/duplicity and bin/rdiffdir to list of files tested   - All
unadorned strings have now been adorned. [kenneth@loafman.com]

* Fixed bug #1828662 with patch from Bas Hulsken   - string.split() had
been deprecated in 2, removed in 3.7. [kenneth@loafman.com]

* Setup.py: allow python 2.7 again. [Mike Gorse]

* Bug #1828869: update CollectionsStatus after sync. [Mike Gorse]

* Imap: python 3 fixes. [Mike Gorse]

* Sync: handle parsed filenames without start/end times. [Mike Gorse]

    Signatures set time, rather than start_time and end_time, so comparisons
    against the latter generate an exception on Python 3.

* More PEP 479 fixes. [Mike Gorse]

* Fix some unadorned strings. [kenneth@loafman.com]

* Fix some unadorned strings. [kenneth@loafman.com]

* Fix to allow >=2.7 or >=3.5. [kenneth@loafman.com]

* Fix to always compile \_librsync before testing. [kenneth@loafman.com]

* Manual merge of lp:\~yajo/duplicity/duplicity   - Support partial
metadata sync.   - Fixes bug #1823858 by letting the user to choose
partial syncing. Only the metadata for the target chain     will be
downloaded. If older (or newer) chains are encrypted with a different
passphrase, the user will     be able to restore to a given time by
supplying only the passphrase for the chain selected by     the
`--restore-time` option when using this new option.   - A side effect
is that using this flag reduces dramatically the sync time when moving
files from one to     another location, in cases where big amounts of
chains are found. [kenneth@loafman.com]

* Change to Python >= 3.5. [kenneth@loafman.com]

* Added documentation on how to use the new AWS S3 Glacier option. [Brandon Anderson]

* Fixed a typo in prior commit. [Brandon Anderson]

* Added support for AWS glacier storage class. [Brandon Anderson]

* Fix bug #1811114 with revised onedrivebackend.py from David Martin   -
Adapt to new Microsoft Graph API. [kenneth@loafman.com]

* Removed last mention of copy.com from man page with help from edso. [kenneth@loafman.com]

* Fix pylint style issues (over-indented text, whitespace on blank lines
etc) * Removed "pylint: disable=bad-string-format-type" comment, which
was throwing an error and does not seem to be needed. [Aaron A Whitehouse]

* Accomodate unicode input for uexc and add test for this. [Aaron A Whitehouse]

* Convert deprecated .message to args[0] [Aaron A Whitehouse]

* Add test case for lp:1770929 * Added fix (though using deprecated
.message syntax) [Aaron A Whitehouse]

* Attempt to port sx backend to python 3. [Mike Gorse]

    Untested, but likely needed changes similar to some other backends.

* Rsync: py3 fixes. [Mike Gorse]

* Ncftp: py3 fixes. [Mike Gorse]

* Test\_selection.py: fix an invalid escape sequence on py3. [Mike Gorse]

* Fix sync\_archive on python 3. [Mike Gorse]

    The recognized suffixes were being stored as unicode, but they were being
    compared against filenames that are stored as bytes, so the comparisons
    were failing.

* Ssh\_pexpect: py3 fixes. [Mike Gorse]

* Fixed bug #1817375 with hint from mgorse   - Added 'global pexpect' at
end of imports. [kenneth@loafman.com]

* Pydrive: delete temporary root file. [Michael Terry]

* \_\_unicode\_\_ -> \_\_str\_\_ [Mike Gorse]

* Fix a regex substitution on python 3. [Mike Gorse]

* Return temporary filenames as bytes. [Mike Gorse]

    We should be consistent in terms of the class used for filenames.
      Fixes warnings about forgetting unknown tempfiles.

* Modify some generators to return when finished. [Mike Gorse]

    Per PEP 479, the proper way to terminate a generator is to return, rather
    than throwing StopIteration.
    Fixes a traceback on Python 3 where RuntimeError is raised.

* Bug #1813214 was marked fixed in 0.7.13.  There were still a couple of
copy.com references remaining in the docs and web.  Got those nuked,
finally. [kenneth@loafman.com]

* Added s3 kms server side encryption support with kms-grants support. [vam]

* Putting option in man in alphabetical order + description improvement. [Marcin Okraszewski]

* Adds setting to specify Azure Blob standard storage tier. [Marcin Okraszewski]

* Fixed bug #1803896 with patch from slawekbunka   - Add \_\_enter\_\_
and \_\_exit\_\_ to B2ProgressListener. [Kenneth Loafman]

* Fix some punctuation. [kenneth@loafman.com]

* Fixed bug #1798206 and bug #1798504   * Made paramiko a global with
import during \_\_init\_\_ so it would     not be loaded unless
needed. [kenneth@loafman.com]

* Change WebDAV backend to not read/write files into memory, but stream
them from/to disk to/from the remote endpoint. [Maurus Cuelenaere]

* Tox: Target py3, rather than py36. [Mike Gorse]

    This should make tox accept versions of python 3 other than 3.6 (ie, 3.7).

* \_librsyncmodule.c: Use s in format parameters again under python 2. [Mike Gorse]

* Fix comment from last commit. [Mike Gorse]

* Compilec.py: work around conflict with collections.py vs. built-in
collections module. [Mike Gorse]

* First pass at a python 3 port. [Mike Gorse]

    Futurized, adjusted some string adornments, added py36 to tox, etc.

* Tox: pass LC\_CTYPE. [Mike Gorse]

    Without this, LC_CTYPE is unset in the test environment. If it is unset and
    LANG is also unset, then sys.getfilesystemencoding() will return "ascii" or
    something similar.

* Fixed but #1797797 with patch from Bas Hulsken   - use bytes instead
of unicode for '/' in filenames. [Kenneth Loafman]

* Run futurize --stage1 on rdiffdir. [Mike Gorse]

* Run futurize --stage1 on bin/duplicity. [Mike Gorse]

* Run futurize --stage1, and adjust so that tests still pass. [Mike Gorse]

* Adorn some remaining strings. [Mike Gorse]

* Fix error message on unmatched glob rules. [Quentin Santos]

* Fix required Python version in README. [Quentin Santos]

* Fixed bug #1795227 global name Dropbox is not defined   - Applied
patch from Pedro Gimeno to restore globals. [kenneth@loafman.com]

* Annotate more strings in duplicity/*.py. [Mike Gorse]

* Adorn strings in some duplicity/*.py files. Several files are still
tbd. [Mike Gorse]

* Unicode fixes. [Mike Gorse]

    All tests pass now

* Make files executable. [kenneth@loafman.com]

* Mark adorned all but one of testing/unit. [kenneth@loafman.com]

* Released some things without proper paperwork: * Adorned strings in
testing/, testing/functional/, and testing/unit * Added AUTHORS file
listing all copyright claimants in headers. [kenneth@loafman.com]

* Missed a couple.  Simple sort. [kenneth@loafman.com]

* Add AUTHORS file. [kenneth@loafman.com]

* Checkpoint: Fixing unadorned strings for testing/unit/*. [Kenneth Loafman]

* Fixed unadorned strings for testing/functional/*. [Kenneth Loafman]

* Fixed unadorned strings for testing/*. [Kenneth Loafman]

* Reverted back to rev 1317 and reimplemented revs 1319 to 1322. [kenneth@loafman.com]

* Reverted back to rev 1317 and reimplemented revs 1319 to 1322. [kenneth@loafman.com]

* Whoops, my bad!  Released before fully testing.  Reverting to rev 1317
and proceeding from there with unadorned string conversion. [kenneth@loafman.com]

* Move docs/conf.py to ignored.  Sphinx rewrites it. [kenneth@loafman.com]

* Fix a misspelling. [kenneth@loafman.com]

* Fix 2to3 error found with newer 2to3 module. [kenneth@loafman.com]

* Nuke remnants of copycom and acdcli backends * Regen docs. [kenneth@loafman.com]

* Fixed unadorned strings to unicode in duplicity/*/*   - Some fixup due
to shifting indenataion not matching PEP8.   - Substituted for non-
ascii char in jottlibbackend.py comment. [kenneth@loafman.com]

* Fixed unadorned strings to unicode in duplicity/backends/*   - Some
fixup due to shifting indenataion not matching PEP8. [kenneth@loafman.com]

* Fixed unadorned strings to unicode in duplicity/backends/*   - Some
fixup due to shifting indenataion not matching PEP8. [kenneth@loafman.com]

* Added function to fix unadorned strings
(testing/fix\_unadorned\_strings.py)   - Fixes by inserting 'u' before
token string   - Solves 99.9% of the use cases we have   - Fix
unadorned strings to unicode in bin/duplicity and bin/rdiffdir   - Add
import for \_\_future\_\_.print\_function to
find\_unadorned\_strings.py. [kenneth@loafman.com]

* Fix unadorned strings to unicode. [kenneth@loafman.com]

* Add gpg sockets to ignore list. [kenneth@loafman.com]

* Add fix\_unadorned\_strings.py to ignore list. [kenneth@loafman.com]

* Add function to fix unadorned strings by inserting 'u' before.
Solves 99.9% of the use cases we have. [kenneth@loafman.com]

* Add import for \_\_future\_\_.print\_function. [kenneth@loafman.com]

* Adorn globs in functional/test\_selection.py and
unit/test\_selection.py * Remove ignores for these files in
test\_code.py. [Aaron A Whitehouse]

* Remove selection.py exception from test\_code.py. [Aaron A Whitehouse]

* Adorn globs in selection.py. [Aaron A Whitehouse]

* Fixed bug #1780617 Test fail when GnuPG >= 2.2.8   - Relevant change
in GnuPG 2.2.8: https://dev.gnupg.org/T3981   - Added '--ignore-mdc-
error' to all gpg calls made. [kenneth@loafman.com]

* Add support for S3 One Zone - Infrequent Access storage class. [Excitable Snowball]

* Adorn strings in testing/unit/test\_globmatch.py. [Aaron A Whitehouse]

* Adorn string literals in duplicity/globmatch.py. [Aaron A Whitehouse]

* Added new script to find unadorned strings
(testing/find\_unadorned\_strings.py python\_file) which prints all
unadorned strings in a .py file. * Added a new test to test\_code.py
that checks across all files for unadorned strings and gives an error
if any are found (most files are in an ignore list at this stage, but
this will allow us to incrementally remove the exceptions as we adorn
the strings in each file). [Aaron A Whitehouse]

* Adorn string literals in test\_code.py with u/b * Add test for
unadorned string literals (currently only single file) [Aaron A Whitehouse]

* Tox changes to accommodate new pycodestyle version warnings. Ignored
W504 for now and marked as a TODO. Marked W503 as a permanent ignore,
as it is prefered to the (mutually exclusive) W504 under PEP8. *
Marked various regex strings as raw strings to avoid the new W605
"invalid escape sequence". [Aaron A Whitehouse]

* Fixed bug #x1717935 with suggestion from strainu   - Use
urllib.quote\_plus() to properly quote pathnames passed via URL. [kenneth@loafman.com]

* Fixed bug #1768954 with patch from Max Hallden   - Add
AZURE\_ENDPOINT\_SUFFIX environ variable to allow setting to non-U.S.
servers. [kenneth@loafman.com]

* Only check decryptable remote manifests   - fixup of revision 1252
which introduces a non-fatal error message (see #1729796)   - for
backups the GPG private key and/or it's password are typically not
available   - also avoid interactive password queries through e.g. gpg
agent. [Martin Nowak]

* Check last manifest only with prev. backup. [Martin Nowak]

* Mass update of po files from launchpad translations. [kenneth@loafman.com]

* Avoid redundant replication of already present backup sets - Add back
BackupSet.\_\_eq\_\_ which was accidentally removed in 1251. [Martin Nowak]

* Reduce dependencies on backend libraries   - Moved backend imports
into backend class \_\_init\_\_ method   - Surrounded imports with
try/except to allow better errors   - Put all library dependencies in
requirements.txt. [kenneth@loafman.com]

* Make backend.tobytes use util.fsencode rather than reimplementing. [Aaron A Whitehouse]

* Fixes so pylint 1.8.1 does not complain about missing conditional
imports.   - Fix dpbxbackend so that imports require instantiation of
the class.   - Added pylint: disable=import-error to a couple of
conditional imports. [kenneth@loafman.com]

* Change util.fsdecode to use "replace" instead of "ignore" (matching
behaviour of util.ufn) * Replace all uses of ufn with fsdecode. [Aaron A Whitehouse]

* Update docs. [kenneth@loafman.com]

* More pytest changes   - Use requirements.txt for dependencies   - Run
unit tests first, then functional   - Some general cleanup. [kenneth@loafman.com]

* More pytest changes   - Use requirements.txt for dependencies   - Run
unit tests first, then functional   - Some general cleanup. [kenneth@loafman.com]

* Converted to use pytest instead of unittest (setup.py test is now
discouraged)   - We use @pytest.mark.nocapture to mark the tests (gpg)
that require     no capture of file streams (currently 10 tests).   -
The rest of the tests are run normally. [kenneth@loafman.com]

* Remove precise-lpbuild.  EOL as of April 28, 1917. [kenneth@loafman.com]

* Remove unused import. [kenneth@loafman.com]

* First cut converting to pytest.   - 'setup.py test' now uses pytest.
We still use tox for     correct virtualenv setup.  All seem to be
current best     practices since 'setup.py test' use is discouraged.
- Global --capture=no option to allow gpg tests to complete
successfully.  Future should only turn off capture to the     gpg
tests themselves.  Creates a still messy output. [kenneth@loafman.com]

* Replace util.ufn(path.name) with path.uc\_name throughout. [Aaron A Whitehouse]

* Various code tidy-ups pre submitting for merge. None should change
behaviour. [Aaron A Whitehouse]

* Change fsdecode to use globals.fsencoding * Add 'ANSI\_X3.4-1968' to
the list of fsencodings that globals.fsencode treats as probably UTF-8. [Aaron A Whitehouse]

* Specify debian dependency too. [Michael Terry]

* Specify future requirement. [Michael Terry]

* Fix PEP8 issues. [Kenneth Loafman]

* Dpbxbackend: fix small files upload (API change) [Eugene Crosser]

    Dropbox file upload API for small files (that do not requre chunking)
    changed as described here:

    https://github.com/dropbox/dropbox-sdk-python/releases/tag/v7.1.0

    Now a data blob needs to be passed to the API instead of a file object.

* Dpbxbackend: check for specific API error for missing folder. [crosser@average.org]

* The "new" Dropbox API for directory listing raises an exception when
the directory is empty (and duplicity directory will be empty on the
first run). We actually want and empty list of files if the list of
files is emtpy. So catch the ListFolderError and continue. [crosser@average.org]

* The "new" Dropbox OAuth API return objects rather than tuples. Adjust
auth flow to that. [Eugene Crosser]

* More fixes for Unicode handling   - Default to 'utf-8' if
sys.getfilesystemencoding() returns 'ascii' or None   - Fixed bug
#1386373 with suggestion from Eugene Morozov. [kenneth@loafman.com]

* Fixed bug #1733057 AttributeError: 'GPGError' object has no attribute
'decode'   - Replaced call to util.ufn() with call to util.uexc().
Stupid typo! [kenneth@loafman.com]

* Fix attribution for patch of 1448094 to Wolfgang Rohdewald. [kenneth@loafman.com]

* Remove non-UTF8 filename from testfiles.tar.gz. [Kenneth Loafman]

* Fixed bug #1730902 GPG Error Handling   - use util.ufn() not str() to
handle encoding. [kenneth@loafman.com]

* Fixed bug #1723890 with patch from Killian Lackhove   - Fixes error
handling in pydrivebackend.py. [kenneth@loafman.com]

* Fixed bug #1720159 - Cannot allocate memory with large manifest file
since 0.7.03   - filelist is not read if --file-changed option in
collection-status not present   - This will keep memory usage lower in
non collection-status operations. [kenneth@loafman.com]

* Fix PEP8 issues in b2backend.py. [kenneth@loafman.com]

* Fixed bug #1724144 "--gpg-options unused with some commands"   - Add
--gpg-options to get version run command. [kenneth@loafman.com]

* Fixed bug #1448094 with patch from Tomáš Zvala   - Don't log
incremental deletes for chains that have no incrementals. [kenneth@loafman.com]

* Fixed bug #1654756 with new b2backend.py module from Vincent Rouille
- Faster (big files are uploaded in chunks)   - Added upload progress
reporting support. [kenneth@loafman.com]

* Patched in lp:\~mterry/duplicity/rename-dep   - Make rename command a
dependency for LP build. [kenneth@loafman.com]

* Remove conditional pexpect in testing/functional/\_\_init\_\_.py --
while the commented-out text is the nicer approach in versions after
pexpect 4.0, we need to support earlier versions at this stage and a
single code path is simpler. [Aaron A Whitehouse]

* Fixed bug #1714663 "Volume signed by XXXXXXXXXXXXXXXX, not XXXXXXXX"
- Normalized comparison length to min length of compared keys before
comparison   - Avoids comparing mix of short, long, or fingerprint
size keys. [kenneth@loafman.com]

* Fix PEP8 issues. [kenneth@loafman.com]

* Fixed bug #1715650 with patch from Mattheww S   - Fix to make
duplicity attempt a get first, then create, a container     in order
to support container ACLs. [Kenneth Loafman]

* More fixes to backend.py plus some cleanup. [Kenneth Loafman]

* Fix backend.py to allow string, list, and tuple types to support
megabackend.py. [Kenneth Loafman]

* Fix some unicode decode errors around exceptions. [Michael Terry]

* Fixed bug introduced in new megabackend.py where
process\_commandline()   takes a string not a list.  Now it takes
both. * Updated web page for new megabackend requirements. [Kenneth Loafman]

* Fixed bug #1638033 Remove leading slash on --file-to-restore   - code
already used rstrip('/') so change to just strip('/') [Kenneth Loafman]

* 2017-08-31  Kenneth Loafman  <kenneth@loafman.com> [Kenneth Loafman]

    Fixed bug #1538333 Assertion error in manifest.py: assert filecount == ...
          - Made sure to never pass .part files as true manifest files
          - Changed assert to log.Error to warn about truncated/corrupt filelist
          - Added unit test to make sure detection works
          - Note: while this condition is serious, it will not affect the basic backup and restore
            functions.  Interactive options like --list-files-changed and --file-changed will not
            work correctly for this backup set, so it is advised to run a full backup as soon as
            possible after this error occurs.
        * Fixed bug #1638033 Remove leading slash on --file-to-restore
          - code already used rstrip('/') so change to just strip('/')

* Fixed bug #1394386 with new module megabackend.py from Tomas Vondra
- uses megatools from https://megatools.megous.com/ instead of mega.py
library     which has been deprecated   - fixed copyright and PEP8
issues   - replaced subprocess.call() with self.subprocess\_popen() to
standardize. [Kenneth Loafman]

* Fixed bug #1394386 with new module megabackend.py from Tomas Vondra
- uses megatools from https://megatools.megous.com/ instead of mega.py
library     which has been deprecated   - fixed copyright and PEP8
issues. [Kenneth Loafman]

* Support gpg versions with -tag suffixes. [Michael Terry]

* Fix errors where log.Warn was invoked with log.warn in
webdavbackend.py. [ken]

* Gio: be slightly more correct and get child GFiles based on display
name. [Michael Terry]

* Fixed PEP8 errors in bin/duplicity. [Kenneth Loafman]

* Fixed bug #1709047 with suggestion from Gary Hasson   * fixed so
default was to use original filename. [Kenneth Loafman]

* Giobackend: handle a wider variety of gio backends by making less
assumptions; in particular, this fixes the google-drive: backend. [Michael Terry]

* Fixed encrypted remote manifest handling to merely put out a non-fatal
error message and continue if the private key is not available. [Kenneth Loafman]

* Fixed slowness in 'collection-status' by basing the status on the
remote system only.  The local cache is treated as empty. [Kenneth Loafman]

* Fix text of last change. [Kenneth Loafman]

* Collection-status should not sync metadata - up-to-date local metadata
is not needed as collection-status is generated from remote file list
- syncing metadata might require to download several GBs. [Martin Nowak]

* Fixed problem in dist/makedist when building on Mac where AppleDouble
files were being created in the tarball.  See:
https://superuser.com/questions/61185/why-do-i-get-files-like-foo-in-
my-tarball-on-os-x. [Kenneth Loafman]

* Merged in lp:\~xlucas/duplicity/swift-multibackend-bug   - Fix a bug
when swift backend is used in a multibackend configuration. [Kenneth Loafman]

* Copy.com is gone so remove copycombackend.py. [Kenneth Loafman]

* Fixed bug #1265765 with patches from Matthias Larisch and Edgar Soldin
- SSH Paramiko backend now uses BufferedFile implementation to enable
collecting the entire list of files on the backend. [Kenneth Loafman]

* Fix bug #1672540 with patch from Benoit Nadeau   - Rename would fail
to move par files when moving across filesystems.   - Patch uses
shutil.move() to do the rename instead. [Kenneth Loafman]

* Some changes ported 0.7 to/from 0.8 to keep up-to-date. [Kenneth Loafman]

* Revisited bug #670891 with patch from Edgar Soldin   - Forced
librsync.PatchedFile() to extract file object from TemporaryFile()
object when on Windows or Cygwin systems.  This allows us to avoid the
problem of tmpfile() use which creates temp files in the wrong place.
- See discussion at https://bugs.launchpad.net/duplicity/+bug/670891. [Kenneth Loafman]

* May have finally fixed bug #1556553, "Too many open files...".   -
Applied patch from Howard Kaye, question #631423.  The fix is to dup
the file descriptor, and then close the file in the deallocator
routine in the glue code. Duping the file lets the C code and the
Python     code each close the file when they are done with it.   -
Invalidated and removed the fix put in for bug #1320832.   - Caveat:
long incremental chains will still eat up a large number of file
descriptors.  It's a very risky practice, so I'm not inclined to fix
it. [Kenneth Loafman]

* Remove run-tests-ve - not needed * move stdin\_test.sh to manual dir. [Kenneth Loafman]

* Fix comments on ignored pylint messages. [Kenneth Loafman]

* Remove precise-lpbuild test since precise is EOL. [Kenneth Loafman]

* Adjust control for LP build process, fasteners not lockfile. [Kenneth Loafman]

* Fixed bug #1320641 and others regarding lockfile   - swap from
lockfile to fasteners module   - use an fcntl() style lock for process
lock of duplicity cache   - lockfile will now clear if duplicity is
killed or crashes. [Kenneth Loafman]

* Fixed bug #1689632 with patch from Howard Kaye   - On MacOS, the
tempfile.TemporaryFile call erroneously raises an     IOError
exception saying that too many files are open. This causes
restores to fail randomly, after thousands of files have been
restored. [Kenneth Loafman]

* Fixed bug #1320832 with suggestion from Oskar Wycislak   - Use chunks
instead of reading it all in swiftbackend. [Kenneth Loafman]

* Quick fix for bug #1680682 and gnupg v1, add missing comma. [ken]

* Fixed bug #1684312 with suggestion from Wade Rossman   - Use
shutil.copyfile instead of os.system('cp ...')   - Should reduce
overhead of os.system() memory usage. [Kenneth Loafman]

* Fixed bug #1680682 with patch supplied from Dave Allan   - Only
specify --pinentry-mode=loopback when --use-agent is not specified *
Fixed man page that had 'cancel' instead of 'loopback' for pinentry
mode. [Kenneth Loafman]

* Add some commented-out debug print and move under error condition. [Kenneth Loafman]

* Fixed bug #1668750 - Don't mask backend errors   - added exception
prints to module import errors. [Kenneth Loafman]

* Fixed bug #1671852 - Code regression caused by revision 1108   -
change util.uexc() back to bare uexc() [Kenneth Loafman]

* Fixed bug #1367675 - IMAP Backend does not work with Yahoo server   -
added the split() as needed in 'nums=list[0].strip().split(" ")'   -
the other fixes mentioned in the bug report comments were already done. [Kenneth Loafman]

* Some fixes to gpg.py to handle gpg1 & gpg2 & gpg2.1 commandline issues
- --gpg-agent is optional on gpg1, but on gpg2 it is used
automatically   - --pinentry-mode is not a valid opt until gpg2.1, so
condition on that. [Kenneth Loafman]

* Fixed the documentation of --use-agent in the man page. [Martin Wilck]

* Fixed bug #1657916 with patch supplied by Daniel Harvey   - B2
provider cannot handle two backups in the same bucket. [Kenneth Loafman]

* Add detail about import exceptions in onedrivebackend.py. [ken]

* Merged in lp:\~matthew-t-bentley/duplicity/duplicity   - Sets a user
agent. Backblaze asked for this in case there are errors that
originate     from the Duplicity B2 backend   - Only retrieves a new
upload URL when the current one expires, to bring it in line     with
their best practices for integrations:
https://www.backblaze.com/b2/docs/integration\_checklist.html. [Kenneth Loafman]

* Fixed bug #1658283 "Duplicity 0.7.11 broken with GnuPG 2.0"   - Made
gpg version check more robust than just major version   - Now use
--pinentry-mode=loopback on gpg 2.1 and greater   - Removed check for
non-Linux systems, a false problem. [Kenneth Loafman]

* Fixed bug #1655268 "--gpg-binary option not working"   - If gpg binary
is specified rebuild gpg profile using new binary location. [Kenneth Loafman]

* Fixed bug #1654220 with patch supplied by Kenneth Newwood   -
Duplicity fails on MacOS because GPG version parsing fails. [Kenneth Loafman]

* Fixed bug #1623342 with patch supplied by Daniel Jakots   - Failing
test on OpenBSD because tar/gtar not found. [Kenneth Loafman]

* Merged in lp:\~breunigs/duplicity/amazondrive3   - As reported on the
mailinglist, if a space is entered while duplicity asks for the URL,
it fails.     Since all important spaces are URL encoded anyway, this
should be fine even if there are spaces in     the URL at all. I also
patched it in the onedrive backend, because it must have similar
issues. [Kenneth Loafman]

* Fix Bug #1642813 with patch from Ravi   - If stat() returns None,
don't attempt to set perms. [Kenneth Loafman]

* Fix problem with gpg2 in yakety and zesty. [ken]

* Some fixes for MAC where gpg2 does not implement --pinentry-mode. [Kenneth Loafman]

* Skip locked folders tests if not on Linux platform. [Kenneth Loafman]

* Added tests to ensure behaviour is as expected for expressions
containing globs, as these traverse a different code path. [Aaron A Whitehouse]

* Fixed Bug #1624725, so that an include glob ending in "/" now includes
folder contents (for globs with and without special characters) [Aaron A Whitehouse]

* Added inline comment to globmatch.py explaining glob matching. *
Removed trailing / from Path() unittests, as paths used in duplicity
do not normally have these, even if they are folders. * Added unit
test to show files within a matched folder are included without a
trailing slash. * Fixed return value of
test\_slash\_star\_scans\_folder unittest from include to scan. [Aaron A Whitehouse]

* Add unittests and code comments to explain glob processing/regex
behaviour. [Aaron A Whitehouse]

* Add more tests for trailing slash behaviour. [Aaron A Whitehouse]

* Added (failing) test to show behaviour in Bug #1624725. [Aaron A Whitehouse]

* Temp fix for tempfile.TemporaryFile failures. [Kenneth Loafman]

* Fix encryption tests by specifying long key instead of short. [Kenneth Loafman]

* Merged in lp:\~horgh/duplicity/copy-symlink-targets-721599   - Add
--copy-links to copy symlink contents, not just the link itself. [Kenneth Loafman]

* Fix html output via rman. [ed.so]

* Merged in lp:\~dernils/duplicity/robust-dropbox-backend   - Added new
command line option --backend-retry-delay     that allows to determine
the time that duplicity sleeps     before retrying after an error has
occured.   - Added some robustness to dpbxbackend.py that ensures re-
authentication     happens in case that a socket is changed (e.g. due
to a forced reconnect     of a dynamic internet connection). [Kenneth Loafman]

* Revert to rev 1246. [Kenneth Loafman]

* Minor fix in manpage. [DerNils]

* Added --backend-retry-delay to the manpage. [DerNils]

* Added new command line option --backend-retry-delay. [DerNils]

* Added some robustness to dpbxbackend.py. [DerNils]

* Revert to rev 1246. [Kenneth Loafman]

* Merged in lp:\~dernils/duplicity/robust-dropbox-backend   - Added new
command line option --backend-retry-delay     that allows to determine
the time that duplicity sleeps     before retrying after an error has
occured.   - Added some robustness to dpbxbackend.py that ensures re-
authentication     happens in case that a socket is changed (e.g. due
to a forced reconnect     of a dynamic internet connection). [Kenneth Loafman]

* Merged in lp:\~dernils/duplicity/robust-dropbox-backend   - Added new
command line option --backend-retry-delay     that allows to determine
the time that duplicity sleeps     before retrying after an error has
occured.   - Added some robustness to dpbxbackend.py that ensures re-
authentication     happens in case that a socket is changed (e.g. due
to a forced reconnect     of a dynamic internet connection). [Kenneth Loafman]

* Fix bug using 40-char sign keys, from Richard McGraw on mail list   -
Remove truncation of argument and adjust comments. [Kenneth Loafman]

* Fixed bug #1642098 - does not create PAR2 archives when '--
par2-options' is used   - Missing space between par2-options plus
default options. [ken]

* Fixed bug #1621194 with code from Tornhoof   - Do backup to google
drive working without a service account. [Kenneth Loafman]

* Merged in lp:\~mwilck/duplicity/duplicity   - GPG: enable truly non-
interactive operation with gpg2   - This patch fixes the IMO
unexpected behavior that, when using GnuPG2, a pass phrase dialog
always pops up for     saving backups. This is particularly annoying
when trying to do unattended / fully automatic backups. [ken]

* GPG: enable truly non-interactive operation with gpg2. [Martin Wilck]

    GPG always tries to grab a passphrase from the gpg agent, even
    if is run with "--batch --no-tty" (as enforced by the
    meta_interactive = 0 setting of gpginterface.py).

    Sometimes this behavior is not intended. I would like to be able
    to run a backup job truly interactively. This would be possible,
    but duplicity's check_manifests() function calls gpg to compare
    the remote (encrypted) and local manifest, which, with gpg2,
    will pop up the gpg agent pinentry every time I try to save backup
    (with gpg1, duplicity will just give up on the verification).

    I found that it's possible to force gpg2 to behave like gpg1 by
    using the command line option "--pinentry-mode=cancel". My patch
    applies this option if duplicity's "--use-agent" option is unset.

    Now, even with gpg2, backups can be saved without any passphrase
    dialog, at the cost of not being able to verify the manifests. Users
    who want the verification would just need to use "--use-agent", as
    with gpg1.

    For restore, this change has no effect, as duplicity will ask for the
    passphrase anyway if "--use-agent" is not specirfied.

* Fixed bug #1623342 with patch from Daniel Jakots   - failing test on
OpenBSD because tar/gtar not found. [Kenneth Loafman]

* Fixed bug #1620085: OSError when using --exclude-if-present with a
locked directory in backup path. * Added tests for errors on locked
files. [Aaron A Whitehouse]

* Add functional tests for --exclude-if-present. [Aaron A Whitehouse]

* Move and rename second TestTrailingSlash block to TestTrailingSlash2. [Aaron A Whitehouse]

* Merged in lp:\~mstoll-de/duplicity/duplicity   - Backblaze announced a
new domain for the b2 api. [Kenneth Loafman]

* Fixed bugs #815510 and #1615480   - Changed default --volsize to 200MB. [Kenneth Loafman]

* Merged in lp:\~fenisilius/duplicity/acd\_init\_mkdir   - Allow
duplicity to create remote folder. [Kenneth Loafman]

* Whoops, committed too much! [Kenneth Loafman]

* Fixed conflict in merge from Martin Wilck and applied   -
https://code.launchpad.net/\~mwilck/duplicity/0.7-series/+merge/301492
- merge fixes setsid usage in functional testing. [ken]

* Remove -w from setsid in functional tests. [ken]

* Fix unit test failures for {Old,Short}FilenamesFinalTest. [Martin Wilck]

    These unit test fail because of the following tricky series of events:

    1. duplicity is started with setsid(1). The setsid process forks duplicity
       and terminates
    2. duplicity prints a warning about depracated option (--old-filenames,
       --short-filenames) before asking for the passphrase. This causes pexpect
       to call os.waitpid(self.pid) but self.pid is the PID of the setsid(1)
       process which has already terminated.
    3. pexpect quits the expect loop for the passphrase with EOF.

    The problem can be solved by using the -w flag for sedsid (wait for child),
    so that the setsid process won't exit before duplicity itself.

* Fix failures of unit tests with --hidden-encrypt-key. [Martin Wilck]

    On distributions that don't have genuine gpg 1.x any more (gpg is a symlink
    to gpg2), such as OpenSUSE Factory, the tests with --hidden-encrypt-key fail
    without the gpg option --try-all-secrets.

    Not even that will help for gpg2 2.1.13 which has a bug preventing
    --try-all-secrets from working correctly
    (https://bugs.gnupg.org/gnupg/issue1985).

* Selection.py: use closure for matching paths with glob expressions. [Martin Wilck]

    (merged from lp:~mwilck/duplicity/duplicity)

    Glob matching in current duplicity uses a selector function that calls path_matches_glob(). This means that whenever a filename is matched, path_matches_glob() goes through the process of transforming a glob expression into regular expressions for filename and directory matching.

    My proposed patches create a closure function instead that uses precalculated regular expressions; the regular expressions are thus constructed only once at initialization time.

    This change speeds up duplicity a *lot* when complex include/exclude lists are in use: for my use case (dry-run, backup of an SSD filesystem), the speedup is a factor of 25 (runtime: 4s rather than 90s).

* Fixed PEP8 and 2to3 issues. [Kenneth Loafman]

* Add support for OVH Public Cloud Archive backend. [Xavier Lucas]

* Support prefix affinity in multibackend. [Xavier Lucas]

* Add integration test for newly added replicate command. [Martin Nowak]

    - also see https://code.launchpad.net/~dawgfoto/duplicity/replicate/+merge/322836

* Fixed problem in dist/makedist when building on Mac where AppleDouble
files were being created in the tarball.  See:
https://superuser.com/questions/61185/why-do-i-get-files-like-foo-in-
my-tarball-on-os-x. [Kenneth Loafman]

* Remove util.bytes\_to\_uc (as either .decode or fsdecode is
preferable). * Move unicode conversion for select options from
selection.py to commandline.py. [Aaron A Whitehouse]

* Replace util.py functions to and from unicode with direct calls to
.encode and .decode, as it did not save much code, means the
"strict"/"ignore"/"replace" decision can be made per call. Also helps
narrow down on why sys.getfilesystemencoding() is not working as
expected in some places. [Aaron A Whitehouse]

* Merge remaining file from trunk. Tests pass. [Aaron A Whitehouse]

* Merged in lp:\~xlucas/duplicity/swift-multibackend-bug   - Fix a bug
when swift backend is used in a multibackend configuration. [Kenneth Loafman]

* Copy.com is gone so remove copycombackend.py. [Kenneth Loafman]

* Fixed bug #1265765 with patches from Matthias Larisch and Edgar Soldin
- SSH Paramiko backend now uses BufferedFile implementation to enable
collecting the entire list of files on the backend. [Kenneth Loafman]

* Added capability to mount user workspace for testing local code. [Kenneth Loafman]

* Added variable substitution to docker-compose.yml   - .env file
contains first 24 bits of subnet addr * Added teardown.sh as
completion of setup.sh. [Kenneth Loafman]

* Fix bin/duplicity.1 entries for --verify and --compare-data. [Aaron A Whitehouse]

* Test infrastructure now using docker-compose. [DerNils]

* Fix bug #1672540 with patch from Benoit Nadeau   - Rename would fail
to move par files when moving across filesystems.   - Patch uses
shutil.move() to do the rename instead. [Kenneth Loafman]

* Some changes ported 0.7 to/from 0.8 to keep up-to-date. [Kenneth Loafman]

* Revisited bug #670891 with patch from Edgar Soldin   - Forced
librsync.PatchedFile() to extract file object from TemporaryFile()
object when on Windows or Cygwin systems.  This allows us to avoid the
problem of tmpfile() use which creates temp files in the wrong place.
- See discussion at https://bugs.launchpad.net/duplicity/+bug/670891. [Kenneth Loafman]

* Fix spurious warning message, return value not needed. [Kenneth Loafman]

* Checkpoint - docker testbed mostly running   - lots of format changes
in setup.sh   - made sure to kill off network and restart   -
simplified container naming and killall process   - most tests run now
with tox, 5 fail. [Kenneth Loafman]

* Go back to original requirements file. [Kenneth Loafman]

* May have finally fixed bug #1556553, "Too many open files...".   -
Applied patch from Howard Kaye, question #631423.  The fix is to dup
the file descriptor, and then close the file in the deallocator
routine in the glue code. Duping the file lets the C code and the
Python     code each close the file when they are done with it.   -
Invalidated and removed the fix put in for bug #1320832.   - Caveat:
long incremental chains will still eat up a large number of file
descriptors.  It's a very risky practice, so I'm not inclined to fix
it. [Kenneth Loafman]

* Fix spelling and rearrange some. [Kenneth Loafman]

* Added lpbuild-trusty to replace lpbuild-precise pre Aaron Whitehouse's
comment that there was a bug in pexpect < 3.4 that affects us. [Kenneth Loafman]

* Minor changes to setup.sh. [DerNils]

* Minor fix to setup.sh. [DerNils]

* Added more test infrastructure. [DerNils]

* Support for Swift storage policies. [Xavier Lucas]

* Changes needed to run-tests without pylint E0401(import-error) errors. [Aaron A Whitehouse]

* Move stdin\_test.sh to manual dir. [Kenneth Loafman]

* Precise is EOL so drop testing for it. [Kenneth Loafman]

* Adjust control for LP build process, fasteners not lockfile. [Kenneth Loafman]

* Fixed bug #1320641 and others regarding lockfile   - swap from
lockfile to fasteners module   - use an fcntl() style lock for process
lock of duplicity cache   - lockfile will now clear if duplicity is
killed or crashes. [Kenneth Loafman]

* Fixed bug #1689632 with patch from Howard Kaye   - On MacOS, the
tempfile.TemporaryFile call erroneously raises an     IOError
exception saying that too many files are open. This causes
restores to fail randomly, after thousands of files have been
restored. [Kenneth Loafman]

* Moved some things around in testing/infrastructure to clean up. [Kenneth Loafman]

* Moved Dockerfile for duplicitytest into
testinfrastructure/duplicity\_test. [Kenneth Loafman]

* Added furhter files for test infrastructure. [DerNils]

* Fixed bug #1320832 with suggestion from Oskar Wycislak   - Use chunks
instead of reading it all in swiftbackend. [Kenneth Loafman]

* Added ftp client to Dockerfile. [DerNils]

* Updated Dockerfile. [DerNils]

* Remove unnecessary unicode conversion on commandline.py filelist
append. * Tests all pass (and in previous commit). [Aaron A Whitehouse]

* Use unicode version of pexpect.spawn for version >= 4.0, but bytes
version below this. [Aaron A Whitehouse]

* Bzr does not honor perms so fix the perms at the start of the testing
and   avoid annoying error regarding testing/gnupg having too lenient
perms. [Kenneth Loafman]

* Replace incoming non-ASCII chars in commandline.py. [Kenneth Loafman]

* Merged in lp:\~marix/duplicity/add-azure-arguments   - Using the Azure
backend to store large amounts of data we found that     performance
is sub-optimal. The changes on this branch add command line
parameters to fine-tune some parameters of the Azure storage library,
allowing to push write performance towards Azure above 1 Gb/s for
large     back-ups. If a user does not provide the parameters the
defaults of the     Azure storage library will continue to be used. [Kenneth Loafman]

* Add command line arguments to fine-tune the Azure backend. [Bjoern Meier]

    Using the default values for internal block sizes and connection
    numbers works well for small back-ups, but provides suboptimal
    performance for larger ones.

* Delete tempfiles as soon as possible. [Martin Nowak]

* Add replicate command - useful to replicate/archive backups to another
backend - allows to partially replicate only older backup sets -
checks existing backup sets on target to avoid redundant copies. [Martin Nowak]

* We need tzdata (timezone data). [ken]

* You need tox to run tox.  Doh! [ken]

* Add libffi-dev back.  My bad. [ken]

* Fixed tox.ini. [DerNils]

* Separated pip requirements into duplicity and testing. [DerNils]

* Separated pip requirements into duplicity and testing. [DerNils]

* Remove dependencies we did not need. [ken]

* Add test user and swap to non-priviledged. [ken]

* Move branch duplicity up the food chain. [ken]

* Simplify Dockerfile per https://docs.docker.com/engine/userguide/eng-
image/dockerfile\_best-practices/ - Add a .dockerignore file -
Uncomment some debug prints - quick fix for bug #1680682 and gnupg v1,
add missing comma. [ken]

* Quick fix for bug #1680682 and gnupg v1, add missing comma. [ken]

* A little reorg, just keeping pip things together. [ken]

* More changes for testing: - keep gpg1 version for future testing -
some changes for debugging functional tests - add gpg-agent.conf with
allow-loopback-pinentry. [Kenneth Loafman]

* Edited Dockerfile. [DerNils]

* Whoops, deleted too much.  Add rdiff again. [Kenneth Loafman]

* Move pep8 and pylint to requirements. [Kenneth Loafman]

* Add rdiff install and newline at end of file. [ken]

* Edited requirements.txt, minor changes to README-REPO and README-
TESTING. [DerNils]

* Added README-TESTING, removed hmtlcov folder. [DerNils]

* Edited requirements.txt. [DerNils]

* Cleaned test cases. [DerNils]

* Added Dockerfile. [DerNils]

* Updated requirements.txt. [DerNils]

* Updated requirements.txt. [DerNils]

* Updated requirements.txt. [DerNils]

* Working on dpbx backend tests§ [DerNils]

* Working on the READMEs. [DerNils]

* Worked on the requirements and README. [DerNils]

* Added some experiences to the README. [DerNils]

* Make all tests pass on py27 tox environment. * lpbuildd-precise tests
still fail because the outdated pexpect (2.4) has issues with unicode
(pexpect.spawn does not support unicode and spawnu.readline fails). [Aaron A Whitehouse]

* Unit/test\_globmatch.py, unit/test\_selection.py,
functional/test\_selection.py tests all pass. * Assume UTF-8 encoding
for filelists (which also allows ASCII encoding). * Use new io module
for selection filelist access. * Create new path.uc\_name that is a
unicode version of the path, which is then used throughout the
selection code for path name matching etc. * Move selection.py to
using unicode strings and uc\_name versions of paths. * Made
functional/\_\_init\_\_.py use unicode arguments to run duplicity for
tests. * Use new io module in functional/test\_selection.py. * Remove
@unittest.expectedFailure from test\_unicode\_paths\_square\_brackets,
which no longer fails. * Make unit/test\_selection.py ParseTest
support unicode and add test\_unicode\_paths\_non\_globbing unit test
version of functional test. [Aaron A Whitehouse]

* Make test\_selection.py use unicode string literals and still pass. *
funtional/test\_selection.py still fails. [Aaron A Whitehouse]

* Make path.py only accept unicode. * Make all string literals in
test\_selection.py unicode. * Create path.uc\_name as an alternative
to path.name, allowing existing  code to continue using bytes during
transition. * Make file writes in test\_selection.py use io.open. *
Tests do not yet pass. [Aaron A Whitehouse]

* Make globmatch.py deal with either unicode or string globs. * Make
path.uc\_name for unicode name of path (vs path.name for bytes). *
Functional select test failures. [Aaron A Whitehouse]

* Test\_globmatch.py now passing with unicode globs/paths *
test\_square\_bracket\_options\_unicode now passing. [Aaron A Whitehouse]

* Glob\_to\_regex converted to unicode, globmatch.py not yet passing
tests. [Aaron A Whitehouse]

* Fixed bug #1668750 - Don't mask backend errors   - added exception
prints to module import errors. [Kenneth Loafman]

* Added future imports to globmatch.py and added future to tox.ini deps. [Aaron A Whitehouse]

* Added (failing) unicode test. [Aaron A Whitehouse]

* Add tests for square brackets. [Aaron A Whitehouse]

* Add test for unicode paths with asterisks in globs. [Aaron A Whitehouse]

* Added files with unicode names to testfiles and added
TestUnicode.test\_unicode\_paths\_non\_globbing, which tests --include
and --exclude works as expected with these files. [Aaron A Whitehouse]

* Fixed bug #1671852 - Code regression caused by revision 1108   -
change util.uexc() back to bare uexc() [Kenneth Loafman]

* Skip pylint on dpbxbackend.py for now. [Kenneth Loafman]

* Refresh docs. [Kenneth Loafman]

* Fixed PEP8 errors: E402 module level import not at top of file. [Aaron A Whitehouse]

* Uses the globals.archive\_dir variable to store only a string in the
case of a path, uses globals.archive\_dir\_path. [benoit@benoit-desktop]

* Fixed bug #1367675 - IMAP Backend does not work with Yahoo server   -
added the split() as needed in 'nums=list[0].strip().split(" ")'   -
the other fixes mentioned in the bug report comments were already done. [Kenneth Loafman]

* Fixed variable name change in last merge which broke a bunch of tests
- Changed archive\_dir\_root back to archive\_dir. [Kenneth Loafman]

* Change the global name archive\_dir to archive\_dir\_root       add
the arglist to the optparser. [benoit@benoit-desktop]

* Fix E305 PEP8 errors: expected 2 blank lines after class or function
definition, found 1 * Remove E305 from pycodestyle ignores. [Aaron A Whitehouse]

* Fix PEP-8 testing by moving to using pycodestyle library. *
Temporarily add ignores to allow these tests to pass. [Aaron A Whitehouse]

* Fix minor pep8 issue - line too long. [Kenneth Loafman]

* Add support for Shared Access Signatures to the Azure backend. [Matthias Bach]

    Authenticating to the Azure storage via the account is suboptimal as it
    grants the process full administrative permissions on the storage
    account. Usage of a shared access signature allows to pass only the
    minimal permissions on a single container to Duplicity. This makes it
    much more sutable for automated usage, e.g. in cron jobs.

* Fix backup creation using azure-storage > 0.30.0. [Matthias Bach]

    The previous fix only fixed restore and verification of backups.

* Make the Azure backend compatible with azure-storage 0.30.0 and up. [Matthias Bach]

* Update setup.py to show only Python 2.7 support. [Aaron A Whitehouse]

* Fixed bug #1603704 with patch supplied by Maciej Bliziński   - Crash
with UnicodeEncodeError. [Kenneth Loafman]

* Fixed bug #1657916 with patch supplied by Daniel Harvey   - B2
provider cannot handle two backups in the same bucket. [Kenneth Loafman]

* Rename path\_matches\_glob\_fn to select\_fn\_from\_glob, as this more
accurately reflects the return value. * Significantly refactored
unit/test\_globmatch.py to make this cleaner and clearer. [Aaron A Whitehouse]

* Add detail about import exceptions in onedrivebackend.py. [ken]

* Remove time from run-tests, in case this causes any issues (e.g. cross
platform support). [Aaron A Whitehouse]

* Add more scan tests. [Aaron A Whitehouse]

* Removed unused non-globbing code (\_glob\_get\_filename\_sf and
\_glob\_get\_tuple\_sf). * Made run-tests time test runs. * Removed
run-tests-ve, which was identical to run-tests. [Aaron A Whitehouse]

* Move to using single (globing, glob\_get\_normal\_sf) function for
glob strings with and without globbing characters. No performance
impact. [Aaron A Whitehouse]

* Make globs of "/" work with globbing code. * Make globs of "/" match
everything. [Aaron A Whitehouse]

* Made \_glob\_get\_filename\_sf and \_glob\_get\_tuple\_sf internal
functions to ensure no unit tests depend on them directly. [Aaron A Whitehouse]

* Only get a new upload URL when needed.  Add a user agent. [Matthew Bentley]

* Fix pep8 issue. [Kenneth Loafman]

* Fixed bug #1655268 "--gpg-binary option not working"   - If gpg binary
is specified rebuild gpg profile using new binary location. [Kenneth Loafman]

* Futurize -stage1 all files, leaving the isinstance(s,
types.StringType) tests unchanged. * Reverted earlier changes to
types.StringType test in test files. * Created python 2/3 compatible
tests for int and long. [Aaron A Whitehouse]

* Futurize -stage1 on py files in testing for improved python 2/3
support. [Aaron A Whitehouse]

* Fix PEP error on adbackend.py. * Add jottalib as a tox dep to fix
pylint error. [Aaron A Whitehouse]

* Merge in TestExcludeIfPresent from 0.7-series, which tests the
behaviour of duplicity's --exclude-if-present option. [Aaron A Whitehouse]

* Move and rename TestTrailingSlash2 test. [Aaron A Whitehouse]

* Fixed bug #1654220 with patch supplied by Kenneth Newwood   -
Duplicity fails on MacOS because GPG version parsing fails. [Kenneth Loafman]

* Fixed bug #1623342 with patch supplied by Daniel Jakots   - Failing
test on OpenBSD because tar/gtar not found. [Kenneth Loafman]

* Merged in lp:\~breunigs/duplicity/amazondrive3   - As reported on the
mailinglist, if a space is entered while duplicity asks for the URL,
it fails.     Since all important spaces are URL encoded anyway, this
should be fine even if there are spaces in     the URL at all. I also
patched it in the onedrive backend, because it must have similar
issues. [Kenneth Loafman]

* Fix Bug #1642813 with patch from Ravi   - If stat() returns None,
don't attempt to set perms. [Kenneth Loafman]

* Whoops, make a couple of changes to match series-7. [Kenneth Loafman]

* Whoops, fix bad patch * Add gpg2 dir to .bzrignore. [Kenneth Loafman]

* Fix some issues with testing on MacOS * Fix problem with gpg2 in
yakety and zesty. [ken]

* Merged in lp:\~aaron-
whitehouse/duplicity/Bug\_1624725\_files\_within\_folder\_slash   -
Fixed Bug #1624725, so that an include glob ending in "/" now includes
folder contents (for globs with     and without special characters).
This preserves the behaviour that an expression ending in "/" only
matches a folder, but now the contents of any matching folder is
included. [Kenneth Loafman]

* Improve description of new argument in man page. [Will Storey]

* Add new argument to duplicity manpage. [Will Storey]

* Add flag to copy target of symlinks rather than the link. [root]

    This allows us to dereference and include what symlinks point to in our backup.
    I named the argument --copy-links. This is the name rsync gives to a similar
    flag. There is a bug requesting this feature on launchpad, 721599:
    https://bugs.launchpad.net/duplicity/+bug/721599

* Merged in lp:\~ed.so/duplicity/manpage.fixes   - Fix html output via
rman on the website. [Kenneth Loafman]

* Merged in lp:\~dernils/duplicity/robust-dropbox-backend   - Added new
command line option --backend-retry-delay     that allows to determine
the time that duplicity sleeps     before retrying after an error has
occured.   - Added some robustness to dpbxbackend.py that ensures re-
authentication     happens in case that a socket is changed (e.g. due
to a forced reconnect     of a dynamic internet connection). [Kenneth Loafman]

* Fix bug using 40-char sign keys, from Richard McGraw on mail list   -
Remove truncation of argument and adjust comments. [Kenneth Loafman]

* Fixed bug #1642098 - does not create PAR2 archives when '--
par2-options' is used   - Missing space between par2-options plus
default options. [ken]

* Fixed missing rename in Amazon Drive backend. [Stefan Breunig]

* Rename to just "AD" to avoid any possible trademark issues. [Stefan Breunig]

* Document peculiarities of AmazonDrive. [Stefan Breunig]

* Add and document native AmazonDrive backend. [Stefan Breunig]

* Remove uses\_netloc directive. [Håvard Gulldahl]

* JottaCloudBackend: Don't return bytestrings in \_list() [Håvard Gulldahl]

* Adding JottaCloud backend. [Håvard Gulldahl]

* Fixed bug #1621194 with code from Tornhoof   - Do backup to google
drive working without a service account. [Kenneth Loafman]

* Merged in lp:\~mwilck/duplicity/duplicity   - GPG: enable truly non-
interactive operation with gpg2   - This patch fixes the IMO
unexpected behavior that, when using GnuPG2, a pass phrase dialog
always pops up for     saving backups. This is particularly annoying
when trying to do unattended / fully automatic backups. [Kenneth Loafman]

* Fixed bug #1623342 with patch from Daniel Jakots   - failing test on
OpenBSD because tar/gtar not found. [Kenneth Loafman]

* Add requirements.txt - Remove module mocks in conf.py. [Kenneth Loafman]

* OK, finally grokked how to mock out \_librsync, but it did mean having
to change librsync.py with a conditional.  Would have preferred a
cleaner solution. - Fixed the remaining warnings in READTHEDOCS build,
including the removal of a couple of files that were extraneous. [Kenneth Loafman]

* Try autodoc\_mock\_imports... [ken]

* Try autodoc\_mock\_imports... [ken]

* Try autodoc\_mock\_imports... [ken]

* Try fully qualified module name, again. [ken]

* Remove fully qualified name. [ken]

* Resolve recursion in Mock. [ken]

* Try fully qualified and not qualified module names. [ken]

* Try without \_librsync. [ken]

* Try fully qualified module name. [ken]

* Try with virtualenv. [ken]

* Try again... [ken]

* Mock sucks, big time! [ken]

* Mock sucks, big time! [ken]

* Mock sucks! [ken]

* Try MagicMock. [ken]

* Try MagicMock. [ken]

* Fix build on RTD. [ken]

* Fix build on RTD. [ken]

* Fix build on RTD. [ken]

* Fix build on RTD. [ken]

* Fix build on RTD. [ken]

* Remove \_build dir from git. Fix some names, authors. [ken]

* Merged in lp:\~mstoll-de/duplicity/duplicity   - Backblaze announced a
new domain for the b2 api. [Kenneth Loafman]

* Fixed bugs #815510 and #1615480   - Changed default --volsize to 200MB. [Kenneth Loafman]

* First pass at some Sphinx docs for moving to readthedocs.org. [Kenneth Loafman]

* Merged in lp:\~fenisilius/duplicity/acd\_init\_mkdir   - Allow
duplicity to create remote folder. [Kenneth Loafman]

* Added documentation for connecting to IBM Bluemix ObjectStorage. [Arashad Ahamad]

* Added support to connect IBM Bluemix ObjectStorage. [Arashad Ahamad]

* Fixed bug #1612472 with patch from David Cuthbert   - Restore from S3
fails with --with-prefix-archive if prefix includes '/' [Kenneth Loafman]

* Restore testing/gnupg/gpg.conf and testing/gnupg/README. [Kenneth Loafman]

* Fixed conflict in merge from Martin Wilck and applied   -
https://code.launchpad.net/\~mwilck/duplicity/0.7-series/+merge/301492
- merge fixes setsid usage in functional testing. [ken]

* Selection.py: glob\_get\_normal\_sf: use closure
path\_matches\_glob\_fn. [Martin Wilck]

    Use the closure function for checking paths rather than path_matches_glob().

* Globmatch: path\_matches\_glob\_fn: return closure for path match. [Martin Wilck]

    path_matches_glob() re-calculates the regular expressions for
    path matching in every match operation. This is highly inefficient.
    Return a closure with pre-calculated REs instead which can be used
    for path matching later.

* Revert log.Error to log.Warn, as it was prior to the merge in rev
1224, as this was affecting other applications (deja dup). [Aaron A Whitehouse]

* Fixed bug #1600692 with patch from Wolfgang Rohdewald   - Allow
symlink to have optional trailing slash during verify. [ken]

* Fix date in CHANGELOG.  Release date was 2016-07-02, not 01. [ken]

* Fixed bug #1600692 with patch from Wolfgang Rohdewald   - Allow
symlink to have optional trailing slash during verify. [ken]

* Remove import of unittest2 for Python <2.7, now that Python 2.7 is the
minimum version. [Aaron A Whitehouse]

* Remove Python 2.6 settings from tox.ini. [Aaron A Whitehouse]

* Remove Python 2.6 support from the test suite and references to it
from README and README-REPO. [Aaron A Whitehouse]

* Merge 0.7-series changes to README-REPO. [Aaron A Whitehouse]

* Merge 0.7 series changes to README. [Aaron A Whitehouse]

* Merge 0.7 series changes to tox.ini. [Aaron A Whitehouse]

* Fix date in CHANGELOG.  Release date was 2016-07-02, not 01. [ken]

* Properly remove line too long errors (E501) from PEP8 ignores. [Aaron A Whitehouse]

* Fixed lines longer than 120 chars. [Aaron A Whitehouse]

* Set line length error length to 120 (matching tox.ini) and fixed PEP8
E501(line too long) errors. [Aaron A Whitehouse]

* Fix PEP8 W503, line break before binary operator. [Aaron A Whitehouse]

* Fixed bug #1594780 with patches from B. Reitsma   - Use re.finditer()
to speed processing. [Kenneth Loafman]

* Only give an error about not being able to access possibly locked file
if that file is supposed to be included or scanned (i.e. not
excluded). [Aaron A Whitehouse]

* Fixed README-REPO to no longer mention 0.6-series. [Kenneth Loafman]

* Fixed bug #822697 ssh-options not passed in rsync over ssh   - Added
globals.ssh\_options to rsync command line * Increased default volume
size to 200M, was 25M. [Kenneth Loafman]

* Fix PEP8 error in onedrivebackend.py (space before bracket). [Aaron A Whitehouse]

* Fix pep8 issues from last two patch sets. [ken]

* B2 reauth: use other log level. [Markus Stoll]

* Handle expired auth token. [Markus Stoll]

* Fixed bug #1589038 with patches from Malte Schröder   - Added
ignore\_case option to selection functions. [ken]

* Fixed bug #1586992 with patches from Dmitry Nezhevenko   - Patch adds
\_delete\_list to Par2Backend. And \_delete\_list fallbacks to
\_delete calls if wrapped backend has no \_delete\_list. [ken]

* Fixed bug #1586934 with patches from Dmitry Nezhevenko   - fixes error
handling in wrapper. [ken]

* Fixed bug #1573957 with patches from Dmitry Nezhevenko   - upload last
chunk with files\_upload\_session\_finish to avoid extra request   -
upload small files using non-chunked api. [ken]

* Adds prefix support to swift backend. [Ghozlane TOUMI]

    Right now duplicity's swift backend only accept a container as target (swift://container)
    trying to use a prefix / pseudo folder (swift://container/backup/path ) results in a JSON exception.

    This patch adds the abiliy to use path in the swift backend, in order to have multiple backups to the same container neatly organized.

    It borrows some code from the S3 backend, and is quite unobtrusive .

* Fix typo in error handling code. [Scott McKenzie]

* Add missing build-dep apparently now not installed by default with
python2 in xenial+ [Michael Terry]

* Fixed bug #1570293   - removed flush() after write.   - revert to
previous version. [ken]

* Fixed bug #1571134 and #1558155   - used patch from
https://bugs.debian.org/820725 but made changes     to allow the user
to continue using the old version. [ken]

* Remove unused (default) argument. [ken]

* Fixed bug #1569523   - bug introduced in improper fix of bug #1568677
- gotta love those inconsistent APIs. [ken]

* Blasted JIT imports got me again! [ken]

* Fixed bug #1568677   - bug introduced by incomplete fix of bug 1296793
- simplified setting of bucket locations. [ken]

* Fixed bug 1568677 with suggestions from Florian Kruse   - bug
introduced by incomplete fix of bug 1296793. [ken]

* Fix bug reported on the mailing list from Mark Grandi (assertion error
while backing up).  In file\_naming.parse() the filename was being
lower   cased prior to parsing.  If you had used a prefix with mixed
case, we   were writing the file properly, but could not find it in
the backend. [Kenneth Loafman]

* Re-added import of re, as re.compile still used in selection.py. [Aaron Whitehouse]

* Move complexity of matching paths to globs into globmatch.py
path\_matches\_glob, rather than in selection.py Select. [Aaron Whitehouse]

* Move ignorecase handling out of re.compile to use .lower() instead. [Aaron Whitehouse]

* Remove glob\_get\_prefix\_res from selection.py, now that it has moved
to globmatch.py. [Aaron Whitehouse]

* Move content of glob\_get\_prefix\_res to globmatch.py
glob\_get\_prefix\_regexs. [Aaron Whitehouse]

* Fixed globmatch tests. Tests pass. [Aaron Whitehouse]

* Move glob\_to\_re to globmatch.py. Moved associated tests into
test\_globmatch.py. [Aaron Whitehouse]

* Move the logic of the glob\_to\_re method into the glob\_to\_regex
function in globmatch.py. [Aaron Whitehouse]

* Improve man page entry for --exclude-if-present. [Aaron Whitehouse]

* Applied patch from Dmitry Nezhevenko to upgrade dropbox backend:   -
update to SDK v2   - use chunked upload. [Kenneth Loafman]

* Path may be unset. [ed.so]

* Duplicity.1, commandline.py, globals.py - added --ssl-cacert-path
parameter backend.py - make sure url path component is properly url
decoded,   in case it contains special chars (eg. @ or space)
lftpbackend.py - quote \_all\_ cmd line params - added missing
lftp+ftpes protocol - fix empty list result when chdir failed silently
- added ssl\_cacert\_path support webdavbackend.py - add ssl default
context support for python 2.7.9+   (using system certs eg. in
/etc/ssl/certs) - added ssl\_cacert\_path support for python 2.7.9+ -
gettext wrapped all log messages - minor refinements. [ed.so]

* Reverted changes made in rev 1164 w.r.t. getting the source from   VCS
rather than local directory.  Fixes bug #1548080. [Kenneth Loafman]

* Use built-in username/password support in backends.py. [Roman Yepishev]

    Backend is no longer reading environment variables.

    MEDIAFIRE_EMAIL ->
       mf://duplicity%40example.com@mediafire.com/some_path

    MEDIAFIRE_PASSWORD ->
       provided via command line via get_password() or
       FTP_PASSWORD env var or
       mf://duplicity%40example.com:some%20password@mediafire.com/some_path

* Remove custom logging, add usage info. [Roman Yepishev]

* Create folder recursively. [Roman Yepishev]

* Use upload session context manager. [Roman Yepishev]

    This context manager allocates an action token that replaces
    session/signature during uploads. This avoids signature check
    failure if an upload operation needs to be retried.

* Allow importing module, but fail on init. [Roman Yepishev]

* MediaFire Backend - initial version. [Roman Yepishev]

* Backed out changes made by patching for bug #1541314.  These   patches
should not have been applied to the 0.7 series. [Kenneth Loafman]

* Added acdclibackend.py from Stefan Breunig and Malay Shah   - renamed
from amazoncloudbackend to stress use of acd\_cli * Fixed some 2to3
and Pep8 issues that had crept in. [Kenneth Loafman]

* Fixed bug 1474994 Multi backend should offer mirror option  - added
query parameter option to multi-backend  - added mode parameter to
alter how the backend list is operated on (mirror/stripe)  - added
onfail parameter to alter how backend failure is handled  - updated
man-page with documentation. [Thomas Harning Jr]

* Make kerberos optional for webdav backend. [Filip Pytloun]

* Applied patch from kay-diam to fix error handling in ssh pexpect,
fixes bug #1541314. [ken]

* Fix bug #1540279 - mistake in --help. [Kenneth Loafman]

* Clean up pep8 issues. [Kenneth Loafman]

* Fix for bug #1538333 - assert filecount == len(self.files\_changed)
- added flush after every write for all FileobjHooked files which
should prevent some errors when duplicity is forcibly closed. [Kenneth Loafman]

* Add more pylint ignore warnings tags * Adjust so test\_restart.py can
run on Mac as well. [Kenneth Loafman]

* Support GSSAPI authentication in webdav backend. [Filip Pytloun]

* Fix submitter name in changelogs. - Change comment to be correct. [ken]

* Fixed bug #1492301 with patch from askretov (manually refresh oauth). [Kenneth Loafman]

* Fixed bug #1379575 with patch from Tim Ruffling (shorten webdav
response). [Kenneth Loafman]

* Fixed bug #1375019 with patch from Eric Bavier (home to tmp). [Kenneth Loafman]

* Fixed bug #1369243 by adjusting messages to be more readable. [Kenneth Loafman]

* Fixed bug #1260666 universally by splitting the   filelist for delete
before passing to backend. [Kenneth Loafman]

* Pep8 corrections for recently released code. [Kenneth Loafman]

* Bug #1313964 fix. lstrip('/') removed all the slashes, it was an
issue. [mchip]

* Fixed bug #1296793 - Failed to create bucket   - use
S3Connection.lookup() to check bucket exists   - skips Boto's
Exception processing for this check   - dupe of bug #1507109 and bug
#1537185. [ken]

* Applied changes from ralle-ubuntu to fix bug 1072130.   - duplicity
does not support ftpes:// [ken]

* Undo changes to test\_restart.py.  GNU tar is needed. * Fix minor pep8
nit in collections.py. [ken]

* Applied patch from abeverly to fix bug #1475890   - allow port to be
specified along with hostname on S3   - adjusted help text and man
page to reflect the change. [ken]

* Applied patch from shaochun to fix bug #1531154,   - --file-changed
failed when file contains spaces. [Kenneth Loafman]

* Fix stupid issue with functional test path for duplicity. [Kenneth Loafman]

* Make test\_restart compatible with both GNUtar and BSDtar. [Kenneth Loafman]

* Partial fix for bug #1529606 - shell code injection in lftpbackend   -
still need to fix the other backends that spawn shell commands. [Kenneth Loafman]

* Random stuff:   - supply correct path for pydevd under Mac   - fix
some tests to run under Mac as well. [Kenneth Loafman]

* Checkpoint: - remove RPM stuff from makedist - have makedist pull
directly from VCS, not local dir - update po translation directory and
build process - clean up some odd error messages - move Pep8 ignores
to tox.ini. [Kenneth Loafman]

* Checkpoint: - remove RPM stuff from makedist - have makedist pull
directly from VCS, not local dir - update po translation directory and
build process - clean up some odd error messages - move Pep8 ignores
to tox.ini. [Kenneth Loafman]

* 2to3 cleanup. [Kenneth Loafman]

* Pep8 cleanup. [Kenneth Loafman]

* Fix date. [ken]

* Make sure listed files are exactly in the requested path Thanks to
Andreas Knab <knabar@gmail.com> for the pull request. [Matthew Bentley]

* Set fake (otherwise unused) hostname for prettier password prompt
Thanks to Andreas Knab <knabar@gmail.com> for the patch. [Matthew Bentley]

* Add debugging for b2backend. [Matthew Bentley]

* Allow multiple backups in the same bucket. [Matthew Bentley]

* Fix missing import and typos. [Matthew Bentley]

* Undo changes to po files. [Matthew Bentley]

* Remove unnecessary requirements section in manpage. [Matthew Bentley]

* Documentation. [Matthew Bentley]

* Add help text for b2. [Matthew Bentley]

* Add basic error handling. [Matthew Bentley]

* Add BackBlaze B2 backend. Still needs some work (error handling, etc) [Matthew Bentley]

* Support new version of Azure Storage SDK * Refactor \_list method to
support containers with >5000 blobs. [Scott McKenzie]

* Make sure which() returns absolute pathname. [Kenneth Loafman]

* Remove some print statements. [Kenneth Loafman]

* Fix bug #1520691 - Shell Code Injection in hsi backend   - Replace use
of os.popen3() with subprocess equivalent.   - Added code to expand
relative program path to full path.   - Fix hisbackend where it
expected a list not a string. [Kenneth Loafman]

* Fix missing self. [Kenneth Loafman]

* Fix bug #1520691 - Shell Code Injection in hsi backend   - Replace use
of os.popen3() with subprocess equivalent. [Kenneth Loafman]

* Fix #1519694. [Feraudet Cyril]

* Debugged storage class import. [Michal Smereczynski]

* Fixed bug #1511308 - Cannot restore no-encryption, no-compression
backup   - Corrected code to include plain file in
write\_multivolume()   - Added PlainWriteFile() to gpg.py. [Kenneth Loafman]

* Make sure packages using python's tempfile create temp files in
duplicity's temp dir. [ede]

* Reversed previous changes to lockfile.  Now it will take any version
extant in the LP build repository.  (PyPi is not avail in LP build). [Kenneth Loafman]

* Reversed previous changes to lockfile.  Now it will take any version
extant in the LP build repository.  (PyPi is not avail in LP build). [Kenneth Loafman]

* Try adding spaces. [Kenneth Loafman]

* Try lockfile>=0.11.0 (use full version number). [Kenneth Loafman]

* Revert last change. [Kenneth Loafman]

* Try lockfile==0.11.0 instead of lockfile>=0.9. [Kenneth Loafman]

* WindowsAzureMissingResourceError and  WindowsAzureConflictError
classes changed due to SDK changes. [Michal Smereczynski]

* Cleanup issues around Launchpad build, mainly lockfile >= 0.9. [Kenneth Loafman]

* Also check python version number upper bound. we run on 2.6 and 2.7
currently. [ede]

* Don't touch my shebang. [ede]

* Modded tox.ini to use the latest lockfile. [Kenneth Loafman]

* Applied patch from Alexander Zangerl to update to changes in lockfile
API 0.9 and later.  Updated README to notify users. [Kenneth Loafman]

* Add \_\_pycache\_\_. [Kenneth Loafman]

* Upgrade to newest version of pep8 and pylint.   Add three ignores   to
test\_pep8 and one to test\_pylint to get the rest to pass.  They
are all valid in our case. [Kenneth Loafman]

* Fix header date. [Kenneth Loafman]

* The ptyprocess module no longer supports Python 2.6, so fix tox.ini to
use an older version.  Make explicit environs for all tests. [Kenneth Loafman]

* Add support for AWS S3 Standard - Infrequent Access storage class. [Min-Zhong John Lu]

* Fix up broken merge. [Bruce Merry]

* Fix bug #1494228 CygWin: TypeError: basis\_file must be a (true) file
- The problem that caused the change to tempfile.TemporaryFile was due
to the fact that os.tmpfile always creates its file in the system
temp directory, not in the directory specified.  The fix applied was
to use os.tmpfile in cygwin/windows and tempfile.TemporaryFile in all
the rest.  This means that cygwin is now broken with respect to temp
file placement of this one file (deleted automatically on close). [Kenneth Loafman]

* Fix bug #1493573.  Correct option typo in man page. [Kenneth Loafman]

* Add more logging info. [Bruce Merry]

* Fix missing argument in \_error\_code. [Bruce Merry]

* Add an ID cache to the PyDrive backend. [Bruce Merry]

    This is an in-memory cache mapping filenames to object IDs. This potentially
    speeds up searching for a filename (although there is some cost to validate the
    cache on each use). It also ensures that running _query immediately after _put
    will find the file, even if the server doesn't have list-after-write
    consistency (Google Cloud Storage doesn't, but I can't find any info on Drive).

    There are also a number of other improvements:
    - Putting a file with a filename that already exists will replace the file
      in-place, instead of creating a new file with identical filename (which
      Google Drive allows).
    - id_by_name now does a targeted search for just the filename, instead of
      iterating over a complete directory listing.
    - Added _error_code to map 404 errors to backend_not_found
    - Files in the trash are excluded from listings
    - Print a warning when trying to delete a file that doesn't exist.

    This should fix cases where duplicate filenames are created, but it doesn't yet
    deal explicitly with cases where they already exist (it's untested).

    There is also a race condition where if a file is externally deleted during
    _delete, it will raise an exception (which is mapped to backend_not_found).
    That is probably acceptable behaviour, but the behaviour really ought to be
    consistent.

* Par2 backend remove par2 files. [Germar]

* Added debug msgs to the routine checking path selection. [Wojciech Baranowski]

* Refactored the selection.Select.Select method; fewer exit points now. [Wojciech Baranowski]

* Fixed Bug 1438170 duplicity crashes on resume when using gpg-agent
with   patch from Artur Bodera (abodera).  Applied the same patch to
incremental   resumes as well. [Kenneth Loafman]

* Rename tox profile for Launchpad's Precise build server to "lpbuildd-
precise" for clarity (and to make it clear it should be removed once
Precise is no longer supported). [Aaron Whitehouse]

* Set RUN\_CODE\_TESTS to 0 for lpbuildd tox profile, reflecting its
value on the Launchpad build server (and therefore skipping PEP8, 2to3
and pylint). More accurately reflects the system we are mimicking and
saves approximately 1 minute per test run. [Aaron Whitehouse]

* Add further instructions in README-REPO on how to test against one
environment. [Aaron Whitehouse]

* Add lpbuilldd as an additional tox profile, replicating the setup of
the launchpad build server. [Aaron Whitehouse]

* Fixed Bug 1476019 S3 storage bucket not being automatically created
with patch from abeverley. [Kenneth Loafman]

* Fixed Bug 1476019 S3 storage bucket not being automatically created
with patch from abeverley. [Kenneth Loafman]

* Change use of mock.patch to accommodate the obsolete version of
python-mock on the build server (and avoid the following error:
TypeError: patch() got an unexpected keyword argument 'return\_value'
) [Aaron Whitehouse]

* Fixed 2to3 issues. Updated README-REPO with more test information.
Updated pylint and test\_diff2 descriptions to make it clear these
require packages to be installed on the system to pass. All tests pass
on Python 2.6 and Python 2.7 as at this revision. [Aaron Whitehouse]

* Added support for Identity v3. [Dag Stenstad]

* Made globs with trailing slashes only match directories, not files,
fixing Bug #1479545. [Aaron Whitehouse]

* Added functional unittests to exhibit current behaviour of trailing
slashes in globs. See Bug #1479545. [Aaron Whitehouse]

* Delete redundant second sys import in test\_code.py. [Aaron Whitehouse]

* Fixed tox.ini to correctly run individual tests. Updated test\_code.py
to use unittest2 for Python versions < 2.7 (instead of failing).
Improved testing directions in README-REPO. [Aaron Whitehouse]

* Re-enable tests that had been temporarily commented out. [Aaron Whitehouse]

* Add test\_glob\_re unit test back in. [Aaron Whitehouse]

* Remove unnecessary use of mock.patch in unit.test\_selection.py. [Aaron Whitehouse]

* Remove special casing for final glob in glob list as no longer
necessary. [Aaron Whitehouse]

* Fixed Bug #932482 by checking for a trailing slash in each glob and
removing it if present. Enabled tests checking this behaviour. PEP8
fixes along the way. [Aaron Whitehouse]

* Stopped an exclude glob trumping an earlier scan glob, but also
ensured that an exclude glob is not trumped by a later include. Fixed
Bug #884371. Activated the (expectedFailure) tests that were failing
because of this bug. [Aaron Whitehouse]

* Additional tests to exhibit current exclude/scan interaction and
implement two functional tests as unit tests. [Aaron Whitehouse]

* Added unit tests for negative square brackets ([!a,b,c] and [!1-4]). [Aaron Whitehouse]

* Added test cases (unit and functional) to test the current behaviour
of selection.py. [Aaron Whitehouse]

* Fixed bug 1471348 Multi back-end doesn't work with hubiC (again)    -
hubiC should reach up to duplicity.backend.\_\_init\_\_ [Kenneth Loafman]

* Fixed bug 1471348 Multi back-end doesn't work with hubiC   - added
init of appropriate superclass in both cases. [Kenneth Loafman]

* Re-enable the test of the --progress option
(test\_exclude\_filelist\_progress\_option), which was marked as an
expected failure. The issue causing this test to fail was fixed in
revision 1095 and the test now passes. [Aaron Whitehouse]

* Fixed two filename references in po/POTFILES.in, a mistake which crept
in in rev 1093 and caused testing/run-tests to fail with "IndexError:
list index out of range". [Aaron Whitehouse]

* New parameter --gpg-binary allows user to point to a different gpg
binary, not necessarily in path. [ed.so]

* Fixed bug 1466582 - reduce unnecessary syscall with --exclude-if-
present - with   patch from Kuang-che Wu to make sure resulting path
is a directory. [Kenneth Loafman]

* Fixed bug 1466160 - pydrive backend is slow to remove old backup set -
with   patch from Kuang-che Wu to implement \_delete\_list(). [Kenneth Loafman]

* Fixed bug 1466582 - reduce unnecessary syscall with --exclude-if-
present - with   patch from Kuang-che Wu to make sure resulting path
is a directory. [Kenneth Loafman]

* Fixed bug 1466160 - pydrive backend is slow to remove old backup set -
with   patch from Kuang-che Wu to implement \_delete\_list(). [Kenneth Loafman]

* Fixed bug 1452263 - par2 option not working on small processors - with
patch   from Kuang-che Wu to ignore default 30 second timeout. [Kenneth Loafman]

* Fixed bug 1465335 - pydrive still use files in trash can - with patch
from Kuang-che Wu to ignore trashed files. [Kenneth Loafman]

* Fixed bug 791794 - description of --gpg-options is misleading, Simply
needed to add the '--' before the options as in "--opt1 --opt2=parm". [Kenneth Loafman]

* Fix a couple of PEP8 glitches. [Kenneth Loafman]

* Add full\_listing=True so that swiftclient returns more than 10000
objects. Default is False. [Remy van Elst relst@relst.nl]

* Manpage - some reordering, update "A NOTE ON SSH BACKENDS" to the new
prefix+ changes. [ede]

* Make pydrive new gdocs default backend keep gdata backend as
gdata+gdocs:// [ede]

* Support using PyDrive with a regular Google account, instead of a
service account. [Bruce Merry]

* Perform seek(0) on filelist before read(). [Scott McKenzie]

* Reset filelist position to beginning of file after calling read().
This allows file to be read again. [Scott McKenzie]

* Add proper error messages for OneDrive backend when python-requests or
python-requests-oauthlib is not installed (bug 1453355). [Sami Jaktholm]

* Added ability to get single file status from collection-status with
patch from jitao (bug 1044715), like so:   $ duplicity collection-
status --file-changed c1 file://./foo. [Kenneth Loafman]

* Enable --ignore-errors flag in rdiffdir. [Kenneth Loafman]

* Fixed bug 1448249 and bug 1449151 thanks to David Coppit.   - When
patching, close base file before renaming. [Kenneth Loafman]

* Fixed bug 1444404 with patch from Samu Nuutamo   - rdiffdir patch
crashes if a regular file is changed to a non-regular     file
(symlink, fifo, ...) [Kenneth Loafman]

* Fix bug 1432229 in Copy.com backend   - Reply header has no content-
type for JSON detection. Now, we also check     whether the content
starts with '{'. [Carlos Eduardo Moreira dos Santos]

* Move requirements section lower in manpage. [Kenneth Loafman]

* Logging cleanup. [Steve Tynor]

* Typo - missing quote. [Steve Tynor]

* Add doc. [Steve Tynor]

* Add doc. [Steve Tynor]

* Adjust delete to make unit tests pass. [Steve Tynor]

* Document json format. [Steve Tynor]

* Use json config in prep for supporting new pydrive backend that
requires env variables. [Steve Tynor]

* Improved logs; dont allow low level retry to kick in. [Steve Tynor]

* Initial working code - tested with gdocs and file backends. [Steve Tynor]

* Fix bug 1437789 with patch from pdf   - par2backend.py incorrect
syntax in get() [Kenneth Loafman]

* Fix bug 1434702 with help from Robin Nehls   - incorrect response
BackendException while downloading signatures file. [Kenneth Loafman]

* Fix bug 1432999 with hint from Antoine Afalo. [Kenneth Loafman]

* Updated duplicity.pot. [Aaron Whitehouse]

* Remove extraneous string format arg in previous scp fix. [Kenneth Loafman]

* Fix for --pydevd debug environment and location under Eclipse. * Fix
for bug where scp was actually working as scp and not working with
rsync.net because of using extraneous test command in restricted
shell.   Was trying "test -d 'foo' || mkdir -p 'foo'", now only "mkdir
-p foo". [Kenneth Loafman]

* Really fix bug 1416344 based on comment #5 by Roman Tereshonkov. [Kenneth Loafman]

* Fix \_librsyncmodule.c compilation, bug 1416344, thanks to Kari
Hautio. [Kenneth Loafman]

* Fix spelling error in manpage, bug 1419314. [Kenneth Loafman]

* Coalesce CHANGELOG. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E401   - see
http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E231, E241, E251, E261,
E262, E271, E272, E301, E302, E303, E502,     E701, E702, E703, E711,
E721, W291, W292, W293, W391   - see http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E231, E241, E251, E261,
E262, E271, E272   - see http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E231, E241   - see
http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E231, E241   - see
http://pep8.readthedocs.org * Fixes for 2to3 issues. [Kenneth Loafman]

* Changed tests to test filelist, rather than globbing filelist, except
for one functional globbing test of each type to ensure this continues
to work until it is deliberately removed. Changed naming of tests etc
accordingly. [Aaron Whitehouse]

* Removed unnecessary tests (post merging of non-globbing and globbing
filelists) and created a globbing version of the one test that was
only written for non-globbing filelists. [Aaron Whitehouse]

* Updated manual to remove references to globbing filelists and stdin
filelists and make consequential changes to the description of
include-filelist and exclude-filelist behaviour. [Aaron Whitehouse]

* Note Bug #1423367 was fixed in the previous commit. [Aaron Whitehouse]

* Mark --include-filelist-stdin and --exclude-fielist-stdin for
deprecation and hide from --help output. Add additional tests in
stdin\_test.sh to test --include-filelist-stdin and that /dev/stdin is
an adequate replacement. [Aaron Whitehouse]

* Added bash script (stdin\_test.sh) showing that filelists from stdin
were working as expected despite the changes. [Aaron Whitehouse]

* Added deprecation warning to the --exclude-globbing-filelist and
include-globbing-filelist options in commandline.py and hid them from
help output. Commented out functions relating to non-globbing
filelists. Commented out unit tests related to non-globbing filelists. [Aaron Whitehouse]

* Made non-globbing filelists use the globbing code path (ie made all
filelists globbing), as per:
http://lists.nongnu.org/archive/html/duplicity-
talk/2015-01/msg00011.html Fixed Bug #1408411 in the process, as this
issue was limited to the non-globbing code path. [Aaron Whitehouse]

* Added functional and unit tests to show Bug #932482 - that selection
does not work correctly when excludes (in a filelist or in a
commandline option) contain both a single or double asterisk and a
trailing slash. [Aaron Whitehouse]

* Added credit to Elifarley Cruz for one of the test cases. [Aaron Whitehouse]

* Added functional tests to functional/test\_selection.py to show Bug
#884371 (* and ** not working as expected) applies to commandline
--include. [Aaron Whitehouse]

* Added tests to unit/test\_selection.py and
funtional/test\_selection.py to show the behaviour reported in Bug
#884371, i.e. that selection is incorrect when there is a * or ** on
an include line. [Aaron Whitehouse]

* Add option --exclude-older-than to only include recently modified
files. [Angus Gratton]

* Ongoing pep8 corrections. [Kenneth Loafman]

* Applied patch from Adam Reichold to fix bug # 1413792. [Kenneth Loafman]

* Fixed bug # 1414418   - Aligned commandline.py options and help
display contents.   - Aligned commandline.py options and manpage
contents. * Changed --s3\_multipart\_max\_timeout to --s3-multipart-
max-timeout to be   consistent with commandline option naming
conventions. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - 201, 202, 203   - see
http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E127, E128   - see
http://pep8.readthedocs.org. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:   - E111, E121, E122, E124,
E125, E126   - see http://pep8.readthedocs.org. [Kenneth Loafman]

* Remove 'gs' and 's3+http' from uses\_netloc[].  Fixes Bug 1411803. [Kenneth Loafman]

* Fixed variable typo in commandline.py that was causing build fails. [Kenneth Loafman]

* Fixed some tabs/spaces problems that were causing install failures. [Kenneth Loafman]

* Changed passing keyfile via query in URL to passing the key by
environment variable. Fixed manpage accordingly. Restored Azure info
in manpage that was somehow mistakenly deleted. [Yigal Asnis yigalasnis@yahoo.com]

* Fixed URI parsing. [Yigal Asnis yigalasnis@yahoo.com]

* Added pydrive backend aimed to replace the deprecated gdocs backend. [Yigal Asnis yigalasnis@yahoo.com]

* Removed underscores from example Azure container names - added Azure
container name rules to man page - handle unicode messages correctly
in Azure Exceptions. [Scott McKenzie]

* Added test\_exclude\_globbing\_filelist\_progress\_option into
functional/test\_selection.py, which shows the error reported in Bug
#1264744 - that the --exclude-globbing-filelist does not backup the
correct files if the --progress option is used. Test is marked as an
expected failure so as not to cause the test suite to fail. [Aaron Whitehouse]

* Add SWIFT\_REGIONNAME parameter to select SWIFT REGION. See bug
#1376628. [Vincent Cassé]

* Fixed some recently added 2to3 and pep8 issues. [Kenneth Loafman]

* Modified:   duplicity/backends/azurebackend.py. [Scott McKenzie]

    Added _error_code method.

* Modified:   duplicity/backends/azurebackend.py. [Scott McKenzie]

    Added _query method.

* Modified:   bin/duplicity.1   duplicity/commandline.py. [Scott McKenzie]

    Added man page and help entry for Azure backend.

* Added:   duplicity/backends/azurebackend.py. [Scott McKenzie]

* Fix Bug #1408289. [Stephane Angot]

* Selection.py modified to pre-process lines for both globbing and non-
globbing filelists to: remove leading and trailing whitespace; process
quoted filenames correctly; remove blank lines; and ignore full-line
comments. Added tests to unit/test\_selection.py and
functional/test\_selection.py to cover these. Added a new folder
select2 to the testfiles.tar.gz for the new functional tests (clearer
names and a folder with trailing whitespace). [Aaron Whitehouse]

* Added functional test cases to show the issue reported in Bug #1408411
(Filelist (non-globbing) should include a folder if it contains higher
priority included files -
https://bugs.launchpad.net/duplicity/+bug/1408411). [Aaron Whitehouse]

* Add a backend for Microsoft OneDrive. [Michael Stapelberg]

* Fixed bug 1278529 by applying patch supplied in report   - Use
get\_bucket() rather than lookup() on S3 to get proper error msg. [Kenneth Loafman]

* Misc fixes for the following PEP8 issues:    - E211, E221, E222, E225,
E226, E228    - see http://pep8.readthedocs.org. [Kenneth Loafman]

* Fixed bug 1406173 by applying patch supplied in report   - Ignore
.par2 files in remote file list * Removed redundant shell test
testing/verify\_test.sh. [Kenneth Loafman]

* Add else to try-except in badupload functional test, to catch where
the test passes successfully instead of throwing an error (as it
should). [Aaron Whitehouse]

* Add comments to the verify\_test.sh script matching up the tests in
there to the tests implemented in test\_verify.py. All the tests in
the shell script have now been implemented, so the shell script should
perhaps be deleted. [Aaron Whitehouse]

* Add tests to test\_verify.py to test that verify fails if the archive
file is corrupted. Changed file objects to use the with keyword to
ensure that the file is properly closed. Small edit to find statement
in verify\_test.sh to make it work as expected (enclose string in
quotes). [Aaron Whitehouse]

* Simplify test\_verify.py to just do a simple backup and verify on a
single file in each test. Modify tests to correctly use --compare-data
option and to add tests for verify when the source files have the
atime/mtime manipulated. [Aaron Whitehouse]

* Make ssh an unsupported backend scheme * Temporarily disable
RsyncBackendTest and test\_verify\_changed\_source\_file. [Kenneth Loafman]

* Move netloc usage definitions into respective backends. [ed.so]

* Added in tests including compare\_data. [Aaron Whitehouse]

* Added test\_verify\_changed\_source\_file test to flag up the issue
mentioned in Bug #1354880. [Aaron Whitehouse]

* Allow --sign-key to use short format, long format alt. full
fingerprint. [Andreas Olsson]

* Source formatted, using PyDev, all source files to fix some easily
fixed   PEP8 issues. Use ignore space when comparing against previous
versions. [Kenneth Loafman]

* Fix identity file parsing of --ssh-options for paramiko manpage fixes. [ede]

* Modded .bzrignore to ignore *.egg test dependencies, normalized,
sorted. [Kenneth Loafman]

* Manually merged in lp:\~m4ktub/duplicity/0.6-reliability   - Per fix
proposed in Bug #1395341. [Kenneth Loafman]

* Fix changelogs comments. [Kenneth Loafman]

* Fixed bug 1255453 with changes by Gaudenz Steinlin, report backend
import   results, both normal and failed, at INFO log level. [Kenneth Loafman]

* Fixed bug 1236248 with changes by az, manpage warning about --extra-
clean. [Kenneth Loafman]

* Fixed bug 1385599 with changes by Yannick Molin. SSL settings are now
conditioned on protocol ftp or ftps. [Kenneth Loafman]

* Update man page. [Adrien Delhorme]

* Update man page Add hubic identity module. [Adrien Delhorme]

* Add Hubic backend. [Adrien Delhorme]

* In webdavbackend.py:   - Fixed bug 1396106 with change by Tim Ruffing,
mispelled member.   - Added missing 'self.' before member in error
message. [Kenneth Loafman]

* Undid move of testing/test\_code.py.  Instead I fixed it   so that it
would not run during PPA build.  It now needs   the setting
RUN\_CODE\_TESTS=1 in the environment which is   supplied in the
tox.ini file. [Kenneth Loafman]

* Moved testing/test\_code.py to testing/manual/code\_test.py   so PPA
builds would succeed.  Should be moved back later. [Kenneth Loafman]

* Remove valid\_extension() check from file\_naming.py.  It was
causing failed tests for short filenames.  Thanks edso. [Kenneth Loafman]

* Partial fix for PPA build failures, new backend name. [Kenneth Loafman]

* Fix dpbx import error import lazily. [ed.so]

* Fix for failing PPA builds.  FTP backend has variable class names. [Kenneth Loafman]

* Fix files list. [Kenneth Loafman]

* Fix typo ('hidding' to 'hiding') [Aaron Whitehouse]

* Escape filename before printing in unicode. [Michael Terry]

* Add https cert verification switches. [ed.so]

* More manpage fixes/reformatting retire parameters --ssh-backend,
--use-scp, functionality is achieved via scheme:// setting now add
lftp webdav support add lftp fish support fix assertionerror when
using par2+ backend. [ed.so]

* Manpage: document ftp changes/minor enhancements. [ed.so]

* Allow ftp backend selection via prefix. [ed.so]

* Rename lftp/ncftp backends. [ed.so]

* Restore ncftp backend. [ed.so]

* Support older versions of dpkg-parsechangelog. [Michael Terry]

* Some small testing fixes to work on older copies of mock and pylint. [Michael Terry]

* Minor tweaks to debian/control to fix building on older versions of
Ubuntu. [Michael Terry]

* Fix Edgar's name. [Michael Terry]

* Add debian packaging. [Michael Terry]

* Avoid super() on old-style class. [Michael Terry]

* Fix pylint/pep8 nits so that tests pass. [Michael Terry]

* Adjust unit tests to expect single FTP backend. [Kenneth Loafman]

* Use lftp for both FTP and FTPS. [Moritz Maisel]

* Minor accounting fix. [Kenneth Loafman]

* Merged in lp:\~johnleach/duplicity/1315437-swift-container-create   -
Check to see if the swift container exists before trying to create it,
in case we don't have permissions to create containers. Fixes #1315437. [Kenneth Loafman]

* Clean up imports. [Kenneth Loafman]

* Merged in lp:\~ed.so/duplicity/0.7-dpbx.importfix   - fix this
showstopper with the dropbox backend     "NameError: global name
'rest' is not defined" [Kenneth Loafman]

* Merged in lp:\~jflaker/duplicity/BugFix1325215   - The reference to "
--progress\_rate" in the man page as a parameter is     incorrect.
Should be "--progress-rate". [Kenneth Loafman]

* Change the branch for stable. lp:duplicity/stable doesn't exist and so
I've changed this to lp:\~duplicity-team/duplicity/0.6-releases as
this is the only non-Windows, non-dev branch. [Aaron Whitehouse]

* Corrected the extra dot in the stable branch line at step 1. [Aaron Whitehouse]

* Updated README-REPO to reflect restructuring of directories. See
https://answers.launchpad.net/duplicity/+question/252898. [Aaron Whitehouse]

* Fixed bug 1375304 with patch supplied by Aleksandar Ivanovic. [Kenneth Loafman]

* Fix two small typos in duplicity man page. [Jeffrey Rogers]

* Clarify verify's functionality as wished for by a user surprised with
a big bandwidth bill from rackspace. [ede]

* Added sxbacked.py, Skylable backend.  Waiting on man page updates. [Kenneth Loafman]

* Fixed bug 1327550: OverflowError: signed integer is greater than
maximum   - Major and minor device numbers are supposed to be one byte
each.  Someone     has crafted a special system image using OpenVZ
where the major and minor     device numbers are much larger (ploop
devices).  We treat them as (0,0). [Kenneth Loafman]

* Added user defined verbatim options for par2. [Anton Maklakov]

* Restore accidental deletion. [Kenneth Loafman]

* Fix setdata() not being called a better way. [Michael Terry]

* Use writefileobj instead of direct write, for less code and so that we
call setdata() [Michael Terry]

* More reliably reset webdav connection. [Michael Terry]

* Webdav backend fix "BackendException: Bad status code 200 reason OK. "
when restarting an interrupted backup and overwriting partially
uploaded volumes. [ede]

* README: add copy.com requirements. [Marco Trevisan (Treviño)]

* Add copy.com to man file. [Marco Trevisan (Treviño)]

* CopyComBackend: import non-main modules only when needed. [Marco Trevisan (Treviño)]

* CopyComBackend: remove unneded upload checks. [Marco Trevisan (Treviño)]

* CopyComBackend: implement \_query method. [Marco Trevisan (Treviño)]

    Now the backend should be pretty complete

* CopyComBackend: disable the \_delete\_list support, it won't work if a
file doesn't exist. [Marco Trevisan (Treviño)]

    If a file in list does not exist, the Copy server will stop deleting the subsequent stuff,
    raising an error and making test_delete_list to fail.

* CopyComBackend: add ability to delete list of files. [Marco Trevisan (Treviño)]

* Backends: Add Copy.com support, implement basic operations. [Marco Trevisan (Treviño)]

* Update shebang line to python2 instead of python to avoid confusion. [Kenneth Loafman]

* Support py2.6.0. [Michael Terry]

* Clean up indentation mismatches. [Kenneth Loafman]

* Misc format fixes. [Kenneth Loafman]

* Applied expat fix from edso.  See answer #12 in
https://answers.launchpad.net/duplicity/+question/248020   * Forward-
ported from r980 in 0.6-series. [Michael Terry]

* First cut of 0.7.00 Changelog. [Kenneth Loafman]

* Fix running ./testing/manual/backendtest to be able to find config.py
and fix the tests in testing/manual/ to not be picked up by ./setup.py
test. [Michael Terry]

* Convert exceptions to unicode. [Michael Terry]

* Further fixes. [Michael Terry]

* Fix map usage for py3 readiness. [Michael Terry]

* Fix filter usage for py3 readiness. [Michael Terry]

* Fixed bug #1312328 WebDAV backend can't understand 200 OK response to
DELETE   - Allow both 200 and 204 as valid response to delete. [Kenneth Loafman]

* Minor fixes. [Michael Terry]

* Add ftp backend test. [Michael Terry]

* Drop popen\_subprocess\_persist in favor of just the basic version;
add ftps backend test. [Michael Terry]

* And test hsi backend too. [Michael Terry]

* Add fake tahoe executable, so we can test the tahoe backend. [Michael Terry]

* Add support for backend prefixes, allow rsync backend to use local
paths, and add some more tests. [Michael Terry]

* Add some backend tests, clean up par2backend, and general fixes. [Michael Terry]

* Checkpoint. [Michael Terry]

* Add overrides dir. [Michael Terry]

* More minor fixes. [Michael Terry]

* Move rootfiles.tar.gz into manual directory. [Michael Terry]

* Add initial pep8 and pylint tests. [Michael Terry]

* Minor fixes. [Michael Terry]

* Make run-tests scripts go through tox, this makes all our standard
test-running modes ultimately go through ./setup test. [Michael Terry]

* Drop little-used misc.py. [Michael Terry]

* More reorg of testing/ [Michael Terry]

* Convert unicode to utf8 before passing to print. [Michael Terry]

* Drop static.py. [Michael Terry]

* Fix subprocess usage to work in py2.6 and fix a missing unicode. [Michael Terry]

* Solve has\_key 2to3 fix. [Michael Terry]

* Move imports fix to the 'don't care' section. [Michael Terry]

* Solve import 2to3 fix. [Michael Terry]

* Solve numliterals 2to3 fix. [Michael Terry]

* Solve long 2to3 fix. [Michael Terry]

* Move urllib fix to the 'don't care' section. [Michael Terry]

* Solve basestring 2to3 fix. [Michael Terry]

* Move long and raw\_input fixes to the 'don't care' section. [Michael Terry]

* Solve reduce 2to3 fix. [Michael Terry]

* Solve raise 2to3 fix. [Michael Terry]

* Mark callable and future fixes as things we explicitly don't care
about. [Michael Terry]

* Solve apply 2to3 fix. [Michael Terry]

* Solve idioms 2to3 fix. [Michael Terry]

* Solve ws\_comma 2to3 fix. [Michael Terry]

* Solve renames 2to3 fix. [Michael Terry]

* Solve except 2to3 fix. [Michael Terry]

* Add test\_python3.py to test readiness of source code to run under
python3 directly. [Michael Terry]

* Fix typo. [Michael Terry]

* Drop local copy of pexpect -- only used by one of our ssh backends and
our tests. [Michael Terry]

* Fix drop-u1 merge. [Michael Terry]

* Drop support for Ubuntu One, since it is closing. [Michael Terry]

* Drop support for Python 2.4 and 2.5. [Michael Terry]

* Add missing mock dep. [Michael Terry]

* Whoops, make dist dir first during sdist. [Michael Terry]

* Enable/use more mordern testing tools like nosetest and tox as well as
more common setup.py hooks like test and sdist. [Michael Terry]

* Consolidate all the duplicity-running code in the test framework. [Michael Terry]

* Added support for amazon s3 encryption by the use of --s3-use-server-
side-encryption. [Fredrik Loch fredrik.loch@gmail.com]

* Added support for serverside encryption in amazon s3. [Fredrik Loch fredrik.loch@gmail.com]

* Fixed boto import issues. [Prateek Malhotra]

* Fix dpbx backend "NameError: global name 'rest' is not defined" [ede]

* Fix boto import. [Kenneth Loafman]

* Make sure each process in a multipart upload get their own fresh
connection. [Prateek Malhotra]

* Updated manpage and tweaked boto backend connection reset. [Prateek Malhotra]

* Added max timeout for chunked uploads and debug lines to gauage upload
speed. [Prateek Malhotra]

* Fixes for merging multi boto backend. [Prateek Malhotra]

* Fixes https://bugs.launchpad.net/duplicity/+bug/1218425. [Prateek Malhotra]

* Fixed get\_connection for new generic storage. [Prateek Malhotra]

* Fixed merge conflicts after merging in changes from main branch,
mostly due to Google Storage class addition. [Prateek Malhotra]

* Trying fix to properly destroy S3 connections. [Prateek Malhotra]

* README update for BOTO version requirement. [Prateek Malhotra]

* Added support for AWS S3 Glacier. [Prateek Malhotra]

* Added commentS. [Prateek Malhotra]

* Added max proc rule for multipart S3 uploads. [Prateek Malhotra]

* Fix pexpect import. [Michael Terry]

* Add documentation to manpage rename \~par2wrapperbackend.py. [Germar]

* Add test that includes unicode characters to check the gpg prompt. [Michael Terry]

* Encode prompt phrase before passing to getpass. [Michael Terry]

* Applied two patches from mailing list message at:
https://lists.nongnu.org/archive/html/duplicity-
talk/2014-01/msg00030.html   "Added command line options to use
different prefixes for manifest/sig/archive files"   This resolves
https://bugs.launchpad.net/duplicity/+bug/1170161 and provides   a
workaround for https://bugs.launchpad.net/duplicity/+bug/1170113. [Kenneth Loafman]

* Update to translations. [Kenneth Loafman]

* Encode sys.argv using system filename encoding before printing. [Michael Terry]

* Remove --add-concurrency option and enhance the error message the case
where an existing lockfile is detected. [Louis Bouchard]

* Reformat --allow-concurrency text and add mention of stale lockfile. [Louis Bouchard]

* Update manpage with new --add-concurrency option. [Louis Bouchard]

* Add the --allow-concurrency option to disable the locking mechanism
that this patch implements. By default, only one instance of duplicity
will be allowed to run at once. When using this switch it disable the
locking mechanism to allow more than one instance to run
simultaneously (LP: #1266763) [Louis Bouchard]

* Raise exception if we can't connect to S3 rather than just silently
pretending there are no files. [Michael Terry]

* Restored patch of gdocsbackend.py from original author (thanks ede) *
Applied patch from bug 1266753: Boto backend removes local cache if
connection cannot be made. [Kenneth Loafman]

* Recommit: implement fix as suggested by original autor
http://lists.nongnu.org/archive/html/duplicity-
talk/2013-11/msg00017.html. [ede]

* Reformat to be more consistent.  Remove tabs. [Kenneth Loafman]

* Reverted changes to gdocsbackend.py. [Kenneth Loafman]

* Leftover from previous commit (thx Kostas for paying attention) [ede]

* Implement fix as suggested by original autor
http://lists.nongnu.org/archive/html/duplicity-
talk/2013-11/msg00017.html. [ede]

* Restored missing line from patch of gdocsbackend.py. [Kenneth Loafman]

* Fix help printing. [Michael Terry]

* Promote filenames to unicode when printing to console and ensure that
filenames from backend are bytes. [Michael Terry]

* Nuke tabs. [Kenneth Loafman]

* Upstream debian patch "webdav create folder recursively" http://patch-
tracker.debian.org/package/duplicity/0.6.22-2. [ede]

* Upstream debian patch "paramiko logging" http://patch-
tracker.debian.org/package/duplicity/0.6.22-2. [ede]

* Fix the fix for dropbox backend. [ede]

* Remove obsolete cfpyrax+http:// scheme from manpage. [ede]

* Update Changelog.GNU fix "Import of duplicity.backends.dpbxbackend
Failed: No module named dropbox" [ede]

* Add mega documentation. [ede]

* Some formatting fixes to rman issues on website display. [ede]

* Update boto minimum version requirements. [Lee Verberne]

* Changed to default to pyrax backend rather than cloudfiles backend.
To revert to the cloudfiles backend use '--cf-backend=cloudfiles' [Kenneth Loafman]

* Fixed cfpyrax entry in man page. [Jonathan Krauss]

* Added Pyrax backend for Rackspace Cloud. [Jonathan Krauss]

* Added Pyrax backend for Rackspace Cloud. [Jonathan Krauss]

* Applied patch to fix "Access GDrive through gdocs backend failing"   -
see https://lists.nongnu.org/archive/html/duplicity-
talk/2013-07/msg00007.html. [Kenneth Loafman]

* Avoid throwing exception because of None element in patch sequence. [Michael Terry]

* Handle a disappearing source file across restarts better. [Michael Terry]

* Fix test comments. [Michael Terry]

* Don't keep dangling volume info in manifest. [Michael Terry]

* Show path type in log when listing files. [Michael Terry]

* Better error message for chown fail. [Gábor Lipták]

* Merged in lp:\~verb/duplicity/bucket\_root\_fix   - Fix bug that
prevents backing up to the root of a bucket with boto backend. [Kenneth Loafman]

* Don't chop the first argument off when restarting (in an admittedly
difficult-to-reach bit of code) [Michael Terry]

* Fix some spacing. [Michael Terry]

* Wrap whole seq2ropath function in a general try/except rather than a
more focused approach -- any problem patching a file should be ignored
but logged before moving on. [Michael Terry]

* If a common exception happens when collapsing a non-file patch, just
log it and continue. [Michael Terry]

* Or better yet, just drop the stanza, it shouldn't be needed. [Michael Terry]

* Fix else: to be except Exception: [Michael Terry]

* Fix util.ignore\_missing; patch by Matthias Witte. [Michael Terry]

* Applied patch from bug 1216921 to fix ignore\_missing(). [ken]

* Changes for 0.6.22. [ken]

* Update paramiko links add command  parameters to synopsis add
--compare-data some polishing several improvements. [ede]

* Applied patch from Eric S Raymond to man page to fix markup problems. [ken]

* Fix requesting filename. [Christian Kornacker]

* Adapt to mega.py API changes. [Christian Kornacker]

* Cleanup copyright notice. [Christian Kornacker]

* Adding Mega backend for mega.co.nz. [Christian]

    this code is based on gdocsbackend.py

    it requires either
    https://github.com/ckornacker/mega.py.git
    or (changes not yet pulled)
    https://github.com/richardasaurus/mega.py.git

* Add documentation for GCS to duplicity.1. [Lee Verberne]

* Add config template for testing boto backend with GCS. [Lee Verberne]

* Add support for Google Cloud Storage to boto backend (single threaded
only) [Lee Verberne]

* Explicitly set umask in test\_tarfile.py. [Lee Verberne]

    tar honors umasks which causes the unittest to fail if a more restrictive mask
    (e.g. 027) is set.  This change sets umask explicitly.

* Adds doc. [Matthieu Huin]

* Better handling of authentication alternatives. [Matthieu Huin]

* Updates copyright. [Matthieu Huin]

* Fixes data size type. [Matthieu Huin]

* Fixes missing argument. [Matthieu Huin]

* Fixes wrong environment variable being used. [Matthieu Huin]

* Adds OpenStack Swift backend. [Matthieu Huin]

* Use FTP\_PASSWORD with pexpect backend without requiring --ssh-
askpass. [Nathan Scowcroft]

* Add par2 wrapper backend. [Germar]

* Applied duplicity-ftps.patch from
https://bugs.launchpad.net/duplicity/+bug/1104069   - Don't try to
delete an empty file list. [Kenneth Loafman]

* Applied blocksize.patch from
https://bugs.launchpad.net/duplicity/+bug/897423   - New option --max-
blocksize (default 2048) to allow increasing delta blocksize. [Kenneth Loafman]

* No more cleartext credentials in the code. [jno]

* Application Key & Secret get obfuscated to fit the rq of Dropbox. [jno]

* Crosser's patch applied. [jno]

* Propagate exceptions upward to facilitate retries. [jno]

* Typo fixed. [jno]

* Log.py had no Error() to supplement Info(), Warn(), and Debug() -
fixed. [jno]

* 1. usage note added (on separate Dropbox account). 2. extraneous and
useless mkdir call was removed in put() method. [jno]

* Even more logging for unhandled exceptions to catch Error connecting
to "api-content.dropbox.com" [jno]

* Traceback logging added for semi-unhandled exceptions to catch that
strange .encode() call error. [jno]

* Progress: Removed an unneeded if. [Juan A. Moya Vicén]

* Progress: Fixes for the previous commit after extensive testing:     -
Fixed the index computation for the rotating cache of Snapshots     -
Moved the start point for the Log progress thread after a proper
computation of the starting volume in case of restart, and adapted
code for it. [Juan A. Moya Vicén]

* Progress: Cover the sigtar and manifest upload with the progress
reporting. Now the last 1% will be dedicated to this upload and
properly report stallment when network goes off while this happens. [Juan A. Moya Vicén]

* Progress: Fixed a missing condition for when the progress flag is not
used. [Juan A. Moya Vicén]

* Progress: Cap data progress upload from 0..99% and show 100% only when
sigtar and manifest file has uploaded correctly. [Juan A. Moya Vicén]

* Progress: Avoid completed percentage to drops between backup retries
when backup fails and has to be restarted.           The current
progress is offset by the previous uncompleted backup from the last
volume that upload correctly.           To achieve it, the progress
tracker now snapshots the current progress to the cache each completed
volume, then           recovers this information later when retrying a
failed backup. [Juan A. Moya Vicén]

* Progress: The algorithm now will drop the confidence interval
adaptively when overpassing the 100%. This may happen when the sigma
is large due to a very heterogeneous distribution of the size of
deltas in files. In this case, the C.I. will be drop by half to adapt
to the variability. If it happens again, it will disregard the sigma
and trust the mean only. [Juan A. Moya Vicén]

* Progress: Simplified computation of progress to compute an upper
bound, fit to a smooth curve. This method embraces better more "change
distribution" scenarios and is much simpler to compute. And also, full
backups will assume 1:1 correspondence in change distribution, so
progress bars during full will be computed linearly, which is closer
to reality. [Juan A. Moya Vicén]

* Progress: Reporting speed in bps for log file. [Juan A. Moya Vicén]

* Progress: Changed verbosity to NOTICE, so progress messages appears by
default when --progress flag is on. [Juan A. Moya Vicén]

* Progress: Added average speed to the log file. [Juan A. Moya Vicén]

* Progress: Fixed a typo in if clause. [Juan A. Moya Vicén]

* Progress: Bugfixed a posible division by zero. [Juan A. Moya Vicén]

* Progress: New feature to compute progress of compress & upload files
The heuristics try to infer the ratio between the amount of data
collected     by the deltas and the total size of the changing files.
It also infers the     compression and encryption ration of the raw
deltas before sending them to     the backend.     With the inferred
ratios, the heuristics estimate the percentage of completion     and
the time left to transfer all the (yet unknown) amount of data to
send.     This is a forecast based on gathered evidence. [Juan A. Moya Vicén]

* Paramiko backend, delete(): Terminate when all files have been deleted
successfully. [Tilman Blumenbach]

    Previously, delete() would delete the entire list of files (as expected) and
    then *always* go into its "retry on error" loop, i. e. it would try to delete
    the (now non-existant) files _again_, which obviously always caused it to fail
    eventually.

* Make the Paramiko backend work with Paramiko 1.10.0. [Tilman Blumenbach]

* The fix in revno. 912 didn't take into account that the parameter
"body" passed into request is overloaded, so when it was NULL or of a
type other than file, it would fail.  This checks if "body" is of type
"file" before actually seek()'ing back to the beginning of the file. [Christopher Townsend]

* Fixes the case where the file pointer to the backup file was not being
set back to the beginning of the file when an error occurs.  This
causes subsequent retries to fail with 400 Bad Request errors from the
server.  This is due to a change in revno. 901 where a file handle is
used instead of a bytearray. * Fixes the removal of Content-Length
from the header in revno. 901.  Content-Length is required according
to the Ubuntu One API documentation. [Christopher Townsend]

* Renamed to --compare-data to make it reusable on other actions e.g.
force data comparision on backup runs where files were modified but
mtime was not set properly by buggy software. [ede]

* Add switch --verify-data, to selectively enable formerly always
disabled data comparison on verify runs. [ede]

* Note on first run was added to the man page. [jno]

* THE BACKEND ITSELF HAS BEEN FINALLY ADDED. [jno]

* Man page fixed to mention dpbx: backend. [jno]

* Dropbox backend (dpbx:) has been added. [jno]

* Applied patches from Laszlo Ersek to rdiffdir to "consume a chain of
sigtar   files in rdiffdir delta mode" which supports incremental
sigtar files. [Kenneth Loafman]

* Make \_librsync module compile under Python 3. [Michael Terry]

* Use PyGI instead of older pygobject style for gio backend. [Michael Terry]

* Webdav manpag updates. [ede]

* Add auto-ctrl-c-test.sh to help stress-test restart support. [Michael Terry]

* Move man page changes to a separate uptodate merge branch. [ede]

* Manpage - document ssl cert verification in man page backend.by -
retry\_fatal decorator accepts now premature fatal errors and supplys
a retry\_count instance variable webdavbackend.py - added ssl cert
verification - added http redirect support - added always create new
connection on retrys - much more debug output for problem pinpointing
commandline.py, globals.py - added ssl cert verification switches
errors.py - add FatalBackendError for signalling exactly that. [ede]

* Reconnect on errors as a precaution against ssl errors see
https://bugs.launchpad.net/duplicity/+bug/709973. [ede]

* Use a copy of file1 rather than writing out a new small file so that
it is clearer the first block is skipped rather than the whole file. [Michael Terry]

* Add test to confirm expected behavior if new files appear before we
restart a backup. [Michael Terry]

* Whoops, fix a test I broke with last commit because I didn't add
get\_read\_size to the mock writer. [Michael Terry]

* Fix block-loss when restarting inside a multi-block file due to block
sizes being variable. [Michael Terry]

* Fix block-loss when restarting after a volume ends with a multi-block
file; fixes test\_split\_after\_large() [Michael Terry]

* Fix block-loss when restarting after a volume ends with a small file;
fixes test\_split\_after\_small() [Michael Terry]

* Add more tests for various restart-over-volume-boundary scenarios. [Michael Terry]

* Move non-encryption-specific tests to the right class. [Michael Terry]

* Tests: add a WithoutEncryption class to restarttest.py. [Michael Terry]

* Fixed 1091269 Data corruption when resuming with --no-encryption   -
Patches from Pascual Abellan that make block size consistent and
that add no-encryption option to manual-ctrl-c-test.sh.   - Modified
gpg.py patch to use 64k block size so unit test passes. [Kenneth Loafman]

* Python3 fix reuse normalized url from oauth. [ede]

* Why bother reading when we can deliver a filehandler alltogether. [ede]

* Fix "not bytearray" prevents PUT with python 2.6. [ede]

    conn.request(method, request_uri, body, headers)
      File "/usr/lib/python2.6/httplib.py", line 914, in request
        self._send_request(method, url, body, headers)
      File "/usr/lib/python2.6/httplib.py", line 954, in _send_request
        self.send(body)
      File "/usr/lib/python2.6/httplib.py", line 759, in send
        self.sock.sendall(str)
      File "/usr/lib/python2.6/ssl.py", line 203, in sendall
        v = self.send(data[count:])
      File "/usr/lib/python2.6/ssl.py", line 174, in send
        v = self._sslobj.write(data)

* Don't hang after putting in credentials (cause it silently retries in
background) but go through with backup. [ede]

* Fix imports not being global. [ede]

* Manpage - document Ubuntu One required libs - added continous
contributors and backend author notes. [ede]

    U1backend
    - lazily import non standard python libs

* Clear up PASSPHRASE reusage as sign passphrase minor fixes. [ede]

* Now files are directly uploaded to destination folder/collection. This
also fixes bug that created a copy of all files in the root
folder/collection in Google Drive. [Carlos Abalde]

* Make sure u1backend returns filenames as utf8. [Michael Terry]

* Added --hidden-encrypt-key testcases. [Marcos Lenharo]

* Added more details in man page. [Marcos Lenharo]

* Fixed a typo in man mage. [Marcos Lenharo]

* Allows duplicity to encrypt backups with hidden key ids. See --hidden-
recipient in man gpg(1) [Marcos Lenharo]

* Add correct error code catch only exceptions again. [ede]

* Catch exceptions only. [ede]

* Show error value instead of class. [ede]

* Bugfix: webdav retrying broke on ERRORS like "error: [Errno 32] Broken
pipe" in socket.pyas reported here
https://answers.launchpad.net/duplicity/+question/212966. [ede]

    added a more generalized 'retry_fatal' decorator which makes retrying backend methods even easier

* Avoid using TestCase.addCleanup, which isn't in older python versions. [Michael Terry]

* Nuke tabs. [Kenneth Loafman]

* Don't duplicate a test for whether we should get passphrase in two
places -- one of them will be out of sync. [Michael Terry]

* Allow .netrc auth for lftp backend. [ede]

* More formatting fixes, clarifications in sections EXAMPLES, FILE
SELECTION. [ede]

* Add a cache for password and group lookups.  This significantly
improves runtime with very large password and group configurations. [Steve Atwell]

* Merged in lp:\~mterry/duplicity/u1-ascii-error   - Fix for u1backend
unicode error.  Patch by Paul Barker. [Kenneth Loafman]

* We no longer need to preserve new-sigs in the cache, since we fixed
the bug keeping them on the remote side. [Michael Terry]

* Port u1backend to oauthlib. [Michael Terry]

* Fix U1 backend's ascii error.  Patch by Paul Barker. [Michael Terry]

* Fix python 2.4 vs 2.5 syntax error. [ede]

    File "/usr/lib64/python2.4/site-packages/duplicity/commandline.py", line 188
        return encoding if encoding else 'utf-8'
                         ^
    SyntaxError: invalid syntax

    see
    http://lists.nongnu.org/archive/html/duplicity-talk/2012-10/msg00027.html

* Update CHANGELOG to reflect all bugs fixed. [Kenneth Loafman]

* Remove dist/mkGNUchangelog script.     * Prep files for 0.6.20
release. [Kenneth Loafman]

* Applied patch from az for bug #1066625 u1backend   + add delay between
retries. [Kenneth Loafman]

* Update Changelog.GNU. [Kenneth Loafman]

* U1backend: interpret http code 402 as no-space-left rather than 507. [Michael Terry]

* Update CHANGELOG and Changelog.GNU. [Kenneth Loafman]

* 1039001 --exclude-if-present and --exclude-other-filesystems causes
crash with inaccessible other fs. [Kenneth Loafman]

* 995851 doc improvement for --encrypt-key, --sign-key. [Kenneth Loafman]

* Update Changelog.GNU. [Kenneth Loafman]

* 1066625 ubuntu one backend does not work without gnome/dbus/x11
session. [Kenneth Loafman]

* Updated Changelog.GNU. [Kenneth Loafman]

* Added gdocs, rsync REQUIREMENTS. [ede]

* Some refinements add cloudfiles documentation. [ede]

* Sort urls alphabetically add abs vs. relative file urls. [ede]

* Typo. [ede]

* Minor fix. [ede]

* Some clarifications mostly for ssh pexpect backend. [ede]

* Update Changelog.GNU. [Kenneth Loafman]

* Some clarifications in README. [ede]

* Refactor GnuPGInterface to gpginterface.py reasoning can be found in
README. [ede]

* Update Changelog.GNU. [Kenneth Loafman]

* Place gpg.py tempfiles in duplicity's tmp subfolder which is cleaned
whatever happens. [ede]

* Tests: apparently on hardy chroots, /bin can be smaller than 3MB
compressed, so instead of using /bin in test\_multi\_volume\_failure,
use largefiles. [Michael Terry]

* Tests: whoops, I had accidentally disabled one of the new tests for
ignoring double entries in a tarball. [Michael Terry]

* Tests: don't use subprocess.check\_output, which was only added in
Python 2.7. [Michael Terry]

* Don't use unittest.TestCase.assertSetEqual, which isn't supported in
older Python versions. [Michael Terry]

* Update Changelog.GNU. [Kenneth Loafman]

* Probably fix. [ede]

    File "/usr/local/lib/python2.7/dist-packages/duplicity/backends/_ssh_pexpect.py", line 223, in run_sftp_command
        log.Warn("Running '%s' with commands:\n %s\n failed (attempt #%d): %s" % (commandline, "\n ".join(commands), n, msg))

* Wrap CHANGELOG to col 80. [Kenneth Loafman]

* Update Changelog.GNU. [Kenneth Loafman]

* Gracefully handle multiple duplicate base dir entries in the sigtar;
avoid writing such entries out. [Michael Terry]

* Retry cloudfiles deletes. [Greg Retkowski]

    This will retry cloudfile delete commands with large numbers of
    archive files over mediocre links deletes occasionally fail
    and should be retried.

* Missing space. [ede]

* Disabled hyphenation and block justification for better readablility
of command line examples. - reformatted REQUIREMENTS section for
hopefully better online rendering - minor clarifications. [ede]

* Delete signature files when doing remove-all-but. [Michael Terry]

* Ssh: actually delete all the requested files, not just the first one. [Michael Terry]

* Update Changelog.GNU and CHANGELOG. [Kenneth Loafman]

* Make sure translations are in utf-8. [Michael Terry]

* Fix dates. [Kenneth Loafman]

* Update CHANGELOG and Changelog.GNU to reflect recent changes. Update
location path in mkGNUChangelog.sh. [Kenneth Loafman]

* Use tempfile.TemporaryFile() so unused temp files are deleted
automagically. [edso]

* Propbably solve bug 'Out of space error while restoring a file' see
bug tracker/mailing list
https://bugs.launchpad.net/duplicity/+bug/1005901
http://lists.gnu.org/archive/html/duplicity-talk/2012-09/msg00000.html. [edso]

* Fix rare 'TypeError: encode() argument 1 must be string, not None'
read here http://lists.nongnu.org/archive/html/duplicity-
talk/2012-09/msg00016.html. [edso]

* Log.py: add a couple comments to reserve error codes 126 and 127
because they conflict with running duplicity under pkexec (very
similar to how 255 is reserved because gksu uses it) [Michael Terry]

* Add note on GnuPGInterface and multiple GPG processes. [Kenneth Loafman]

* Fixed ssh/gio backend import warnings  + ssh paramiko backend imports
paramiko lazily now  + gio backend is not imported automatically but
on request when --gio option is used - added a warning when --ssh-
backend is used with an incorrect value. [edso]

* Ssh paramiko backend respects --num-retries now - set retry delay for
ssh backends to 10s - ssh pexpect backend  + sftp part does not claim
'Invalid SSH password' although it's only 'Permission denied' now  +
sftp errors are now more talkative - gpg.py  + commented assert which
broke otherwise working verify run. [edso]

* Add a couple more warning codes for machine consumption of warnings. [Michael Terry]

* Allow answering gio mount questions (albeit naively) [Michael Terry]

* Add missing files. [edso]

* Readd ssh pexpect backend as alternative - added --ssh-backend
parameter to switch between paramiko,pexpect - manpage -- update to
reflect above changes -- added more backend requirements -
Changelog.GNU removed double entries. [edso]

* Update Changelog.GNU. [Kenneth Loafman]

* Changelog entry. [edso]

* Add missing\_host\_key prompt similar to ssh procedure. [edso]

* Fixing most basic stuff. Pending all testing. [Carlos Abalde]

* Changelog entry. [edso]

* Add ssh\_config support (/etc/ssh/ssh\_config + \~/.ssh/config) to
paramiko sshbackend. [edso]

* Empty listbody for enhanced webdav compatibility - bugfix: initial
folder creation on backend does not result in a ResponseNotReady
anymore. [edso]

* Added REQUIREMENTS section - restructure SYNOPSIS/ACTIONS to have
commands sorted by backup lifecycle - added restore and some more
hints when --time or --file-to-restore are supported - replaced scp://
with sftp:// in examples as this is the suggested protocol anyway -
added an intro text to ACTIONS section - adapted --ssh-askpass
description to latest functionality. [edso]

* Changes for 0.6.18. [kenneth@loafman.com]

* Use correct dir name for cleanup. [kenneth@loafman.com]

* Adjust roottest.py to new test dir structure. [kenneth@loafman.com]

* Changes for 0.6.18. [kenneth@loafman.com]

* Some code/import changes to make the ssh and boto backends compatible
with Python 2.4. [kenneth@loafman.com]

* Changes for 0.6.18. [kenneth@loafman.com]

* Changes for 0.6.18. [kenneth@loafman.com]

* Fix for bug 931175 'duplicity crashes when PYTHONOPTIMIZE is set' [kenneth@loafman.com]

* Remove duplicate line. [kenneth@loafman.com]

* File /etc/motd may not exist in test environment.  Use \_\_file\_\_
instead to point to a known plaintext source file. [kenneth@loafman.com]

* Remove tests for 884371.  Can't test that yet. [kenneth@loafman.com]

* Raise log level on backend import failure so it will be visible under
default conditions. [kenneth@loafman.com]

* Fix for bug 929465 -- UnsupportedBackendScheme: scheme not supported
in url: scp://u123@u123.example.com/foo/ [kenneth@loafman.com]

* Applied patch from 930727. [kenneth@loafman.com]

    ftpsbackend should respect num_retries for ftp commands

* Drop unused pexpect.py. [Michael Terry]

* A couple small code fixes to help tests pass. [Michael Terry]

* Applied patch by Alexander Zangerl from bug 909031, "SSH-Backend:
Creating dirs separately causes a permissons-problems". [Kenneth Loafman]

* Change the way the file\_naming regular expressions are created to
support --file-prefix option. [nguyenqmai]

* Don't have TarFile objects cache member TarInfo objects; it takes too
much space. [Michael Terry]

* Always delay a little bit when a backend gives us errors. [Michael Terry]

* Changelog update - fixed comment. [Tobias Genannt]

* Added option to not compress the backup, when no encryption is
selected. [Tobias Genannt]

* Added patch for testing of bug 884371, 'Globbing patterns fail to
include some files if prefix is "**"' [kenneth@loafman.com]

* Applied patch from 916689 "multipart upload fails on python 2.7.2" [kenneth@loafman.com]

* Applied patch from 884638 and fixed version check to allow Python 2.5
and above. [kenneth@loafman.com]

* Resuming an incremental results in a 'Restarting backup, but current
encryption settings do not match original settings' error because
curtime is incorrectly set away from previous incremental value. [Michael Terry]

* Tests: make other-filesystem check more robust against certain
directories being mounts or not. [Michael Terry]

* Tests: use backup source that is more likely to be larger than 1M
compressed. [Michael Terry]

* Tests: add delay between backups to avoid assertion error. [Michael Terry]

* Fix extraneous '.py' that keeps import from working. [Kenneth Loafman]

* Changes for 0.6.17. [Kenneth Loafman]

* Not used. [Kenneth Loafman]

* Run tests using virtualenv for each. [Kenneth Loafman]

* Make adjustments for the new structure. - Adjust boto requirements to
be 1.6a or higher. - Cleanup install scripts. [Kenneth Loafman]

* Some doc changes including new requirements. [Kenneth Loafman]

* Don't assume dir location for Python. [Kenneth Loafman]

* Adds --rsync-options to command line Allows uer to pass additional
options to the rsync backend Commit include paragraph in man page, new
global variable, and the small changes needed to the backend itself. [Eliot Moss]

* Check that we have the right passphrase when restarting a backup. [Michael Terry]

* 411145  Misleading error message: "Invalid SSH password" [Kenneth Loafman]

* Split botobackend.py into two parts, \_boto\_single.py which is the
older single-processing version and \_boto\_multi.py which is the
newer multi-processing version.  The default is single processing and
can be overridden with --s3-use-multiprocessing. [Kenneth Loafman]

* The function add\_filename was rejecting anything non-encrypted as a
legit file.  This fixes that problem and the bug. [Kenneth Loafman]

* Fix to allow debugging from pydev.  The check for --pydevd must be
done after command line is parsed. [Kenneth Loafman]

* Changed functions working with UTC time file format from localtime()
to gmtime() and timegm() [Ivan Gromov]

* Fixed time\_separator global attribute usage in some tests. [ivan.gromov]

* Made proper setUp method for tests in dup\_timetest.py. [Ivan Gromov]

* Remove random\_seed from VCS, adjust .bzrignore. [Kenneth Loafman]

* Remove localbackend.testing\_in\_progress since all it accomplished
was to make the local backend test fail. [ken]

* Make tarball layout match bzr layout much more closely; ship tests in
tarballs and adjust things so that they can work. [Michael Terry]

* Rename auto/ to tests/ [Michael Terry]

* Undo accidental changes to run-tests and convert pathtest and
rdiffdirtest (for both of which, I uncommented a failing test I didn't
understand) [Michael Terry]

* Move some more custom scripts to manual/ [Michael Terry]

* Move some things around; converge on one script for running any kind
of test or list of tests. [Michael Terry]

* Convert patchdirtest to auto; rip out its root-requiring tests and
move them to roottest script; fix roottest script to work now with the
new rootfiles.tar.gz, whoops. [Michael Terry]

* Convert finaltest to auto; workaround an ecryptfs bug with long
filenames in the test. [Michael Terry]

* Drop state file random\_seed from test gnupg home. [Michael Terry]

* Convert gpgtest to auto; add testing keys to the suite, so testers
don't have to make their own; delete gpgtest2, as it didn't do
anything. [Michael Terry]

* Drop unused darwin tarball and util file. [Michael Terry]

* Convert GnuPGInterfacetest and dup\_timetest to auto. [Michael Terry]

* Convert file\_namingtest, parsedurltest, and restarttest to auto. [Michael Terry]

* Convert manifesttest, selectiontest, and test\_tarfile to auto. [Michael Terry]

* Convert cleanuptest, dup\_temptest, and misctest to auto. [Michael Terry]

* Convert statisticstest to auto; make sure tests are run in English and
in US/Central timezone. [Michael Terry]

* Convert statictest to auto. [Michael Terry]

* Convert tempdirtest to auto. [Michael Terry]

* Convert logtest to auto. [Michael Terry]

* Convert lazytest to auto. [Michael Terry]

* Clean up run scripts a little bit, rename testfiles.tgz to
rootfiles.tgz. [Michael Terry]

* Make diffdirtest auto. [Michael Terry]

* Make badupload auto. [Michael Terry]

* Make collectionstest auto. [Michael Terry]

* Move all manual tets into their own subdirectory. [Michael Terry]

* -- Applied patch 0616.diff from bug 881070. -- Fixed compile issues in
reset\_connection. -- Changed 'url' to 'parsed\_url' to make
consistent with backends. [ken]

* Changes for 0.6.16. [ken]

* Changes for 0.6.16. [ken]

* Merge in lp:\~duplicity-team/duplicity/po-updates. [Kenneth Loafman]

* Remove Eclipse stuff from bzr. [Kenneth Loafman]

* Update .pot and add all languages to LINGUAS list file. [kenneth@loafman.com]

* Some links for UnicodeDecodeError. [edso]

* Fix UnicodeDecodeError: 'ascii' codec can't decode byte on command
usage. [edso]

* Remove evil tab characters causing indent errors. [kenneth@loafman.com]

* 838162  Duplicity URL Parser is not parsing IPv6 properly. [kenneth@loafman.com]

* 676109 Amazon S3 backend multipart upload support. [kenneth@loafman.com]

* 739438 Local backend should always try renaming instead of copying. [kenneth@loafman.com]

* Updated --verbosity symmetric and signing. [edso]

    minor fixes

* Checkpoint. [kenneth@loafman.com]

* Make sure sig\_path is a regular file before opening it. [Michael Terry]

* Gpg2 will not get the passphrase from gpg-agent if --passphrase-fd is
specified. Added tests to disable passphrase FD if use\_agent option
is true. [Ross Williams]

* Use cached size of original upload file rather than grabbing it after
put() call.  Some backends invalidate the stat information after put
(like local backend after a rename) [Michael Terry]

* Allow upgrading partial chain encryption status. [Michael Terry]

* Make tarfile.py 2.4-compatible. [Michael Terry]

* Use python2.7's tarfile instead of whichever version comes with user's
python. [Michael Terry]

* Use a proper fake TarFile object when reading an empty tar. [Michael Terry]

* Handle empty headers better than passing ignore\_zeros -- instead
handle ReadErrors. [Michael Terry]

* And update trailing slashes in test too. [Michael Terry]

* Fix how trailing slashes are used to be cross-python-version
compatible. [Michael Terry]

* Whoops, forgot an import. [Michael Terry]

* Handle different versions of tarfile. [Michael Terry]

* First pass at dropping tarfile. [Michael Terry]

* Make query\_info a little easier to use by guaranteeing a well-
formated return dictionary. [Michael Terry]

* Add rackspace query support. [Michael Terry]

* Add query support to boto backend. [Michael Terry]

* Make clear the difference between sizes from errors and backends that
don't support querying. [Michael Terry]

* Add query\_info support to u1 backend. [Michael Terry]

* First pass at checking volume upload success. [Michael Terry]

* Cloudfiles: allow listing more than 10k files. [Michael Terry]

* Drop sign passphrase verification prompt. [edso]

* Bugfix of rev767 on using sign key duplicity claimed 'PASSPHRASE
variable not set' [edso]

* Sync with master. [Kenneth Loafman]

* Remove another non-2.4-ism I introduced. [Michael Terry]

* Changes for 0.6.15. [Kenneth Loafman]

* Fixes to unit tests to support SIGN\_PASSPHRASE. [Kenneth Loafman]

* Typo fix. [edso]

* Numowner & hash mismatch verbosity. [edso]

* Remove use of virtualenv. [Kenneth Loafman]

* Ignore ENOENT (file missing) errors where it is safe. - Set minimum
Python version to 2.4 in README. [Kenneth Loafman]

* 824678     0.6.14 Fails to install on 8.04 LTS (Hardy) [Kenneth Loafman]

* 823556     sftp errors after rev 740 change. [Kenneth Loafman]

* Fixed indentation: 2 to 4 spaces. [Carlos Abalde]

* Fetching user password correctly (i.e. not using directly
self.parsed\_url.password) [Carlos Abalde]

* Now using backend.retry(fn) decorator to handle API retries. [Carlos Abalde]

* Added subfolders support + several minor improvements and fixes. [Carlos Abalde]

* Added support for captcha challenges. [Carlos Abalde]

* Replacing get\_doclist by get\_everything in put & delete methods.
Raisng BackendException's in constructor. [Carlos Abalde]

* Replaces get\_doclist by get\_everything when retrieving remote list
of files in backup destination folder. [Carlos Abalde]

* Added authentication instruction for accounts with 2-step verification
enabled. [Carlos Abalde]

* A couple of assert + missing local\_path.setdata on remote file get. [Carlos Abalde]

* Better error logging + retries for each API op. [Carlos Abalde]

* Improved upload: check duplicated file names on destination folder +
better error handling. [Carlos Abalde]

* Improved API error handling. [Carlos Abalde]

* Checking Google Data APIs Python libraries are present. [Carlos Abalde]

* Fixed URI format. [Carlos Abalde]

* First usable prototype. [Carlos Abalde]

* Some u1 backend fixes: handle errors 507 and 503; add oops-id to
message user sees so U1 folks can help. [Michael Terry]

* Merged in lp:\~ed.so/duplicity/encr-sign-key2. [Kenneth Loafman]

* Introduce --encrypt-sign-key parameter  - duplicity-
bin::get\_passphrase          skip passphrase asking and reuse
passphrase if          sign-key is also an encrypt key and     a
passphrase for either one is already set    - add \_() gettext to text
in duplicity-bin::get\_passphrase    - document changes and minor
additions in manpage. [ede]

* Don't try to delete partial manifests from backends. [Michael Terry]

* Retry operations on u1 backend. [Michael Terry]

* When copying metadata from remote to local archive, first copy to a
temporary file then move over to archive. [Michael Terry]

* Report whether a chain is encrypted or not. [Michael Terry]

* Be more careful about what we try to synchronize. [Michael Terry]

* Pay attention to local partials when sync'ing metadata and make sure
we don't end up with three copies of a metadata file. [Michael Terry]

* Ignore ENOTCONN when scanning files. [Michael Terry]

* Really restore threaded\_waitpid(). [Kenneth Loafman]

* Also guard the recursive call. [Michael Terry]

* Guard tarinfo object from being None. [Michael Terry]

* Detabify.  Tabs are evil. [Kenneth Loafman]

* Restore previous version with threaded\_waitpid(). [Kenneth Loafman]

* U1backend: ignore file-not-found errors on delete. [Michael Terry]

* Update to duplicity messages. [Kenneth Loafman]

* 777377     collection-status asking for passphrase. [Kenneth Loafman]

    Various fixes to unit tests to comprehend changes made.

* Duplicity.1: move information about the PASSPHRASE and
SIGN\_PASSPHRASE   environment variables to the Environment Variables
section - duplicity.1: add information about the limitation on using
symmetric+sign to the bugs section - In the passphrase retrieval
function get\_passphrase, do not switch from   "ask password without
verifying" to ask+verify if the passphrase was   empty - Allow an
empty passphrase for signing key - Make clear in the verification
prompt whether the encryption passphrase   or the signing passphrase
is being confirmed - Fix passphrase retrieval for sym+sign (duplicity-
bin and gpg.py) - Allow sym+sign with limitation (see comments and
manual page) [Lekensteyn]

* Invalid function description fixed for get\_passphrase in duplicity-
bin - function get\_passphrase in duplicity-bin accepts argument
"for\_signing"   which indicates that a passphrase for a signing key
is requested - introduces the SIGN\_PASSPHRASE environment variable
for passing a   different passphrase to the signing key - commandline
option --encrypt-secret-keyring=path introduced to set a   custom
location for the secret keyring used by the encryption key - manual
page updated with SIGN\_PASSPHRASE and --encrypt-secret-keyring - ask
for a new passphrase if the passphrase confirmation failed to
prevent an endless retype - improved some comments in the code - due
to the difference in the handling of the signing and encryption
passphrase, the passphrase is asked later in the duplicity-bin. [Lekensteyn]

* Always catch Exceptions, not BaseExceptions. [Michael Terry]

* Checkpoint. [Kenneth Loafman]

* 794123     Timeout on sftp command 'ls -1' [Kenneth Loafman]

* Checkpoint. [Kenneth Loafman]

* 487720     Restore fails with "Invalid data - SHA1 hash mismatch" [Kenneth Loafman]

* Fixed boolean swap made when correcting syntax. [Kenneth Loafman]

* Fix syntax for Python 2.4 and 2.5. [Kenneth Loafman]

* Fix syntax for Python 2.4 and 2.5. [Kenneth Loafman]

* Fix CHANGELOG. [Kenneth Loafman]

* 782337     sftp backend cannot create new subdirs on new backup. [Kenneth Loafman]

* 782294     create tomporary files with sftp. [Kenneth Loafman]

* Move logging code up to retry decorator; fixes use of 'n' variable
where it doesn't belong. [Michael Terry]

* Add retry decorator for backend functions; use it for giobackend; add
retry to giobackend's list and delete operations. [Michael Terry]

* U1: allow any success status, not just 200. [Michael Terry]

* Checkpoint. [Kenneth Loafman]

* Giobackend: use name, not display name to list files. [Michael Terry]

* Fix MachineFilter logic to match new level name code. [Michael Terry]

* Cautiously avoid using levelname directly in log module.  It can be
adjusted by libraries. [Michael Terry]

* Update man page. [Michael Terry]

* Drop test file. [Michael Terry]

* Further fixups. [Michael Terry]

* Further upload work. [Michael Terry]

* Start of u1 support. [Michael Terry]

* 792704     Webdav(s) url scheme lacks port support. [Kenneth Loafman]

* 782321     duplicity sftp backend should ignore removing a file which
is not there. [Kenneth Loafman]

* 778215     ncftpls file delete fails in ftpbackend.py. [Kenneth Loafman]

* 507904     Cygwin: Full Backup fails with "IOError: [Errno 13]
Permission denied" [Kenneth Loafman]

* 761688     Difference found: File X has permissions 666, expected 666. [Kenneth Loafman]

* 739438     [PATCH] Local backend should always try renaming instead of
copying. [Kenneth Loafman]

* 705499     "include-filelist-stdin" not implemented on version 0.6.11. [Kenneth Loafman]

* As restoring is non-destructive by default (overideable with --force)
there is no need to raie fata errors if not supported in/exclude
parameters are given as parameters. see also:
http://lists.gnu.org/archive/html/duplicity-talk/2011-04/msg00010.html. [ed]

* 512628     --exclude-filelist-stdin and gpg error with/without
PASSPHRASE. [Kenneth Loafman]

* 512628     --exclude-filelist-stdin and gpg error with/without
PASSPHRASE. [Kenneth Loafman]

* Insure Python 2.4 compatible. [Kenneth Loafman]

* 433591  AttributeError: FileobjHooked instance has no attribute 'name' [Kenneth Loafman]

* Link sftp to ssh backend, thus enabling sftp:// urls modified
explanation in manpage minor changes in manpage. [ed]

* Boto has refactored too many times, so back off and just use Exception
rather than searching. [Kenneth Loafman]

* Boto moved S3ResponseError, so allow for different imports. [Kenneth Loafman]

* Changes for 0.6.13. [Kenneth Loafman]

* Changes for 0.6.13. [Kenneth Loafman]

* Changes for 0.6.13. [Kenneth Loafman]

* Check for presence of bucket before trying to create. [Kenneth Loafman]

* 579958  Assertion error "time not moving forward at appropriate pace" [Kenneth Loafman]

* Add in ftpsbackend.py.  Missed it. [Kenneth Loafman]

* 613244     silent data corruption with checkpoint/restore. [Kenneth Loafman]

* Add a manual test for Ctrl-C interrupts.  This could be automated, but
I find that the old hairy eyeball works quite well as is. [Kenneth Loafman]

* Use python-virtualenv to provide a well-defined environment for
testing multiple versions of Python. [Kenneth Loafman]

* Add (undocumented) option --pydevd to allow easier debugging when
executing long chains of duplicity executions. [Kenneth Loafman]

* Remove threaded\_waitpid().  We still need GnuPGInterface because of
the shift bug in the return code and the ugly mix of tabs and spaces.
All has been reported to the author. [Kenneth Loafman]

* Replace 2.5 'except...as' syntax. [Kenneth Loafman]

* Changes for 0.6.12. [Kenneth Loafman]

* Various fixes for testing.  All tests pass completely. [Kenneth Loafman]

* Add test for new ftps backend using lftp. [Kenneth Loafman]

* Some FTP sites return 'total NN' in true ls fashion, so ignore line
during listing of files. [Kenneth Loafman]

* Fix typo on fix for 700390. [Kenneth Loafman]

* Miscellaneous fixes for testing. [Kenneth Loafman]

* 700390  Backup fails silently when target is full (sftp, verbosity=4) [Kenneth Loafman]

* 581054  Inverted "Current directory" "Previous directory" in error
message. [Kenneth Loafman]

* 626915     ftps support using lftp (ftpsbackend) [Kenneth Loafman]

* 629984  boto backend uses Python 2.5 conditional. [Kenneth Loafman]

* 670891  Cygwin: TypeError: basis\_file must be a (true) file, while
restoring inremental backup. [Kenneth Loafman]

* 655797     symbolic link ownership not preserved. [Kenneth Loafman]

* Lp:\~blueyed/duplicity/path-enodev-bugfix. [Kenneth Loafman]

* Merged: lp:\~blueyed/duplicity/path-enodev-bugfix. [Kenneth Loafman]

* 629136     sslerror: The read operation timed out with cf. [Kenneth Loafman]

* 704314     Exception in log module. [Kenneth Loafman]

* 486489  Only full backups done on webdav. [Kenneth Loafman]

* 620163  OSError: [Errno 2] No such file or directory. [Kenneth Loafman]

* Use log error codes for common backend errors. [Michael Terry]

* 681980     Duplicity 0.6.11 aborts if RSYNC\_RSH not set. [Kenneth Loafman]

* Changes for 0.6.11. [Kenneth Loafman]

* Changes for 0.6.11. [Kenneth Loafman]

* Add --s3-unencrypted-connection (bug 433970) [Martin Pool]

* Solve bug 631275 rsync 3.0.7 persists on either rsync:// \_or\_ ::
module notation both together and it interpretes it as a dest for rsh. [ed]

* Protect rsync from possibly conflicting remote shell environment
setting. [ed]

* Restored backend:subprocess\_popen\_* methods moved ncftpls workaround
into ftpbackend introduced new backend:popen\_persist\_breaks setting
for such workarounds enhanced backend:munge\_password rsyncbackend:
rsync over ssh does not ask for password (only keyauth supported) [ed]

* Survive spaces in path on local copying with encryption enabled. [ed]

* Allow signing of symmetric encryption. [ed]

* Catch "Couldn't delete file" response in sftp commands. [Daniel Hahler]

* When using listmatch filenames are now unqouted so colons and other
special characters don't cause problems. [Tomaž Muraus]

    Also all the tests now pass.

* Added test for SpiderOak backend (it should probably just fail in most
cases since the API is still very unstable). [Tomaž Muraus]

* Add ability to retry failed commands. [Tomaž Muraus]

* Handle exceptions when listing files and display coresponding HTTP
status code on HTTPError exception. [Tomaž Muraus]

* First version of SpiderOak DIY backend. [Tomaž Muraus]

    Still very rough and needs tests.

* Support new backend-error log codes. [Michael Terry]

* Adding conftest.py for py.test configuration hooks (right now just
setting up temporary directories) [Larry Gilbert]

* Use py.path to simplify a little. [Larry Gilbert]

* Don't try to change dirs in cleanup\_test\_files for now. Actually,
this file probably won't be here much longer. [Larry Gilbert]

* Fix non-root-based test skipping. [Larry Gilbert]

* Expose test files' root directory as config.test\_root. [Larry Gilbert]

* New helper module for tests; have backendtest.py make use of it. [Larry Gilbert]

* Refactored.  Put in py.test.skip to skip tests when tarfile can't be
used. [Larry Gilbert]

* Commit.py already adjusts sys.path, so anything that imports commit
doesn't need to. [Larry Gilbert]

* Allow testing/config.py to find duplicity even when run outside
testing/. Added a missing import. [Larry Gilbert]

* 637556     os.execve should get passed program as first argument. [Kenneth Loafman]

* Changes for 0.6.10. [Kenneth Loafman]

* Replace ternary operator with simple if statement.  Python 2.4 does
not support the ternary operator. [Kenneth Loafman]

* Upgrade setup dependency to Python 2.4 or later. [Kenneth Loafman]

* Changes for 0.6.10. [Kenneth Loafman]

* 612714     NameError: global name 'parsed\_url' is not defined. [Kenneth Loafman]

* 589495     duplicity --short-filenames crashes with TypeError. [Kenneth Loafman]

* 589495     duplicity --short-filenames crashes with TypeError. [Kenneth Loafman]

* Fix remove-older-than which would no longer work Differentiate the
function name from global option name for remove\_all\_but\_n\_full. [olivier]

* Added bits of manpage. [olivier]

* Adding the remove-all-inc-of-but-n-full variant to
remove\_all\_but\_n\_full() : remove only incremental sets from a
backup chain selected as older than the n last full. [olivier]

* Adding the 2 new remove-all-but commands as global markers. [olivier]

* Adding new remove-all-inc-of-but-n-full command as a variant of
remove-all-but-n-full. [olivier]

* Fix small typo in comments. [olivier]

* 613448     ftpbackend fails if target directory doesn't exist. [Kenneth Loafman]

* 615449     Command-line verbosity parsing crash. [Kenneth Loafman]

* Man page improvements and clarification. [Kenneth Loafman]

* Final changes for 0.6.09. [Kenneth Loafman]

* 582962     Diminishing performance on large files. [Kenneth Loafman]

* Fix to warning message in sshbackend. [Kenneth Loafman]

* Upgraded tahoebackend to new parse\_url. [Kenneth Loafman]

* Merged in lp:\~duplicity-team/duplicity/po-updates. [Kenneth Loafman]

* 502609     Unknown error while uploading duplicity-full-signatures. [Kenneth Loafman]

* Support new backend-error log codes. [Michael Terry]

* Don't crash when asked to encrypt, but not passed any gpg\_options.
my bad. [Michael Terry]

* #532051 rdiffdir attempts to reference undefined variables with some
command arguments. [Kenneth Loafman]

* #519110 Need accurate man page info on use of scp/sftp usage. [Kenneth Loafman]

* Use global gpg options. [Michael Terry]

* Fix time command line handling. [Michael Terry]

* And handle initial, empty value for extend commandline actions. [Michael Terry]

* Fix crash on empty gpg-options argument. [Michael Terry]

* #520470 - Don't Warn when there's old backup to delete. [ken]

* Patch #505739 - "sslerror: The read operation timed out" with S3. [ken]

* Patch 522544 -- OSError: [Errno 40] Too many levels of symbolic links. [ken]

* Patched #497243 archive dir: cache desynchronization caused by remove* [ken]

* Logging: fix logging to files by opening them with default of 'a' not
'w' [Michael Terry]

* Merge lp:\~mterry/duplicity/rename. [Michael Terry]

* Make a comment reserving 255 as an error code (used by gksu) [Michael Terry]

* Merge lp:\~mterry/duplicity/optparse. [Michael Terry]

* Remove antiquated file. [ken]

* Remove requirement for GnuPGInterface, we have our own. [ken]

* 576564     username not url decoded in backend (at least rsync) [ken]

* 579958     Assertion error "time not moving forward at appropriate
pace" [Kenneth Loafman]

    setcurtime() must change with time changes.

* 550455           duplicity doesn't handle with large files well
(change librsync.SigGenerator.sig\_string to a list) [ken]

* Changes for 0.6.08b. [Kenneth Loafman]

* Manually apply patch from http://bazaar.launchpad.net/\~duplicity-
team/duplicity/0.7-series/revision/637 which did not make it into 0.6. [Kenneth Loafman]

* Changes for 0.6.08a. [Kenneth Loafman]

* Changes for 0.6.08. [Kenneth Loafman]

* #532051 rdiffdir attempts to reference undefined variables with some
command arguments. [Kenneth Loafman]

* #519110 Need accurate man page info on use of scp/sftp usage. [Kenneth Loafman]

* Use global gpg options. [Michael Terry]

* Fix time command line handling. [Michael Terry]

* And handle initial, empty value for extend commandline actions. [Michael Terry]

* Fix crash on empty gpg-options argument. [Michael Terry]

* Changes for 0.6.07. [ken]

* #520470 - Don't Warn when there's old backup to delete. [ken]

* Patch #505739 - "sslerror: The read operation timed out" with S3. [ken]

* Patch 522544 -- OSError: [Errno 40] Too many levels of symbolic links. [ken]

* Patched #497243 archive dir: cache desynchronization caused by remove* [ken]

* Logging: fix logging to files by opening them with default of 'a' not
'w' [Michael Terry]

* Make a comment reserving 255 as an error code (used by gksu) [Michael Terry]

* Patch 501093 SSHBackend doesn't handle spaces in path. [ken]

* Try again -- remove Eclipse/PyDev control files from bzr. [ken]

* Eclipse settings should not be in bzr. [ken]

* No longer needed. [ken]

* Fix real errors found by PyLint.  Remove unneeded includes.  Tag
spurious errors so they don't annoy. [ken]

* Fix problem in put() where destination filename was not being passed
properly. [ken]

* Add --rename argument. [Michael Terry]

* Add back accidentally-dropped --use-scp option from commandline merge. [Michael Terry]

* Fix CHANGELOG. [ken]

* Merged in lp:\~mterry/duplicity/typos. [ken]

* Whoops, and this typo. [Michael Terry]

* Fix some typos found when using pydev+eclipse. [Michael Terry]

* 459511 --tempdir option doesn't override TMPDIR. [ken]

* 487686 re-add scp backend and make available via command line option
Option --use-scp will use scp, not sftp, for get/put operations. [ken]

* Applied patch 467391 to close connection on a 401 and retry with
authentication credentials. [ken]

* CVS no longer used, so no longer needed. [ken]

* Checkpoint. [Kenneth Loafman]

* I18nized a few error messages in duplicity.selection. [Larry Gilbert]

* More strings internationalized in asyncscheduler and commandline. [Larry Gilbert]

* Warn if we don't have signatures for the given date period. [Michael Terry]

* Allow deleting old signatures with cleanup --extra-clean. [Michael Terry]

* Don't delete signature chains for old backups; allow listing old
backup chain files. [Michael Terry]

* Add missing par2\_utils.py to dist tarball. [Michael Terry]

* Remove unused \_\_future\_\_ imports. [Kenneth Loafman]

* Add entry for patches from Stéphane Lesimple for par2. [Kenneth Loafman]

* Applied patch from Stéphane Lesimple found at:
https://bugs.launchpad.net/duplicity/+bug/426282/comments/5 patch
skips the par2 files when building up the sets and chains of backups. [Kenneth Loafman]

* Applied patch from Stéphane Lesimple found at:
https://bugs.launchpad.net/duplicity/+bug/426282/comments/4 patch
avoids storing all the par2 files into the local cache. [Kenneth Loafman]

* Fixed 435975 gpg asks for password in 0.6.05, but not in 0.5.18. [Kenneth Loafman]

* Ugh, I'm the worst; add missing import. [Michael Terry]

* Add extra information to the 'hostname changed' log message, split it
from the 'source dir changed' message. [Michael Terry]

* Modify file name test to test short filenames even when not
specifically requested to. [Michael Terry]

* Accept short filenames even if not specifically requested. [Michael Terry]

* Fix problems with unittests under Jaunty.  It appears that redirection
in os.system() has changed for the worse, so a workaround for now. [Kenneth Loafman]

    Fix problem in restart where there were no manifest entries and no
    remote volumes stored.  We clean out the partial and restart.

* Applied "426282 [PATCH] par2 creating support", corrected some coding
format issues and made sure all unit tests passed. [Kenneth Loafman]

* Clean up testing run scripts. [Kenneth Loafman]

* * 422477 [PATCH] IMAP Backend Error in delete() [Kenneth Loafman]

* Whoops, remove debug code. [Michael Terry]

* Don't set xdg dirs in duplicity-bin now that globals.py is restored. [Michael Terry]

* Use defaults from globals.py for commandline options. [Michael Terry]

* Fix an undefined variable usage. [Michael Terry]

* Fix a few typos. [Michael Terry]

* Whoops, and this typo. [Michael Terry]

* Fix some typos found when using pydev+eclipse (backported from 0.7
line) [Michael Terry]

* Fix typo with log-fd support. [Michael Terry]

* First pass at getopt->optparse conversion. [Michael Terry]

* Remove antiquated file. [ken]

* Remove requirement for GnuPGInterface, we have our own. [ken]

* 459511 --tempdir option doesn't override TMPDIR. [ken]

* 487686 re-add scp backend and make available via command line option
Option --use-scp will use scp, not sftp, for get/put operations. [ken]

* Applied patch 467391 to close connection on a 401 and retry with
authentication credentials. [ken]

* Checkpoint. [Kenneth Loafman]

* Changes for 0.6.06. [Kenneth Loafman]

* Merge old-chain signature work from 0.7 branch; keep old sigs around,
allow listing them, warn if a too-old listing is requested. [Michael Terry]

* Remove .cvsignore. [kenneth@loafman.com]

* Remove unused \_\_future\_\_ imports. [Kenneth Loafman]

* Fixed 435975 gpg asks for password in 0.6.05, but not in 0.5.18. [Kenneth Loafman]

* Ugh, I'm the worst; add missing import. [Michael Terry]

* Whoops, use error code 42, not 41 -- that's for par2. [Michael Terry]

* Add extra information to the 'hostname changed' log message, split it
from the 'source dir changed' message. [Michael Terry]

* Fix problems with unittests under Jaunty.  It appears that redirection
in os.system() has changed for the worse, so a workaround for now. [Kenneth Loafman]

    Fix problem in restart where there were no manifest entries and no
    remote volumes stored.  We clean out the partial and restart.

* Add some machine codes to various warnings when iterating over source
files. [Michael Terry]

* Additional Portuguese and brand-new Bulgarian translations. [Larry Gilbert]

* Clean up testing run scripts. [Kenneth Loafman]

* * 422477  [PATCH] IMAP Backend Error in delete() [Kenneth Loafman]

* Change message "--cleanup option" to "'cleanup' command" [Larry Gilbert]

* Translation of Spanish and Portuguese has begun. [Larry Gilbert]

* Updated existing PO files with Rosetta translations. [Larry Gilbert]

* When generating PO[T] files, only use code comments starting with
"TRANSL:" for notes to the translators.  "TRANSL:" is filtered out of
the POT file with sed after it's generated. [Larry Gilbert]

* Applied patches from Kasper Brand that fixed device file handling.
http://lists.gnu.org/archive/html/duplicity-talk/2009-09/msg00001.html. [Kenneth Loafman]

* Changes for 0.6.05. [Kenneth Loafman]

* Test separate filesystems using /dev instead of /proc (more widely
used) [Larry Gilbert]

* Dd on Darwin (and FreeBSD?) doesn't like e.g. "bs=1K", so changed it
to "bs=1024" [Larry Gilbert]

* "cp -pR" seems to be a better analogue to "cp -a".  This may not be
perfect but it won't hang on a fifo copy like "cp -pr". [Larry Gilbert]

* Got test\_get\_extraneous working in collectionstests.py. [Larry Gilbert]

* Unpacked testfiles.tar.gz on Mac OS X file system and repacked as new
file. [Larry Gilbert]

* Changed options to 'cp' to be compatible with BSD style yet
(hopefully) stay compatible with GNU. [Larry Gilbert]

* Took care of some redundancy in tar usage. [Larry Gilbert]

* Use bash "command" command to look for Python binaries beyond /usr/bin. [Larry Gilbert]

* 418170  [PATCH] file names longer then 512 symbols are not supported. [Kenneth Loafman]

* 408059  Failure due to \_logger.log failure for content with special
characters: TypeError decoding Unicode not supported. [Kenneth Loafman]

* "remove-older-than" asks for passphrase even though not required;
watch for correct internal action name to fix this. [Larry Gilbert]

* Typo in remove-older-than may have caused unnecessary passphrase
prompts? [Larry Gilbert]

* Changes for 0.5.19. [Kenneth Loafman]

* Fix getrlimit usage for Cygwin, which was returning -1 for the hard
limit on max open files. [Kenneth Loafman]

* Ignore unicode() translation errors in log messsages. [Kenneth Loafman]

* Make sure 'invalid packet (ctb=14)' from gpg is not a fatal error. [Kenneth Loafman]

* On processes that complete before waitpid(), log them and return zero
as the process.returned value.  They will have already trapped in the
main thread if they returned in error. [Kenneth Loafman]

* Copy changes from trunk for duplicity translation. [Kenneth Loafman]

* Comment out Pydev debug startup code. [Kenneth Loafman]

* Typo in "remove-older-than" may have caused unnecessary passphrase
prompts? [Larry Gilbert]

* Fixed #409593 deja-dup (or duplicity) deletes all signatures. [Kenneth Loafman]

* Allow gio backend to restore by setting correct state.  LP: #407968. [Michael Terry]

* Changes for 0.6.04. [Kenneth Loafman]

* Changes for 0.6.04. [Kenneth Loafman]

* Fixed 405734 duplicity fails to restore files that contain a newline
character. [Kenneth Loafman]

* Fixed 403790 Backup error: No such file or directory. [Kenneth Loafman]

* Last changes for 0.6.03. [Kenneth Loafman]

* Changes for 0.6.03. [Kenneth Loafman]

* Changes for 0.6.03. [Kenneth Loafman]

* Fixed 402794 duplicity public-key-only incompatible with gnupg 2.0.11. [Kenneth Loafman]

* Fixed 405975 duplicity.gpg.gpg\_failed() breaks and spews on GnuPG
error. [Kenneth Loafman]

* Fixed 398230 Deja-dup backup fails with message: "Unable to locate
last file" [Kenneth Loafman]

* Oops, one too many things in usage() were dictionarified. [Larry Gilbert]

* Minor header comment correction. [Kenneth Loafman]

* Adjust to file renames. [Kenneth Loafman]

* Sorry... I missed the point being made here... [Larry Gilbert]

* Minor capitalization changes in the manpage. [Larry Gilbert]

* CVS-README changed to REPO-README and updated with Launchpad/bzr info. [Larry Gilbert]

* Redid dictionary in usage to use a local hash instead of a bunch of
local variables, to make things a tad more pleasant. [Larry Gilbert]

* Broke up the usage() help info to simplify translation maintenance.
Imported .po files from Launchpad Translation (not sure how necessary
they are to have in here, but here they are.) [Larry Gilbert]

* Updated some intltool config info. [Larry Gilbert]

* Updated *.po and *.pot files. [Larry Gilbert]

* Fix restart issues when local manifest does not agree with the
contents of the remote system.  In all cases, clean up as needed, and
restart the backup at the last known good state. [Kenneth Loafman]

* Refactor to put loop outside of try/except clause. [Kenneth Loafman]

* BackupSet.delete() now removes both local and remote files. [Kenneth Loafman]

* Make testing into a module. [Kenneth Loafman]

* Capture stderr as well as logger and display stderr with logger only
if gpg fails.  Cuts out some of the noise from gpg. [Kenneth Loafman]

* Split restarttest.py from finaltest.py for ease in debugging. [Kenneth Loafman]

* Fix test config to import backends (now optional). [Kenneth Loafman]

* S/pair/tuple/ (method doc fix) [Peter Schuller]

* When doing the "sleep to make sure we have different current time than
last backup":     - sleep for 2 seconds instead of 1, since it is an
expected case that time may be moving       slightly slower as a
result of adjtime() and such     - assert afterwards that current time
really does differ from previous time. [Peter Schuller]

* Update .bzrignore only. [Kenneth Loafman]

* Fixed 401303 0.6.2 manpage inconsistent wrt. archive-dir/name. [Kenneth Loafman]

* Fix 377528 --file-to-restore doesn't work with trailing slash. [Kenneth Loafman]

* First pass at bug 394757 - Optional Backends
https://bugs.launchpad.net/bugs/394757. [Kenneth Loafman]

* Ignore unicode() translation errors in log messsages. [Kenneth Loafman]

* Make sure 'invalid packet (ctb=14)' from gpg is not a fatal error. [Kenneth Loafman]

* On processes that complete before waitpid(), log them and return zero
as the process.returned value.  They will have already trapped in the
main thread if they returned in error. [Kenneth Loafman]

* Use correct name of error class ConflictingScheme. [Kenneth Loafman]

* Make Changelog.GNU close to GNU Changelog format. [Kenneth Loafman]

* Changes for 0.6.02. [Kenneth Loafman]

* Another attempt at fixing #394629 Hang on first collection-status. [Kenneth Loafman]

* Fix Bug #395826 "No such file or directory" when backing up second
time. [Kenneth Loafman]

* Optimistically try to resolve final issue by passing ParseResult:s
sense of what's what to   get\_suffix() rather than hard-coding based
on manifest. not sure if this has other bad side-effects   though -
will discuss on ML. [Peter Schuller]

* Nuke accidentally added characters in comments - left control is
breaking on my keyboard... [Peter Schuller]

* Initial stab (broken): synch both ways; i.e., remove spurious local
files in addition to downloading missing ones * problem remaining with
determining the correct local name. [Peter Schuller]

* Fix bug #394629 Hang on first collection-status. [Kenneth Loafman]

* Support an --ignore-errors command which is intended to mean "try to
continue in the face of" errors   that might possibly be okay to
ignore   - intended during restoration to avoid bailing out on errors
that are not fatal yet would in fact     produce an "incorrect"
restoration   - for now, only changes behavior on file meta data
restoration where I happened to have a problem     (I had a +t file
which was impossible to restore to +t even though it was possible for
it to     exist and for me to read it)   - be clear in the man page
that this is only supposed to be used in case of problems and even
then     to please contact maintainer if use is needed. [Peter Schuller]

* Print archive directory in a more readable fashion #394627. [Peter Schuller]

* Update ignore list. [Kenneth Loafman]

* Fixes: [Bug 379386] Fix 'list-current-files' with missing archive dir. [Kenneth Loafman]

* Fix po dir layout, update POTFILES.in, add pot file to bzr. [Michael Terry]

* Changes for 0.6.01. [Kenneth Loafman]

* Fixed issues in Checkpoint/Restart: * The --name backupname" option
was added to allow the   user to separate one archive from another.
If not   specified, the default is an MD5 hash of the target   URL,
which should suffice for most uses. [Kenneth Loafman]

    The archive_dir (cache) is now stored in a standard
      location, defaulting to ~/.cache/duplicity.  See
      http://standards.freedesktop.org/basedir-spec/latest/

    * The interaction between the --archive-dir option and
      the --name option allows for four possible results
      for the location of the archive dir.
        - neither specified (default)
          ~/.cache/duplicity/hash-of-url
        - --archive-dir=~/arch, no --name
          ~/arch/hash-of-url
        - no --archive-dir, --name=foo
          ~/.cache/duplicity/foo
        - --archive-dir=~/arch, --name=foo
          ~/arch/foo

    * duplicity will now copy needed metadata from the
      remote store to the local cache as needed.  This
      means that the first use after upgraded from 0.5.x
      will have the metadata copied to the local archive
      dir in order to sync both.

    * cleanup will now work correctly with the archive
      dir and separates the local from the remote files.

* Fixes bug 392905.  Allow omission of remote file name if the same as
the source file name. [Kenneth Loafman]

* Change to use XDG\_ convention per
http://standards.freedesktop.org/basedir-spec/latest/ [kenneth@loafman.com]

* Change handling of smart archive dir so both archive and name can be
changed. [kenneth@loafman.com]

* Fix "external file not found" to show command and file names. [kenneth@loafman.com]

* Actually distribute the gio backend. [Michael Terry]

* Avoid deprecation warning for md5 in Python 2.6. [kenneth@loafman.com]

* * --name affects *expansion*, not default value, of --archive-dir. [Peter Schuller]

* Fix a man page mistake from previous merge * remove last remnants of
DUPLICITY\_ARGS\_HASH. [Peter Schuller]

* Correct man page to claim hash of backend url rather than has of args. [Peter Schuller]

* Figure out which arg is a backend url without actually instantiating a
backend. [Peter Schuller]

* Make default value to --name be the has of the backend URL
specifically, rather than   the has of remaining args * outstanding
issue: in order to figure out which arg is a backend we call
get\_backend();   must either fix this or feel comfortable that
instantiating (and not using) a backend   is side-effect free. [Peter Schuller]

* Introduce --name parameter to specify symbolic name of a backup *
change --archive-dir expansion to look for %DUPLICITY\_BACKUP\_NAME% *
which in turn defaults to the args hash previously used for
--archive-dir and %DUPLICITY\_ARGS\_HASH% expansion. [Peter Schuller]

* Support expansion of %DUPLICITY\_ARGS\_HASH% in --archive-dir value *
default to \~/.duplicity/%DUPLICITY\_ARGS\_HASH$ so that default
behavior   works well even when the user has multiple backup
destinations * update the manpage accordingly. [Peter Schuller]

* Misc project changes. [kenneth@loafman.com]

* If python is run setuid, it's only partway set, so make sure to run
with euid/egid of root. [kenneth@loafman.com]

* Create testfiles/output in SetUp routine so it will run standalone. [kenneth@loafman.com]

* Surround --gio option with try/except so user will not see traceback. [kenneth@loafman.com]

* Make GIO tests dependent on presence of gio module. [kenneth@loafman.com]

* Fix 'get' command args. [kenneth@loafman.com]

* Initial attempt at using only sftp on the client
(https://savannah.nongnu.org/bugs/index.php?26464) [Colin Watson]

* S/self.\_\_waiter/self.\_\_failed\_waiter/ [Peter Schuller]

* Significantly re-design the asynch scheduler to be much simpler;
instead of keeping workers   and queues, simply launch a thread for
each unit of work, blocking when called for by   a concurrency limit
or a barrier. the old design was a result of initially designing for
keeping a persistent set of workers, only to then drop that idea. when
dropping that idea,   I should have re-done it like this from the
start instead of retaining the complexity   i introduced for the
persistent worker design. [Peter Schuller]

* GPGWriteFile: what was previously the minimum block is is now just the
block size; meaning   the maximum block size used for individual I/O
operations, but still the minimum in terms   of when to give up on the
iteration * GZipWriteFile: similar change, though blocksize handling
was a bit different. [Peter Schuller]

* Fix regression -- add tahoebackend back in. [kenneth@loafman.com]

* S/src.name/self.src.name/ in exception handling path. [Peter Schuller]

* Don't be so specific about exceptions we catch. [Michael Terry]

* Add info codes for upload events. [Michael Terry]

* Fix omitted changes in duplicity manpage. [kenneth@loafman.com]

* Changes for 0.6.0. [loafman]

* Some cleanup on the forced assertion test code to allow multiple
failures and no traceback for the assert. [loafman]

* Add code for testing of Checkpoint/Restore that I had been doing by
hand, both single and multiple failure tests, with verify at the end. [loafman]

* Fix getrlimit usage for Cygwin, which was returning -1 for the hard
limit on max open files. [loafman]

* After merge of Checkpoint/Restart. [loafman]

* Allow handling of unicode filenames in log messages. [loafman]

* Changes for 0.5.18. [loafman]

* Changes for 0.5.18. [loafman]

* Correct copyright. [loafman]

* Reset file type preferences. [loafman]

* Changed from using ulimit external command to resource.getrlimit to
check open files limit. [loafman]

* Patch #6743: Tahoe backend for duplicity
https://savannah.nongnu.org/patch/?6743. [loafman]

* Only half of this bug is fixed but it's still useful. bug #21792: pipe
call fails with an error OSError:             [Errno 24] Too many open
files https://savannah.nongnu.org/bugs/?21792. [loafman]

* Added support for RackSpace's CloudFiles, cf+http. [loafman]

* Add more detail on connection failure. [loafman]

* Added support for RackSpace's CloudFiles, cf+http. [loafman]

* Changes for 0.5.17. [loafman]

* Checkpoint. [loafman]

* The previous revision got the wrong comment, so I cleaned up some code
and checked back in.  The correct release comment should be: [loafman]

    patch #6814: Ignore comments in filelists
    https://savannah.nongnu.org/patch/?6814

* Patch #6813: Making changelist easy to read
https://savannah.nongnu.org/patch/?6813. [loafman]

* Moved from using the df command to get temp space availability to
Python's os.statvfs() call.  Not all df commands work the same way. [loafman]

* I had put in some trial code that I removed incompletely that forced a
full backup action.  This removes the last line of that code. [loafman]

* Changes for 0.5.16. [loafman]

* Reduce max\_open\_files limit needed to 1024, was 2048. [loafman]

* Fix argument list in FatalError call re max open files. [loafman]

* Bug #24825: duplicity warn on insufficient TMPDIR             space
availability and low max open             file limits pre-backup.
https://savannah.nongnu.org/bugs/?24825. [loafman]

    bug #25976: Password requested when not needed.
    https://savannah.nongnu.org/bugs/?25976

* Use os.access() check on regular files and dirs only. [loafman]

* Added tilde and variable expansion to the source or target argument
that is not a URL. [loafman]

* Remove check for only one $version string. [loafman]

* Bug #24825: duplicity warn on insufficient TMPDIR             space
availability and low max open             file limits pre-backup.
https://savannah.nongnu.org/bugs/?24825. [loafman]

* Bug #25976: Password requested when not needed.
https://savannah.nongnu.org/bugs/?25976. [loafman]

* Make sure gettext is included first. Add variable at top of file for
verbosity. [loafman]

* Add some documentation. [loafman]

* Make sure gettext is available by importing first. [loafman]

* Move ssh and imap backend globals to globals.py. [loafman]

* Patch #6806: More graceful handling of old              --short-
filename files https://savannah.nongnu.org/patch/?6806. [loafman]

* Bug #25594: wrong backup statistics
https://savannah.nongnu.org/bugs/?25594. [loafman]

* Not needed. [loafman]

* Changes for 0.5.15. [loafman]

* If a file is unreadable due to access rights or other non-fatal
errors, put out error message and continue rather than dying messily
with a traceback. [loafman]

* Move SystemExit function back to the top and put a large note NOT to
move it back down, otherwise, Exception gets invoked instead. [loafman]

* Remove "--restore-dir" from options[].  It's not an option and never
has been. [loafman]

* Added tilde '\~' expansion and variable expansion in the options that
require a filename.  You can now have this "--archive-
dir=\~/ArchDir/$SYSNAME" if you need it.  No expansion is applied to
the source or target URL's. [loafman]

* Unit tests were failing for ftp because of the filtering for
duplicity-only filenames.  Corrected this and removed the check for
the filename in the first element. [loafman]

* If a file is unreadable due to access rights or other non- fatal
errors, put out error message and continue. [loafman]

* FTP backend was failing on PureFTPd when the "-x ''" option was
removed from the second ncftpls popen, a fix that was implemented due
to bug #24741.  This fix does the ls in one pass by extracting either
the first or the last entry on the 'ls -l'.  [Standard FTP would be
nice!] [loafman]

* Changes for 0.5.14. [loafman]

* Normalized include statements and tried to insure that all duplicity
includes were from the duplicity module. [loafman]

* After email voting among known duplicity contributors, the decision
was reached to revert to the GPL Version 2 license, so with their
consensus, duplicity is now under GPL Version 2. [loafman]

* The -vN option has not changed.  Verbosity may also be one of:
character [ewnid], or word ['error', 'warning', 'notice',  'info',
'debug'].  The default is 4 (Notice).  The options  -v4, -vn, and
-vnotice are functionally equivalent, as are  the mixed-case versions,
-vN, -vNotice, -vNOTICE. [loafman]

* The -vN option has not changed.  Verbosity may also be one of:
character [ewnid], or word ['error', 'warning', 'notice',  'info',
'debug'].  The default is 4 (Notice).  The options  -v4, -vn, and
-vnotice are functionally equivalent, as are  the mixed-case versions,
-vN, -vNotice, -vNOTICE. [loafman]

* Patch #6790: Add --exclude-if-present
https://savannah.nongnu.org/patch/?6790. [loafman]

* Clarify recent log entries. [loafman]

* Add '../' to Python path so we find our GnuPGInterface and not
another. [loafman]

* Changed from log.Log with numbered log levels to log.Debug, log.Info,
log.Notice, log.Warn, log.FatalError as below:     0  log.FatalError
1  log.Warn     2  log.Warn     3  log.Notice     4  log.Notice     5
log.Info     6  log.Info     7  log.Info     8  log.Info     9
log.Debug The -vN option has not changed at this point. [loafman]

* Revert to calling NcFTP utilities (ls, get, put) directly rather than
scripting ncftp via pexpect.  Move fatal error regarding version 3.2.0
to a warning message since it has been reported that the segfault
problem does not occur on most distributions. [loafman]

* Add Changelog.GNU to website and distribution to add a bit of detail
showing the CVS changes via rcs2log.  Added dist/mkGNUChangelog.sh. [loafman]

* Bug #22908: Don't block gpg-agent
https://savannah.nongnu.org/bugs/?22908. [loafman]

    To fix the above, --use-agent was added as a command line option.
    When this is specified and asymetric encryption is enabled, then all
    GnuPG passphrases will come from the gpg-agent or equivalent program
    and no passphrase prompt will be issued.

* Add testing/manual dir. [loafman]

* Bug #25976: Signed Backups Now Required
https://savannah.nongnu.org/bugs/?25976. [loafman]

* Patch #6787: import duplicity.GnuPGInterface explicitly
https://savannah.nongnu.org/patch/?6787. [loafman]

* Project setting changes. [loafman]

* One statement per line. Indent text of error message to code level. [loafman]

* Fixed bug where an extra comma caused a traceback during a warning
about unnecessary sig files.  Plus fixed print so the real filename
would show up and not a Python object representation. [loafman]

* Bug #25787: Usernames with escaped @-sign are not handled properly
https://savannah.nongnu.org/bugs/?25787. [loafman]

* Adjust log levels so errors show up without verbosity. [loafman]

* BackendException does not cause traceback except when verbosity is at
level 9 (debug). [loafman]

* Fix backends so sleep does not occur after last retry. [loafman]

* Add more error detection to FTP backend. [loafman]

    Fix backends so sleep does not occur after last retry.

* Patch #6773: Make user name optional in rsync backend
https://savannah.nongnu.org/patch/?6773. [loafman]

* Bug #25853: duplicity fails with boto passwords coming from \~/.boto
https://savannah.nongnu.org/bugs/?25853. [loafman]

* GPG errors will no longer cause tracebacks, but will produce a log
entry, from gpg, similar to the following: ===== Begin GnuPG log =====
gpg: BAD0BAD0: skipped: public key not found gpg: [stdin]: encryption
failed: public key not found ===== End GnuPG log ===== This will let
the user know what really caused the GPG process to fail, and what
really caused errors like 'broken pipe'. [loafman]

* Bug #25838: Backup fails / ncftp - remote file already exists
https://savannah.nongnu.org/bugs/?25838. [loafman]

* Add / modify / repair Epydoc docstrings and format. [loafman]

* One statement per line. [loafman]

* One statement per line. [loafman]

* Changes for 0.5.11. [loafman]

* Bug #333057: GnuPGInterface prints exit statuses incorrectly
https://bugs.launchpad.net/bugs/333057. [loafman]

* Bug #25787: Usernames with @-sign are not handled properly
https://savannah.nongnu.org/bugs/?25787. [loafman]

* Detabify (was tab-width 8). [loafman]

* Bug #333057: GnuPGInterface prints exit statuses incorrectly
https://bugs.launchpad.net/bugs/333057. [loafman]

* Fix issue on return from waitpid where the result was shifted left and
not right, producing 131072 instead of 2, as it should. [loafman]

    Fixed some indent problems that PyDev complained about (Eclipse IDE).

* One statement per line. [loafman]

* Bug #25696: ncftp error with 0.5.09
https://savannah.nongnu.org/bugs/?25696. [loafman]

* Also log the quit command. [loafman]

* One statement per line. [loafman]

* Bug #15664: When restoring backup: "OverflowError:             long
int too large to convert to int"
https://savannah.nongnu.org/bugs/?15664. [loafman]

* One statement per line. [loafman]

* Patch #6761: More robust pexpect handling of SSH authentication
https://savannah.nongnu.org/patch/?6761. [loafman]

* Patch #6762: Wrong exit() used for 2.3/2.4 Python
https://savannah.nongnu.org/patch/?6762. [loafman]

* One statement per line. [loafman]

* Explain new filenames and --time-separator better. [loafman]

* Changes for 0.5.10. [loafman]

* Add deprecation warnings for options affected by old filenames. [loafman]

* Bug #19988: Incompatibility to Samba/SMB share
https://savannah.nongnu.org/bugs/?19988. [loafman]

* One statement per line. [loafman]

* One statement per line. [loafman]

* Module gettext should be imported and installed prior to importing any
other modules.  This allows long strings to be translated when put at
the module level rather than at the function call level.  See
dup\_time.py for examples. [loafman]

* One statement per line and other cleanup. [loafman]

* Bug #25550: Error codes do not propagate from log to exit status
https://savannah.nongnu.org/bugs/?25550. [loafman]

* Bug #25097: Allow listing files from any time, not just current time
https://savannah.nongnu.org/bugs/?25097. [loafman]

* Bug #229826 duplicity crashed with ValueError in port()
https://bugs.launchpad.net/duplicity/+bug/229826. [loafman]

* Changes for 0.5.09. [loafman]

* If tempdir.py is included, but not instantiated, then deleted, it
throws an exception, as happens during testing when duplicity main is
not used to instantiate tempdir. The fix is to make sure instantiation
has happened before calling cleanup(). [loafman]

* These are changes to make debugging easier. - Filter ANSI control
(bolding) characters from NcFTP responses. - Turn off ad for ncftp
server at close of each session. [loafman]

* Bug #25530: commandline passwd not working
https://savannah.nongnu.org/bugs/?25530. [loafman]

* FTP is now driven with pexpect rather than NcFTP utilities. This
closes the following bugs: bug #24741: ncftpls -x '' causes failure on
Yahoo FTP server bug #23516: duplicity/ncftpget not closing unlinked
files, ... [loafman]

* Merge from pexpect\_ftp. [loafman]

* Applied retryImap2.patch from bug 25512. [loafman]

* Bug #25509: Logic error in imapbackend.py [IMAP\_SERVER]
https://savannah.nongnu.org/bugs/?25512. [loafman]

    bug #25512: [Patch] Retry on Imap failure
    https://savannah.nongnu.org/bugs/?25509

* Replace rdiff-backup with duplicity in strings. [loafman]

* Add copyright for author. [loafman]

* Split parsedurl test from backendtest and add test cases. [loafman]

* Add NcFTP 3.2.0 exception clause to dependencies. [loafman]

* Turns out going backwards in the license is not as easy as forwards.
Restoring GPLv3 license until consensus reached. [loafman]

* Add/update copyright statements in all distribution source files and
revert duplicity to GPL version 2 license. [loafman]

* Changes for 0.5.07. [loafman]

* Python 2.3 unittest.py tried to call to a test-local variable named
'test\_id' and failed.  Changed to 'my\_test\_id' and all is well. [loafman]

* Original fix to disallow use of ncftpput 3.2.0 mistyped the ErrorCode
used. [loafman]

* Patch #6733: Improve error handling in imapbackend.py
https://savannah.nongnu.org/patch/?6733. [loafman]

* Add/update copyright statements in all distribution source files and
revert duplicity to GPL version 2 license. [loafman]

* Patch #6729: New imap backend. Replaces current gmail backend
https://savannah.nongnu.org/patch/?6729. [loafman]

* Bug #25293: IOError: [Errno 22] Invalid argument
https://savannah.nongnu.org/bugs/?25293. [loafman]

* Modify patch #6730: Fix timing out for SSH backend Do not take out the
first line from the return buffer (#4). [loafman]

* Patch #6730: Fix timing out for SSH backend
https://savannah.nongnu.org/patch/?6730. [loafman]

* Patch #6729: New imap backend. Replaces current gmail backend
https://savannah.nongnu.org/patch/?6729. [loafman]

* Removed ref to bug 25331 since the analysis and fix were both wrong.
The issue was fixed correctly in bug 25403. [loafman]

* Bug #25403: 0.5.06 "manifests not equal because different volume
numbers" https://savannah.nongnu.org/bugs/?25403. [loafman]

* Bug #25403: 0.5.06 "manifests not equal because different volume
numbers" https://savannah.nongnu.org/bugs/?25403. [loafman]

* One statement per line. [loafman]

* Move alltests list to separate file. [loafman]

* Add coverage output to .cvsignore. [loafman]

* Turn on verbose for unit tests. [loafman]

* Fix backendtest.py so that empty URL's in config.py cause the backend
test to be skipped rather than erroring.  Added notes in
config.py.tmpl explaining the change. [loafman]

* Make default Python be system default version. [loafman]

* Add Releases directory. [loafman]

* First pass at coverage analysis, collect the data. [loafman]

* Remove LOG entries.  Not needed. [loafman]

* Change to ASCII (-kkv) [loafman]

* Run a single unit test. [loafman]

* Increase default volume size (--volsize) to 25M from 5M.  This reduces
the number of volumes to accomodate larger backups. [loafman]

* Bug #25379: sys.exit() causes traceback and should not
https://savannah.nongnu.org/bugs/index.php?25379. [loafman]

* Reworked patch 6701 to list collection one at a time rather than
writing all as one huge list.  Was causing memeory problems when the
collections got large. [loafman]

* Bug #25331: When --archive-dir and --encrypt-key are used together,
incremental fails. https://savannah.nongnu.org/bugs/index.php?25331. [loafman]

* Bug #25331: When --archive-dir and --encrypt-key are used together,
incremental fails. https://savannah.nongnu.org/bugs/index.php?25331. [loafman]

* Changes for 0.5.06. [loafman]

* Fix illegal macro .PP. by removing extraneous period on end. [loafman]

* NcFTP version 3.2.0 will not work with duplicity since we require the
use of both -f and -C options on ncftpput.  3.1.9, 3.2.1+ work fine. I
put in error checks for this situation in the FTP backend code. [loafman]

* Noah Spurrier has given us permission to distribute pexpect.py along
with duplicity, so this will no longer be an install requirement. [loafman]

* Added loop to run-all-tests.sh to run all tests against all supported
versions of Python if available.  Looks for 2.3, 2.4, 2.5, 2.6. [loafman]

* Fix to deprecation warnings about sha and md5 modules. Uses hashlib if
available, otherwise original module. [loafman]

* Missed the most basic case, no selection functions.  Fixed. [loafman]

* Bug #25230: --include-globbing-filelist only including first entry.
https://savannah.nongnu.org/bugs/?25230. [loafman]

* Sr #106583: document the need to use the --force option
https://savannah.nongnu.org/support/?106583. [loafman]

* Patch #6709: Report correct number of volumes when restoring
https://savannah.nongnu.org/patch/?6709. [loafman]

* Bug #25239: Error during clean, wrong case in duplcicity
https://savannah.nongnu.org/bugs/?25239. [loafman]

* Changes for 0.5.05. [loafman]

* Add po files back into distribution. [loafman]

* Cosmetic - reformat FatalError calls at end for readability. [loafman]

* Change "test" to "$version". [loafman]

* Build list of .mo files to be installed from po directory. [loafman]

* Bug #25194: Duplicity 5.04 requires python-distutils-extra...
https://savannah.nongnu.org/bugs/?25194. [loafman]

* Use reldate expansion to include release date. [loafman]

* Use os.path.join() instead of hardcoded strings - Make VersionedCopy
replace $reldate as well as $version. [loafman]

* Adjust RPM spec file for translations. [loafman]

* Changes for 0.5.04. [loafman]

* Patch #6702: handle unknown errnos in robust.py
https://savannah.nongnu.org/patch/?6702. [loafman]

* Patch #6700: Make duplicity translatable
https://savannah.nongnu.org/patch/?6700 [not in patch - added after
unit tests] [loafman]

* Patch #6701: Make current-list command machine-readable
https://savannah.nongnu.org/patch/?6701. [loafman]

* Patch #6700: Make duplicity translatable
https://savannah.nongnu.org/patch/?6700. [loafman]

* GPG was throwing "gpg: [don't know]: invalid packet (ctb=14)" and
apparently this is non-fatal. There is a fix for this being rolled
into GPG 2.x. http://lists.gnupg.org/pipermail/gnupg-
devel/2006-September/023180.html Copied from collections.py.  Fix
supplied by Simon Blandford <simon@onepointltd.com> [loafman]

* One statement per line.  No other changes. [loafman]

* One statement per line.  No other changes. [loafman]

* Print backend name for each test started. [loafman]

* Remove test for assert on non-existing delete.  Not all backends will
raise an exception when the target of a delete does not exist. [loafman]

* Log correct file name in line 67.  Use diff\_ropath, not basis\_path. [loafman]

* Fix patch applied during Patch #6696.  Applied fixiter.diff. [loafman]

* Patch #6697: Always log at least one progress during dry run
https://savannah.nongnu.org/patch/?6697. [loafman]

* Patch #6696: Consolidate get\_delta\_iter and get\_delta\_iter\_w\_sig
https://savannah.nongnu.org/patch/?6696. [loafman]

* Patch #6695: Log filenames https://savannah.nongnu.org/patch/?6695. [loafman]

* Patch #6694: Log exceptions https://savannah.nongnu.org/patch/?6694. [loafman]

* Patch #6693: Some FatalError's don't have codes still
https://savannah.nongnu.org/patch/?6693. [loafman]

* Patch #6692: Print collection status in a machine-readable way
https://savannah.nongnu.org/patch/?6692. [loafman]

* Bug #24889: NCFTP cannot deal with some FTP servers
https://savannah.nongnu.org/bugs/?24889. [loafman]

* Bug #25090: Typos and trailing whitespace in duplicity manpage
https://savannah.nongnu.org/bugs/?25090. [loafman]

* Patch #6686: Add error codes for all fatal errors
https://savannah.nongnu.org/patch/?6686. [loafman]

* Patch #6678: Add progress metering
https://savannah.nongnu.org/patch/?6678. [loafman]

* Changes for 0.5.03. [loafman]

* Patch #6676: Raw delta stats aren't right for multivolumes
https://savannah.nongnu.org/patch/?6676. [loafman]

* Patch #6675: Add modelines https://savannah.nongnu.org/patch/?6675. [loafman]

* Patch #6674: Add --log-* options to man page
https://savannah.nongnu.org/patch/?6674. [loafman]

* Patch #6673: Add --dry-run option
https://savannah.nongnu.org/patch/?6673. [loafman]

* Patch #6672: makedist doesn't ship util.py
https://savannah.nongnu.org/patch/?6672. [loafman]

* Add log.setup() call to main() to support new logging. [loafman]

* *** empty log message *** [loafman]

* Add log.setup() to support new logging. [loafman]

* Checkpoint 2 prior to 5.03. [loafman]

* Patch #6670: Machine Readable Output
https://savannah.nongnu.org/patch/?6670. [loafman]

* Correct spelling of parsed\_url (parsed\_urk) in patch #6662. [loafman]

* Sr #106534: GMail backups aren't stored in the correct location
https://savannah.nongnu.org/support/?106534. [loafman]

* Sr #106496: put install-from-cvs-notes in CVS-README
https://savannah.nongnu.org/support/?106496. [loafman]

* Checkpoint prior to 5.03. [loafman]

* Patch #6638: correct typo in reporting lack of sufficiently new boto
backend https://savannah.nongnu.org/patch/?6638. [loafman]

* Patch #6642: make ParsedUrl() thread-safe with respect to itself
https://savannah.nongnu.org/patch/?6642. [loafman]

* Patch #6652: improve asynch scheduler (including the synchronous case)
https://savannah.nongnu.org/patch/?6652. [loafman]

* Patch #6662: improve s3 backend error reporting
https://savannah.nongnu.org/patch/?6662. [loafman]

* Patch #6670: Machine Readable Output
https://savannah.nongnu.org/patch/?6670. [loafman]

* Bug #24775: Digest Auth for WebDAV backend
https://savannah.nongnu.org/bugs/?24775. [loafman]

* Bug #24731: Documentation error: "if... if" in remove-older-than
paragraph https://savannah.nongnu.org/bugs/?24731. [loafman]

* Changes for 0.5.02. [loafman]

* Patch #6297: Add IMAP/s/gmail support
https://savannah.nongnu.org/patch/index.php?6297. [loafman]

* Patch #6297: Add IMAP/s/gmail support
https://savannah.nongnu.org/patch/index.php?6297. [loafman]

* Change to one statement per line. [loafman]

* Change use of logger so that gpg logs are always collected. The log is
always printed in the case of gpg IO errors. Verbosity level 5 or
greater will also print the logs the same as previous versions. [loafman]

* Make one statement per line.  No other changes. [loafman]

* Add -h option for help. [loafman]

* Bug #24274: asyncscheduler.py missing sys import
https://savannah.nongnu.org/bugs/index.php?24274. [loafman]

* Bug #24260: backend.py missing re import
https://savannah.nongnu.org/bugs/index.php?24260. [loafman]

* Changes for 0.5.01. [loafman]

* Ignore test log file. [loafman]

* Untabify all files.  To compare against previous versions use 'cvs
diff -w' or 'diff -w'. [loafman]

* Create target dir (collection) if needed. [loafman]

* Ignore testfiles dir. [loafman]

* Add tests for webdav and webdavs. [loafman]

* Bug #24223: WebDAV backend broken in 0.5.00
https://savannah.nongnu.org/bugs/index.php?24223. [loafman]

* Changes for 0.5.00. [loafman]

* Changes for 0.5.00. [loafman]

* Temp2.tar was a test-created file that had to be present at the
beginning of test\_tarfile.py.  Removed the need for it to be present
and removed the file from CVS. [loafman]

* Changes to get unit tests working again:   - resolve circular imports
during unit tests   - resolve exception error import - now in
errors.py. [loafman]

* Patch #6623: slightly augment tempdir cleanup logging
https://savannah.nongnu.org/patch/index.php?6623. [loafman]

* No longer needed, see backends dir. [loafman]

* No comment. [loafman]

* Bug #23988: scp destination fails if no username is specified
https://savannah.nongnu.org/bugs/index.php?23988. [loafman]

* Bug #23985: --no-encryption option does not work in 0.4.12
https://savannah.nongnu.org/bugs/index.php?23985. [loafman]

* Patch #6596: re-organize backend module structure
https://savannah.nongnu.org/patch/index.php?6596. [loafman]

* Patch #6353: Concurrency for volume encryption and upload.
https://savannah.nongnu.org/patch/index.php?6353. [loafman]

* Patch #6589: S3 european bucket support
https://savannah.nongnu.org/patch/index.php?6589. [loafman]

* Changes for 0.4.12. [loafman]

* Bug #23362: Documentation for --version, --time-separator <char>
https://savannah.nongnu.org/bugs/index.php?23362. [loafman]

* Cosmetic only. [loafman]

* Bug #23540: doc bug in man page (environment FTP\_PASSWORD)
https://savannah.nongnu.org/bugs/?23540. [loafman]

* Dan Muresan created a patch that tries to minimize the number of
password prompts.  To do so, it sometimes requests a password once
without confirmation; if later it turns out that a full backup is
needed, the user is prompted for confirmation. [loafman]

* Bug #23066: ssh uris with given portnumbers are not handled correctly
https://savannah.nongnu.org/bugs/index.php?23066. [loafman]

* Fix sort() for Python 2.3. [loafman]

* Change back to requiring Python 2.3. [loafman]

* Change requirements back to Python 2.3. [loafman]

* Changes for 0.4.11. [loafman]

* Modified to run on Python 2.3. [loafman]

* Bug #22826: regressions caused by boto 1.1c
https://savannah.nongnu.org/bugs/?22826. [loafman]

* Reinstate patch #6340 with a detailed explanation.
http://savannah.nongnu.org/patch/index.php?6340. [loafman]

* Changes for 0.4.10. [loafman]

* Remove --sign for now. [loafman]

* Bug #22728: FTP backend fails on empty directory
https://savannah.nongnu.org/bugs/?22728. [loafman]

* Fix log.debug to log.Debug. [loafman]

* Patch #6453: handle absolute urls in webdav backend
https://savannah.nongnu.org/patch/index.php?6453. [loafman]

* Patch #6449: add additional debug level logging
https://savannah.nongnu.org/patch/index.php?6449. [loafman]

* Patch #6403: Restore by overwriting files/directories by using --force
option https://savannah.nongnu.org/patch/?6403. [loafman]

* Password should be None, not empty string. [loafman]

* Add config for S3 tests. [loafman]

* Reformat to one statement per line. [loafman]

* Fix problem where S3 prefix was appended with 'd'.  This caused a
failure in the regression tests.  Unsure where it came from. [loafman]

* Patch #6389: Possible Fix for pagefile.sys on Win32 systems
https://savannah.nongnu.org/patch/?6389. [loafman]

* Patch #6380: add additional named logging levels
https://savannah.nongnu.org/patch/?6380. [loafman]

* Patch #6374: Duplicity --tempdir patch documentation.
https://savannah.nongnu.org/patch/?6374. [loafman]

* Patch #6375: Duplicity reports the epoch for a nonexistant last full
backup date https://savannah.nongnu.org/patch/?6375. [loafman]

* Remove sleep() from dup\_time.py - not used. - make one statement per
line format change. [loafman]

* Remove testSleeping since sleep() removed from dup\_time.py. [loafman]

* Add S3 backend test. [loafman]

* Do not store object. [loafman]

* Add requirements for source package install. [loafman]

* Changes for 0.4.9. [loafman]

* Add more info on URL formats. [loafman]

* Updated URL Formats in the Help Screen. [loafman]

* Added section URL FORMAT in the duplicity man page. [loafman]

* Make sure to strip extraneous single colon when dealing with non-
module URLs.  We provide the colon as needed. [loafman]

* Bug #21909: Problematic typo in compare\_verbose() method
https://savannah.nongnu.org/bugs/index.php?21909. [loafman]

* Patch #6357: Explicit restore action is missing from the command list,
https://savannah.nongnu.org/patch/?6357. [loafman]

* Patch #6356: Command line option for the temporary directory root.
https://savannah.nongnu.org/patch/?6356. [loafman]

* Added regression tests for absolute, relative, and module pathing in
the rsync scheme. [loafman]

* Fixed rsync URL description text in --help. [loafman]

* Added 2nd patch to bug #21475 that forces all versions of Python to
use the fixed urlparse.py. [loafman]

    Fixed issue with Pure-FTPd that would always return an empty
    directory listing and thus force a full backup every time.
    A side effect of the change is that we now only make one call
    to ncftpls to get the listing, thereby reducing the overhead
    on systems with a large number of backup files.

    bug #21896: Two problems with rsync under 0.4.8 + patch
    https://savannah.nongnu.org/bugs/index.php?21896

    patch #6354: S3 staight typo results in a bogus exception
    https://savannah.nongnu.org/patch/?6354

* Fixed so that remove-older-than and remove-all-but-n-full will not
request a GPG passphrase. [loafman]

* Fixed regression caused by changeover to new urlparse.py. bug #21475:
FTP Usernames that contain '@' are not recognized
https://savannah.nongnu.org/bugs/index.php?21475. [loafman]

* Changes for 0.4.8. [loafman]

* Format to one statement per line. [loafman]

* Allow pexpect to force the close of the child on sftp calls.  We
already do that with scp calls.  This cleans up that exception. [loafman]

* Patch #6344: S3 bad bad key key handling
http://savannah.nongnu.org/patch/?6344. [loafman]

* Replace set\_password/phrase with set\_environ and clarify meaning in
config.py. [loafman]

* Complete description of install using --prefix=. [loafman]

* Fix version of boto needed plus formatting. [loafman]

* Patch #6340: S3 short filename regression
https://savannah.nongnu.org/patch/?6340. [loafman]

* Make sure config.py not checked in. [loafman]

* Initial release. [loafman]

* This test requires a file that no longer exists. Plus, it is unclear
what this test is supposed to accomplish.  Tar is tested by the other
tests. [loafman]

* First pass at getting tests up to date:   -- isolate config in
'config.py' (see config.py.tmpl)   -- silence noisy tests as much as
possible   -- fix code on both sides as needed. [loafman]

* Initial release. [loafman]

* Remove 2nd call to dup\_time.settimestr() since it overrides the time
that may be set by --current-time (used for testing). [loafman]

* Regen dup\_time.curtimestr if time-separator changed. [loafman]

* Fixed previous patch that assumed the presence of the user and
password in the rsync URL. [loafman]

* Bring tests up to date. [loafman]

* Bug #21751: rsync module urls do not work in 0.4.7
https://savannah.nongnu.org/bugs/index.php?21751. [loafman]

    bug #21752: Boto backend needs version 0.9d or later
    https://savannah.nongnu.org/bugs/index.php?21752

* Changes for version 0.4.7. [loafman]

* Change to require Python 2.4 or later. [loafman]

* Formatted list and added tempdir.py and urllib\_2\_5.py to the
released files list. [loafman]

* Fix confusion over patches applied to different versions. Patch #6300
should now be applied completely. [loafman]

    Added back munge_password() so entire commandline could
    be logged without the password showing.

* Hole imapbackend till next release. [loafman]

* Hold till next release. [loafman]

* Patch #6300: Standard library replacement for ParsedUrl class
https://savannah.nongnu.org/patch/?6300. [loafman]

    I had to fix the ssh/scp scheme to remove the leading '/' in
    parsed_url.path, otherwise it tried to treat the path as absolute.

* Backed out the following patch until bugs fixed... patch #6300:
Standard library replacement for ParsedUrl class
https://savannah.nongnu.org/patch/?6300. [loafman]

* Patch #6301: log sftp commands at verbosity 5
https://savannah.nongnu.org/patch/?6301. [loafman]

* Patch #6300: Standard library replacement for ParsedUrl class
https://savannah.nongnu.org/patch/?6300. [loafman]

* Patch #6299: re-design tempfile handling
https://savannah.nongnu.org/patch/?6299. [loafman]

* Move import of imapbackend to the end of the module.  Circular
dependency.  Needs fixing. [loafman]

* Undo regression of bug #21508 contained in patch #6298: URI unquoting
patch for FTP backend https://savannah.nongnu.org/patch/?6298. [loafman]

    Some cosmetic cleanup.

* Patch #6298: URI unquoting patch for FTP backend
https://savannah.nongnu.org/patch/?6298. [loafman]

* Patch #6297: Add IMAP/s/gmail support
https://savannah.nongnu.org/patch/?6297. [loafman]

    Added 2nd patch for above.

* Patch #6297: Add IMAP/s/gmail support
https://savannah.nongnu.org/patch/?6297. [loafman]

* Patch #6292: Amazon S3 bucket creation deferral for Duplicity 0.4.6
https://savannah.nongnu.org/patch/?6292. [loafman]

* Bug #21686: NcFTPGet 3.2.0 tempfile incompatibility
https://savannah.nongnu.org/bugs/index.php?21686. [loafman]

* Applied patch from Eric Hanchrow to fix logging error in botoBackend,
and fix delete() in rsyncBackend. [loafman]

    bug #21686: NcFTPGet 3.2.0 tempfile incompatibility
    https://savannah.nongnu.org/bugs/index.php?21686

* Bug #21673: remove-all-but-n-full wrong arg usage
https://savannah.nongnu.org/bugs/index.php?21673. [loafman]

    patch #6293: [patch] left-over patching from
    remove-all-but-n-full patch
    https://savannah.nongnu.org/patch/?6293

* More Changes for 0.4.6. [loafman]

* Changes for 0.4.6. [loafman]

* Fixed coding problem where matched\_sig\_chain could be referenced
before it was defined. [loafman]

* Https://savannah.nongnu.org/patch/index.php?6291 patch #6291:
Alternative WebDAV HTTPS patch. [loafman]

* Https://savannah.nongnu.org/patch/index.php?6289 patch #6289: Amazon
S3 key prefix patch for Duplicity 0.4.5. [loafman]

* Https://savannah.nongnu.org/patch/?6284 patch #6285: security fix:
eliminate use of mktemp() [loafman]

* Https://savannah.nongnu.org/bugs/index.php?21651 bug #21651, add https
support for webdav. [loafman]

    https://savannah.nongnu.org/patch/?6284
    patch #6284: document TMPDIR and friends

* Https://savannah.nongnu.org/bugs/index.php?21657 bug #21657: ncftpls
fails to create dir in ver 0.4.5. [loafman]

* Https://savannah.nongnu.org/bugs/index.php?21651 bug #21651, add https
support for webdav. [loafman]

* Try, the second.  See comments in the bug tracker.
https://savannah.nongnu.org/bugs/index.php?21646 bug #21646:
--archive-dir causes delete of remote full sigs and orphaned sig files. [loafman]

* Https://savannah.nongnu.org/bugs/index.php?21651 bug #21651, add https
support for webdav. [loafman]

* Fix release date in 0.4.5. [loafman]

* Changes for 0.4.5. [loafman]

* Https://savannah.nongnu.org/bugs/index.php?21646 Fix to handling of
collections when --archive-dir is used. Prior to this, duplicity would
write the full sig files to both local and remote, then delete the
remote.  Now, it does not delete the remote full sigs. [loafman]

    Applied the following patches from Peter Schuller
    patch #6279, add command 'remove-all-but-n-full'
    patch #6280, clarify --archive-dir option
    patch #6281, --help should print to stdout, not stderr
    patch #6282, collection-status: output in more consistent order

* Changes for version 0.4.4. [loafman]

* Applied a patch from Gregory Hartman to correct handling of DST in
time calculations.  This affects backups made the night of a DST time
switch. [loafman]

* Cosmetic - Use True and False, not 1 and None. [loafman]

* Fix version checking code in ftpBackend. [loafman]

* Changes to commandline processing to allow non-ambiguous short strings
for commands, i.e. 'i', 'inc', 'incr' for 'incremental', 'f' for
'full', etc..  A warning message is printed if the short command is
not unique. [loafman]

* Changes to ftpBackend to use the login config file rather than putting
the username and password on the command line.  This requires the use
of NcFTP 3.1.9 or later. [loafman]

    Thanks to a patch from Greg Hewgill the Amazon S3 backend now
    uses --num-retries to retry IO repeatedly if needed.

* Changes for 0.4.4.RC4 try 2. [loafman]

* Changes for 0.4.4.RC4. [loafman]

* Replace with Version 3 GPL text. [loafman]

* Fixed issue in --time-separator where the current time string was
being set prior to setting the separator, causing errors when trying
to set the --time-separator for Windows systems. [loafman]

* There is a new command line syntax to separate actions and options.
Refer to the new man page for full details. [loafman]

* Correct calling sequence in calls to get\_signature\_chains(). [loafman]

* Fix so that ftpBackend.delete() does not print file list. [loafman]

* Fix so that file mtime is always compared in full seconds. [loafman]

* Changes for 0.4.4.RC3 -- Corrected. [loafman]

* Changes for 0.4.4.RC3. [loafman]

* Add 'patch' dir to ignore list. [loafman]

* Patch from Olivier Croquette to add :port option in FTP. [loafman]

* Patch from Olivier Croquette to add --full-if-older-than=<time> option
to force a full backup at <time> rather than incremental. [loafman]

* Patch from Olivier Croquette to add :port option in FTP. [loafman]

    Patch from Mitchell Garnaat to get all keys from S3, rather
    than just the first 1000.

    Fix to sshBackend to version check for python-pexpect 2.1.

    Fix one case in ftpBackend where host string was used instead of
    url_string.  This only affected the creation of the target dir on
    the remote system, if it did not exist, and only if the user or
    port needed to be specified.

* Changes for 0.4.4.RC2. [loafman]

* Added --timeout <seconds> (default 30) to allow users to change
duplicity's network timeout settings. [loafman]

    Added --time-separator <char> to allow users to change the time
    separator from ':' to another character that will work on their
    system.  HINT: For Windows SMB shares, use --time-separator='_'.

* Add patch from Olivier Croquette to allow user@domain usernames,
making ftp://user@domain@domain.com/path a valid URL. [loafman]

    Added a bit of debug print to sshBackend for --verbosity=9.

* Add patch from Alexander Zangerl to suppress the GPG passphrase prompt
when a passphrase is not needed.  - full and pubkey enc:  doesn't
depend on old encrypted info  - inc and pubkey enc and archive-dir:
need manifest and sigs,    which the archive dir contains unencrypted
- with encryption disabled  - listing files:  needs manifest, but the
archive dir has that  - collection status:  only looks at a repository. [loafman]

* Changes for 0.4.4.RC1. [loafman]

* Https://savannah.nongnu.org/patch/index.php?6205 Add option
--librsync-dir for when its not found. [loafman]

* Bug #21123: duplicity 0.4.3 does not find any backup chains
https://savannah.nongnu.org/bugs/?21123. [loafman]

* Make tempfiles with useful names. [loafman]

* Fixes manual page and usage msg for rsync url and --remove-older-than. [loafman]

* Fix for Debian bug #228388: old/aborted/offending sig files prohibit
any further action. [loafman]

* Fixes manual page and usage msg for rsync url and --remove-older-than. [loafman]

* Do not ask for passphrase when none is needed. [loafman]

* Final patch for Peter Schuller's fix to max read size. The first one
was broken (revision previous to this). [loafman]

* Add patch submitted by Peter Schuller which removes the default SSH
options that ignored known hosts files and disabled strict host
checking.  This patch also handles the authentication failures from
these issues. [loafman]

* Fixed so that max read size is 64k, not the volume size which can be
quite large. [loafman]

* Fix release date. [loafman]

* Changes for 0.4.3 release. [loafman]

* Removed use of tempfile.TemporaryFile().  This fixes the restore
problem on Windows that was due to Python bug 1776696 reported on
Sourceforge. [loafman]

* Removed hardwired options to use bzip2 compression. [loafman]

    Added gpg-options to allow users to add options to
    the gpg process.

* Changed ssh-command to ssh-options to allow users to add options to
the scp and sftp commmands. [loafman]

    Added gpg-options to allow users to add options to
    the gpg process.

* Move get\_password() to Backend class to standardize. [loafman]

    Fix problem with ftpBackend to create target directory if needed.

* Upgrade to GPL version 3 license. [loafman]

* Do not pass :port part of URL to scp backend. Its taken as the target
file and errors out. [loafman]

* Change ssh\_command option to be ssh\_options.  This adds options to
the scp and sftp commands that are used by the ssh backend. [loafman]

* Fixed bug 20764 - unable to use port in ssh backend.
https://savannah.nongnu.org/bugs/?20764. [loafman]

    Change ssh backend to send 'quit' instead of EOF when
    using sftp.  This allows it to run under cron as long
    as the password is supplied non-interactively.

* Changes for 0.4.3.RC12. [loafman]

* Changes for 0.4.3.RC12. [loafman]

* Changed the file:, ftp:, and ssh: backends so that the target
directory will be created at start. [loafman]

    Changed the ftp: backend so that empty target dirs
    do not error out.

* Clean up help list formatting. [loafman]

* Fix index out of range in Bug 20730, triggered when there is only one
incremental and no previous in list.
https://savannah.nongnu.org/bugs/?20730. [loafman]

* Print warning if pexpect version is less than 2.1. - Fix author and
maintainer settings. [loafman]

* Fix environment var name for ssh backend. [loafman]

* Changes for 0.4.3.RC11. [loafman]

* Add --ssh-askpass option. [loafman]

* Duplicity now correctly processes scp URL's of the form:
scp://user@host[:port]/ where the directory spec is empty.  This fixes
a bug where the user could not write into the home directory on the
target. [loafman]

    The SSH/SCP backend has had an overhaul.  It now requires the
    python-pexpect module.  Normally this can be obtained from your
    distro's repository, but if you want, you can download pexpect
    from http://pexpect.sourceforge.net.

    The SSH/SCP backend work was done to allow the user to use password
    authentication rather than public-key.  You may now enter a password,
    either through the FTP_PASSWORD environment variable, or at the
    console.  To activate this feature you will need to use the option
    --ssh-askpass on the command line.  The default is public-key, which
    does *not* look for a password from either source.

* Patch #6094, Boto Backend Fixes for RC10. [loafman]

* Changes for 0.4.3.RC10. [loafman]

* Add support for:   --ftp-passive,   --ftp-regular,   --num-retries. [loafman]

    Removed -m option on FTP put command.  This means that
    the remote directory must exist prior to backup.

    Changed ftpBackend from -f option back to commandline.
    Various versions of ncftp* interact differently when
    both -f and commandline options are supplied.

    The FTP password is munged in all log operations.

    Added logging of filenames in the bucket when -v9 is
    used on Amazon S3.

* Add support for:   --ftp-passive,   --ftp-regular,   --num-retries. [loafman]

* Add descriptions for:   --ftp-passive,   --ftp-regular,   --num-
retries. [loafman]

* Replace missing comma in argument list. [loafman]

* Changes for 0.4.3.RC9. Drop ftplib.py. [loafman]

* No longer needed. [loafman]

* Changes for 0.4.3.RC9. [loafman]

* Added a commandline option, '--num-retries=<int>', to set the number
of retries.  The default is 5. [loafman]

* New S3 backend, Boto, from Eric Evans, replaces bitBucket.  Boto can
be obtained from http://code.google.com/p/boto/.  I did not make this
a requirement for setup since its not in the normal repositories. [loafman]

    New FTP backend from Thorsten Schnebeck that uses ncftp instead of
    Pythons ftplib.  This seems to be much more solid.  I added the -f
    option with a secure temp file to contain host, user, and password,
    rather than having them on the command line.  I also added the -m
    option to the put command to create the target directory and the -t
    option to make sure it times out if there is a network problem.

    The Backend class now contains a popen_persist function that acts like
    run_command_persist.  Both use the new num_retries global.

* Change to a max block size of 2048 bytes for rsync difference buffer.
This may slow things down for truly large files, but will give much
smaller deltas on files with numerous small changes, such as database
files. [loafman]

* Initial release. [loafman]

* Changes for 0.4.3.RC8. [loafman]

* Bug 20039 - Andreas Schildbach: --and-- Patch 6030 - Alexander Zangerl
<az@debian.org>: Duplicity now uses bzip2 for compression.  This
matches the way the Debian distribution handles it.  I'll think about
adding an option to override later, if its needed. [loafman]

* Bug 20282 - Thomas Tuttle: An out of range index when checking past
history in the backup sets caused a failure when trying to access
later. [loafman]

    Bug 20149 - dAniel hAhler:
    dAniel submitted a second patch for this for further cleanup.
    The new patch prefers the latest intact backup set.

* Changes for 0.4.3.RC7. [loafman]

* Patch 6029 - Alexander Zangerl <az@debian.org>:
http://bugs.debian.org/370206 archive-dir together with incremental
backup results in crash. the patch is simple, the code in 0.4.2 did
attempt to access strings as objects. [loafman]

* Patch 6033 - Alexander Zangerl <az@debian.org>: let's add a --help
terse usage message and don't just direct the user to the manual. this
should come handy if somebody needs to restore stuff without having
the manual available. [loafman]

* Patch 6032 - Alexander Zangerl <az@debian.org>: a new feature patch:
i've recently gotten annoyed with having gazillions of 5mb files and
therefore added a --volsize option to allow the user setting the chunk
size. the patch is simple and contains a manpage update as well. [loafman]

* Add -u (unbuffered) to shebang line. [loafman]

* Add stderr.flush() in FatalError(). [loafman]

* Bug 20179 - dAniel hAhler: When errors cause login to fail in FTP,
reset and try again. [loafman]

* Not needed. [loafman]

* Cosmetic change to force new log.  The log for revision 1.28 is not
correct.  It should read as follows: [loafman]

    Patch 5993 - daacyy302@sneakemail.com: Make Amazon S3 backend
    incrementally more robust for recovery.

* Changes for 0.4.3.RC6. [loafman]

* Patch 5998 - Kuang-che Wu: Cache uid and gid lookup to speed
operations. [loafman]

* Bug 20419 - dAniel hAhler: When errors cause an incomplete backup set,
flag the error with a message, rather than erroring out.  The user
then knows to run --cleanup. [loafman]

* Changes for 0.4.3.RC5. [loafman]

* DAniel hAhler submitted a patch to change "Error initializing file
foo" (log level 2), where foo was a socket, to "Skipping socket foo"
(log level 7).  https://savannah.nongnu.org/patch/?5985. [loafman]

* Change logging to flush after every write, unbuffering stdout and
stderr, thus producing logs that are coherent. [loafman]

* GnuPG fails when trying to access stdin on an empty passphrase.
Changes allow empty passphrase on public-key encryption and now
respond gracefully on empty passphrase for symmetric encryption. [loafman]

* Changes for 0.4.3.RC4. [loafman]

* Move catch of NLST errors back to self.error\_retry() [loafman]

* More FTP fixes: - clean up error handling - change initial error delay
to zero - move catch of NLST errors to self.list() [loafman]

* Changes to release 0.4.3.RC3. [loafman]

* Fix so that FTP connection/login is closed and reopened when errors
221 or 421 are reported. [loafman]

    - Fix grammer in error message.

* Changes to release 0.4.3.RC2. [loafman]

* Remove GnuPGInterface.py. [loafman]

* Apply patch for bug 19998, ValueError exception. [loafman]

* Added change notices for FTP password and rsync backend. [loafman]

* Fix request password in ftpBackend if environ not set. [loafman]

* Allow connection after 226 in NLST (ProFTPD) - request password in
ftpBackend if environ not set - rsyncBackend was using the full URL,
now uses server:path. [loafman]

* Document changes for 0.4.3. [loafman]

* Do not set FTP to active mode at start of session. [loafman]

* 1) WebDAV needs a Depth: 1 header otherwise infinite depth is assumed
and may be restricted due to load. [loafman]

    2) Used the allprop XML command to get back properties that
    included the filenames.  Refer to RFC 2518.

* Fixes bug:   https://savannah.nongnu.org/bugs/?19940. [loafman]

* Applied patches:   https://savannah.nongnu.org/patch/?5680
https://savannah.nongnu.org/patch/?5681. [loafman]

* Added patches:   https://savannah.nongnu.org/patch/?4486
https://savannah.nongnu.org/patch/?5183
https://savannah.nongnu.org/patch/?5185
https://savannah.nongnu.org/patch/?5412
https://savannah.nongnu.org/patch/?5413
https://savannah.nongnu.org/patch/?5680
https://savannah.nongnu.org/patch/?5681
https://savannah.nongnu.org/patch/?5682
https://savannah.nongnu.org/patch/?5794
https://savannah.nongnu.org/patch/?5830. [loafman]

    Fixed bugs:
      https://savannah.nongnu.org/bugs/?2441
      https://savannah.nongnu.org/bugs/?16711

    Miscellaneous cosmetic fixes (spelling and spacing).

* BitBucketBackend:     * if something goes wrong and we need to re-
connect, dump the exception       on stderr. Be very noisy so that
whatever is wrong will be fixed. [jinty]

* Typo fix for error message. [bescoto]

* Fix a bug in the bitbucket backend: We need to get a new bits from the
new bucket if we re-connect. [jinty]

* Changes to the bitbucket backend: * Update to work with bitbucket
0.3b. * Add some docimentation. * Implement a suggestion by Ben Escoto
to move the access and secret keys to   environment variables. *
Implement a very simplistic error correction mechanisim that will re-
connect   on an operation failure and re-try the operation. Note that
this is just a   band-aid for issues that should be resolved at lower
levels. [jinty]

* Removed time\_separator entry from changelog when I backed out patch. [bescoto]

* Went back to old time\_separator, because I realized new way wouldn't
handle some cases, and could break backwards compatibility. [bescoto]

* Andre Beckedorf's patches for ftp and rsync backends, and
time\_separator. [bescoto]

* Checked in Brian Sutherland's Amazon S3 code. [bescoto]

* Added --sftp-command to changelog. [bescoto]

* Added --sftp-command option and man page documentation. [bescoto]

* Fixed Jiri's name.  Sorry about that :-) [bescoto]

* Final changes for version 0.4.2. [bescoto]

* Fixes to the scp backend. [bescoto]

* Stop --remove-older-than from deleting current chain. [bescoto]

* Catch ftp error 450 when listing directory. [bescoto]

* Cleaned up and documented --collection-status. [bescoto]

* Asdf's tarfile large uid/gid patch. [bescoto]

* Jiri Tyr's scp/sftp patch. [bescoto]

* Eric Hanchrow's remove signature patch. [bescoto]

* A few minor updates so test pass on my system again. [bescoto]

* MDR patch allows signing with different key. [bescoto]

* Added note about passphrase confirmation. [bescoto]

* When collecting password from user, make type it twice to confirm. [bescoto]

* Final changes for 0.4.1. [bescoto]

* Updating rpm for Fedora. [bescoto]

* Trying to remove... [bescoto]

* Small changes for 0.4.1 and python 2.3. [bescoto]

* Variable block size, librsync 0.9.6. [bescoto]

* Remove large file note now that block size chosen based on file size. [bescoto]

* Ported some code from rdiff-backup:  choose sig block based on file
length, and work with librsync 0.9.6. [bescoto]

* Mention problem with /proc. [bescoto]

* Cache pwd and group files. [bescoto]

* Added --version switch, small change to man page. [bescoto]

* Sebastian Wilhelmi's update for rsync backend. [bescoto]

* Applied Stephen Isard's patch for --exclude-globbing-filelist. [bescoto]

* Added mention of rsync backend. [bescoto]

* Added rsync contributed by Sebastian Wilhelmi. [bescoto]

* Added test and fix for long symlink to long file bug. [bescoto]

* Raise error (instead of exiting silently) if no files found to restore. [bescoto]

* Added long filenames test. [bescoto]

* Added man page info on --short-filenames option. [bescoto]

* (version of) Helmut Schneider's patch to display mtimes with list
files. [bescoto]

* Added --no-encryption option, fixed crash on inc when no changed files. [bescoto]

* Added --verify option, tweaked some verbosity levels. [bescoto]

* Added compare\_verbose and test to path module. [bescoto]

* Changed restore procedure.  Now all sets integrated simultaneously. [bescoto]

* Fixed typo in get\_ropath. [bescoto]

* Added a few options for only doing upload/move/checkin/etc. [bescoto]

* Changed way difftars are split between volumes to waste less space. [bescoto]

* Slight tweak to base36 code. [bescoto]

* Added extra tests for base36 conversion. [bescoto]

* Shorted short filenames (use base36) [bescoto]

* Swallow GPG logging output if verbosity 3 or less. [bescoto]

* Added --remove-older-than option, changed --current-time behavior. [bescoto]

* Added --cleanup option. [bescoto]

* Added --force option. [bescoto]

* Added code for finding extraneous and old files. [bescoto]

* For ssh, deleted in groups of 10 so command line doesn't overflow. [bescoto]

* Fixed a few minor collections bugs, added get\_extraneous. [bescoto]

* Added note on one pass restores/verifies. [bescoto]

* Added --restore-time bug fix note. [bescoto]

* Better fix for same (current\_time) bug. [bescoto]

* Fixed minor bug erasing output dir too early. [bescoto]

* Restores now default to current time if restore time not specified. [bescoto]

* Added undocumended --collection-status option for testing purposes. [bescoto]

* More misc updates for 0.3.0. [bescoto]

* Few last minute tweaks to prepare for 0.3.0 release. [bescoto]

* Added --ssh-command and --scp-command options. [bescoto]

* Fixed time-must-be-int bug with --short-filenames, added test. [bescoto]

* Various bugfixes so ftp backend passes final test. [bescoto]

* Added --short-filenames option. [bescoto]

* Added ftp backend support. [bescoto]

* Added man page entry for --file-to-restore option. [bescoto]

* Added statistics reporting after successful backup. [bescoto]

* Added --list-current-files option. [bescoto]

* Make CVS more friendly; don't depend on src symlink. [bescoto]

* Updated documentation on new globbing options. [bescoto]

* Fixed bug & added test when root was reg file, not dir. [bescoto]

* Added --include/exclude-globbing-filelist options. [bescoto]

* Fixed tar '..' security bug. [bescoto]

* Added 2 test cases: neg mtimes, missing u/gnames. [bescoto]

    Now check to make sure these files aren't spuriously marked as
    changed.

* Fixed dumb st\_time/st\_mtime typo. [bescoto]

* Updated with new web page/mailing list information. [bescoto]

* Added full GPL statement in source files at request of Jaime Villate
of the Savannah site.  Also updated address of FSF. [bescoto]

* Initial checkin. [bescoto]


