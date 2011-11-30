"""
This module contains an interface to the Adas Data File type 15 (ADF 15),
that contain Photon Emissivity Coefficients (PEC). See [1] for an example
file.

[1] http://www.adas.ac.uk/man/appxa-15.pdf
"""
import os
import _xxdata_15

# Some hard coded parameters to run src/xxdata_15/xxdata_15.for routine.  The
# values have been take from src/xxdata_15/test.for, and should be OK for
# all files.
parameters = {
    'nstore' : 500,
    'nddim' : 50,
    'ntdim' : 40,
    'ndptnl' : 4,
    'ndptn' : 128,
    'ndptnc' : 256,
    'ndcnct' : 100,
    'ndstack' : 40,
    'ndcmt' : 2000,
}

class Adf15(object):
    def __init__(self, name):
        if not os.path.isfile(name):
            raise IOError("no such file: '%s'" % name)

        self.name = name

    def read(self):
        self._read_xxdata_15()
        return self._convert_to_dictionary()

    def _read_xxdata_15(self):
        iunit = _xxdata_15.helper_open_file(self.name)
        dsname = os.path.basename(self.name)
        ret =  _xxdata_15.xxdata_15(iunit, dsname, **parameters)
        _xxdata_15.helper_close_file(iunit)

        self._raw_return_value = ret

    def _convert_to_dictionary(self):
        ret = self._raw_return_value
        iz0, is_, is1, esym, nptnl, nptn, nptnc, iptnla, iptna, iptnca,\
                ncnct, icnctv, ncptn_stack, cptn_stack, lres, lptn, lcmt,\
                lsup, nbsel, isela, cwavel, cfile, ctype, cindm, wavel,\
                ispbr, isppr, isstgr, iszr, ita, ida, teta, teda, pec,\
                pec_max, ncmt_stack, cmt_stack = ret

        d = {}
        d['nuclear_charge'] = iz0
        d['charge'] = is_
        d['charge+1'] = is1
        d['element'] = esym.strip()
        d['partition_levels'] = nptnl
        d['partial_file'] = bool(lres)
        d['partial_block_present'] = bool(lptn)
        d['comment_text_block_present'] = bool(lcmt)

        n_datablocks = nbsel
        n_densities = ita
        n_temperatures = ida
        densities = teta
        temperatures = teda
        pec = pec
        wavelengths = wavel
        transition_types = ctype.T.reshape(-1, 8)


        datablocks = []
        for i in xrange(n_datablocks):
            b = {}
            nd, nt = n_densities[i], n_temperatures[i]
            b['density'] = densities[:nd,i]
            b['temperature'] = temperatures[:nt,i]
            b['pec'] = pec[:nt, :nd, i]
            b['wavelength'] = wavelengths[i]
            b['transition'] = ''.join(transition_types[i]).strip()

            datablocks.append(b)

        d['datablocks'] = datablocks
        return d


if __name__ == '__main__':
    out = Adf15('src/xxdata_15/test.dat').read()
