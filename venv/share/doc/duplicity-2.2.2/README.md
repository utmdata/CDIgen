# INSTALLATION

Thank you for trying duplicity.  To install, run:
```
python3 -m pip install
```

The build process can be also be run separately:
```
python3 -m build
```

The default prefix is /usr, so files are put in /usr/bin,
/usr/share/man/, etc.  An alternate prefix can be specified
using the --prefix=<prefix> option.  For example:
```
python3 setup.py install --prefix=/usr/local
export PYTHONPATH='/usr/local/lib/python.x/site-packages/'
/usr/local/bin/duplicity -V`
```

# REQUIREMENTS

 * Python 3.8 to 3.12
 * librsync v0.9.6 or later
 * GnuPG for encryption
 * see `requirements.txt` for complete list

If you install from the source package, you will also need:

 * Python development files, normally found in module 'python3-dev'.
 * librsync development files, normally found in module 'librsync-dev'.
 
Install python modules by performing the following command in duplicity's root directory:
```
python3 -m pip install -r requirements.txt
```

# DEVELOPMENT

For more information on downloading duplicity's source code from the
code repository and developing for duplicity, see README-REPO.

For source docs: http://duplicity.readthedocs.io/

# HELP

For more information see the duplicity web site at:

  http://duplicity.us

  or at:

  http://duplicity.gitlab.io

or post to the mailing list at

  https://lists.nongnu.org/mailman/listinfo/duplicity-talk
