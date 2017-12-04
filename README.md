Atomic
======

Atomic is a set of tools to calculate fractional abundance and radiation of
different elements in hot plasmas.


Installation and running the code
---------------------------------

Required code from OPEN-ADAS:

    $ ./fetch_adas_data # fetch the atomic data and reading routines
    $ python3 setup.py build_ext --inplace # to compile the extension module

See below for details.

Launch ipython and try out the examples:

    $ ipython

    (in ipython) >>> %run examples/radiation.py



Fetching the atomic data
------------------------

Atomic needs atomic data ionisation/recombination etc. coefficients, as well as
the routines to read them. These are fetched from the OpenADAS [1] website.
In order to download your own dataset and reading routines
run:

    $ ./fetch_adas_data

For description of these so called iso-nuclear master files see [2].

The routines to download are 

http://open.adas.ac.uk/codes/xxdata_11.tar.gz and 
http://open.adas.ac.uk/codes/xxdata_15.tar.gz 

and should be put in the src folder and unzipped like 

src/xxdata_11 and
src/xxdata_15.


Compiling python extension module
---------------------------------

The extension module is compiled using numpy.distutils:

    $ python3 setup.py build_ext --inplace


Testing
-------

Have nose2 installed.

    $ nose2

Test boilerplate was first produced automatedly with pythoscope, so
at time of writing (20160916) many tests are skipped. (S)


Cleaning
--------

    $ rm -r build/ src/xxdata_11 src/xxdata_15
    $ rm atomic/_xxdata_* src/*.gz src/*.c


References
----------

[1] http://open.adas.ac.uk
[2] http://www.adas.ac.uk/man/chap4-04.pdf

