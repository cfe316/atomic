Atomic
======

Atomic is a set of tools to calculate fractional abundance and radiation of
different elements in hot plasmas.

Requirements
------------

- python3
- scipy, numpy, matplotlib
- f2py
- a Fortran compiler. For me, f2py appears to use gfortran:f77.


Installation and running the code
---------------------------------

Required data files and code from OPEN-ADAS:

    $ ./fetch_adas_data # fetch the atomic data and reading routines
    $ python3 setup.py build_ext --inplace # to compile the extension module

See below for details.

Try one of the examples:

    $ python3 examples/radiation.py

Or launch `jupyter notebook` (with a python3 kernel):
(in the notebook)
    
    >>> %run examples/radiation.py

Fetching the atomic data
------------------------

Atomic needs atomic data ionisation/recombination etc. coefficients, as well as
the routines to read them. These are fetched from the OpenADAS [1] website.
In order to download your own dataset and reading routines
run the python script:

    $ ./fetch_adas_data

It will download files to a folder called `adas_data`.

For description of these so called iso-nuclear master files see [2].

The routines to download are 

http://open.adas.ac.uk/codes/xxdata_11.tar.gz and 
http://open.adas.ac.uk/codes/xxdata_15.tar.gz 

and should be put in the src folder and unzipped to

    src/xxdata_11
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
These clean up the effects of source file downloads and Fortran compliation from the above setup.py command.
Recompiling is necessary after these commands.

    $ rm -r build/ src/xxdata_11 src/xxdata_15
    $ rm atomic/_xxdata_* src/*.gz src/*.c


References
----------

[1] http://open.adas.ac.uk
[2] http://www.adas.ac.uk/man/chap4-04.pdf

