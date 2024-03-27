# REPO README - Notes for people checking out of GitLab (git)

## Getting duplicity to run:

By the numbers:

1.  Do the checkout to a location called $DUP_ROOT:
```shell
    $ git clone git@gitlab.com:duplicity/duplicity.git $DUP_ROOT 
    --or--
    $ git clone https://gitlab.com/duplicity/duplicity.git $DUP_ROOT
```
2. Build the extension module
```shell
    $ cd $DUP_ROOT
    $ ./setup.py build_ext
```
3. Run
```shell
    $ PYTHONPATH=$DUP_ROOT duplicity/__main__.py -V
````
You should see something like "duplicity 2.2.0 January 05, 2024".

Use PYTHONPATH to set the path each time that you use the binaries.
