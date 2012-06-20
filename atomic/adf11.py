"""
This module contains an interface to the Adas Data File type 11 (ADF 11), so
called Iso-nuclear master files.  See [1] for an example file and [2] for
detailed description of the possible subclasses.

[1] http://www.adas.ac.uk/man/appxa-11.pdf
[2] http://www.adas.ac.uk/man/chap4-04.pdf
"""
import os
import _xxdata_11


# Supported adf11 data classes.  See src/xxdata_11/xxdata_11.for for all the
# twelve classes.
adf11_classes = {
    'acd' : 1, # recombination coefficients
    'scd' : 2, # ionisation coefficients
    'prb' : 4, # continuum radiation power
    'plt' : 8, # line radiation power
    'prc' : 5, # charge-exchange recombination radiation
}


# Some hard coded parameters to run xxdata_11.for routine.  The values have
# been take from src/xxdata_11/test.for, and should be OK for all files.
parameters = {
    'isdimd' : 200,
    'iddimd' : 40,
    'itdimd' : 50,
    'ndptnl' : 4,
    'ndptn' : 128,
    'ndptnc' : 256,
    'ndcnct' : 100
}


class Adf11(object):
    def __init__(self, name):
        if not os.path.isfile(name):
            raise IOError("no such file: '%s'" % name)

        self.name = name

    def read(self, class_=None):
        if class_ == None:
            self._sniff_class()
        self._read_xxdata_11()
        return self._convert_to_dictionary()

    def _read_xxdata_11(self):
        null_fds = os.open(os.devnull, os.O_RDWR)
        save = os.dup(1)
        os.dup2(null_fds, 1)

        iclass = adf11_classes[self.class_]
        iunit = _xxdata_11.helper_open_file(self.name)
        ret =  _xxdata_11.xxdata_11(iunit, iclass, **parameters)
        _xxdata_11.helper_close_file(iunit)

        self._raw_return_value = ret

        os.dup2(save, 1) # restore stdout
        os.close(null_fds) # close the temporary fds

    def _convert_to_dictionary(self):
        ret = self._raw_return_value
        iz0, is1min, is1max, nptnl, nptn, nptnc, iptnla, iptna, iptnca, ncnct,\
        icnctv, iblmx, ismax, dnr_ele, dnr_ams, isppr, ispbr, isstgr, idmax,\
        itmax, ddens, dtev, drcof, lres, lstan, lptn = ret

        d = {}
        d['charge'] = iz0
        d['log_density'] = ddens[:idmax]
        d['log_temperature'] = dtev[:itmax]
        d['number_of_charge_states'] = ismax
        d['log_coeff'] = drcof[:ismax, :itmax, :idmax]

        d['class'] = self.class_
        d['element'] = self.element
        d['name'] = self.name

        # convert everything to SI + eV units
        d['log_density'] += 6 # log(cm^-3) = log(10^6 m^-3) = 6 + log(m^-3)
        d['log_coeff'] -= 6 # log(m^3/s) = log(10^-6 m^3/s) = -6 + log(m^3/s)
        return d

    def _sniff_class(self):
        s = Sniffer(self.name)
        if s.class_ not in adf11_classes:
            raise NotImplementedError('unknown adf11 class: %s' % s.class_)
        self.class_ = s.class_
        self.element = s.element


class Sniffer(object):
    def __init__(self, file_):
        self.file_ = file_
        self.name = os.path.basename(file_)

        self._sniff_name()
        self._check()

    def _sniff_name(self):
        name, extension = self.name.split(os.path.extsep)

        type_, element = name.split('_')
        class_ = type_[:3]
        year = type_[3:]
        resolved = year.endswith('r')

        self.element = element
        self.year = year
        self.class_ = class_
        self.extension = extension
        self.resolved = resolved

    def _check(self):
        assert self.extension == 'dat'
        assert self.resolved == False, 'metastable resolved data not supported.'


if __name__ == '__main__':
    out = Adf11('adas_data/scd96_c.dat').read()
