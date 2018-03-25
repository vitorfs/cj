CJ
==

Personal collection of command line utilities. I usually add more functions as
I need them. No particular subject.

The idea of this package is to be self-contained and easily installed in any
unix-like system. It should also be safe to install it globally without a
virtual environment. For that matter, I try to avoid at all cost using
external Python dependencies and using Python 3 specific features.

The usage varies from command-line utilities, automation scripts to cron tasks.

Installation
------------

Using `pip`:

.. code-block:: console

    pip install cj

Usage
-----

.. code-block:: console

    cj COMMAND

Examples
~~~~~~~~

Backup a Wordpress site:

.. code-block:: console

    cj wp

Compress a folder:

.. code-block:: console

    cj zip foldername/

License
-------

The source code is released under the `MIT License <https://github.com/vitorfs/cj/blob/master/LICENSE>`_.
