import os
import _xxdata_11

parameters = {
    'isdimd' : 200,
    'iddimd' : 40,
    'itdimd' : 50,
    'ndptnl' : 4,
    'ndptn' : 128,
    'ndptnc' : 256,
    'ndcnct' : 100
}

def read_scd(filename):
    fd = open(filename, 'r')

    fortran_filename = 'fort.%d' % fd.fileno()
    os.symlink(filename, fortran_filename)

    iclass = 2 # class number for scd files
    ret =  _xxdata_11.xxdata_11(fd.fileno(), iclass, **parameters)
    os.unlink(fortran_filename)
    return ret


def convert_to_dictionary(out):
    iz0, is1min, is1max, nptnl, nptn, nptnc, iptnla, iptna, iptnca, ncnct,\
    icnctv, iblmx, ismax, dnr_ele, dnr_ams, isppr, ispbr, isstgr, idmax,\
    itmax, ddens, dtev, drcof, lres, lstan, lptn = out

    d = {}
    d['charge'] = iz0
    d['density'] = ddens[:idmax]
    d['temperature'] = dtev[:itmax]
    d['number_of_charge_states'] = ismax
    d['coeff_table'] = drcof[:ismax, :itmax, :idmax]
    return d


if __name__ == '__main__':
    out = read_scd('scd96_c.dat')
    d = convert_to_dictionary(out)
