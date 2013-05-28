pep438
======

.. image:: https://secure.travis-ci.org/treyhunner/pep438.png?branch=master
   :target: http://travis-ci.org/treyhunner/pep438
.. image:: https://coveralls.io/repos/treyhunner/pep438/badge.png?branch=master
   :target: https://coveralls.io/r/treyhunner/pep438
.. image:: https://pypip.in/v/pep438/badge.png
   :target: https://crate.io/packages/pep438
.. image:: https://pypip.in/d/pep438/badge.png
   :target: https://crate.io/packages/pep438


Check packages in your requirements file for proper usage of the `PEP 438`_ tools.

This `online PEP 438 checker`_ is also great.

Installation
------------

The script is `available on PyPI`_.  To install with pip:

.. code-block:: bash

    $ sudo pip install pep438

Usage
-----

Check individual packages:

.. code-block:: bash

    $ pep438 django pillow
    ✓ django: 0 links
    ✗ pillow: 360 links

Check requirements file:

.. code-block:: bash

    $ pep438 -r requirements.txt
    ✓ django: 0 links
    ✗ south: 1 links
    ✓ django-model-utils: 0 links
    ✓ django-simple-history: 0 links
    ✓ django-email-log: 0 links

Check piped input:

.. code-block:: bash

    $ cat *-requirements.txt | pep438
    ✓ django: 0 links
    ✗ south: 1 links
    ✓ django-model-utils: 0 links
    ✓ django-simple-history: 0 links
    ✓ django-email-log: 0 links


Contributing
------------

Pull requests are welcome.  Please read the CONTRIBUTING file for tips on
submitting pull requests.


License
-------

This project is released under an `MIT License`_.

.. _pep 438: http://www.python.org/dev/peps/pep-0438/
.. _mit license: http://th.mit-license.org/2013
.. _available on PyPI: http://pypi.python.org/pypi/pep438/
.. _online pep 438 checker: http://pypi-externals.caremad.io/
