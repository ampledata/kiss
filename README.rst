KISS Protocol implementation in Python
**************************************

A pure-Python implementation of the KISS Protocol for communicating with
serial TNC devices for use with Amateur Radio.

Installation
============
Install from pypi using pip: ``pip install kiss``


Usage Example
=============
Read & print frames from a TNC connected to '/dev/ttyUSB0' at 1200 baud::

    import kiss

    k = kiss.KISS('/dev/ttyUSB0', 1200)
    k.start()  # inits the TNC, optionally passes KISS config flags.
    k.read(callback=print)


See also: examples/ directory.


Testing
=======
Run nosetests from a Makefile target::

    make test


Inspiration
===========
Inspiration for this project came from:

* HA5DI's dixprs_: A Python APRS project with KISS, digipeater, et al., support.
* GE0RG's APRSDroid_: A Java/Scala Android APRS App.
* KA2DDO's YAAC_: A Java APRS app.
* aprs.fi_'s Ham-APRS-FAP_: A Perl APRS parser.

.. _dixprs: https://sites.google.com/site/dixprs/
.. _aprsdroid: http://aprsdroid.org/
.. _YAAC: http://www.ka2ddo.org/ka2ddo/YAAC.html
.. _aprs.fi: http://search.cpan.org/dist/Ham-APRS-FAP/
.. _Ham-APRS-FAP: http://search.cpan.org/dist/Ham-APRS-FAP/


Build Status
============

Master:

.. image:: https://travis-ci.org/ampledata/aprs.svg?branch=master
    :target: https://travis-ci.org/ampledata/aprs


Source
======
https://github.com/ampledata/kiss


Author
======
Greg Albrecht W2GMD gba@orionlabs.io

http://ampledata.org/


Copyright
=========
Copyright 2016 Orion Labs, Inc. and Contributors


License
=======
Apache License, Version 2.0. See LICENSE for details.
