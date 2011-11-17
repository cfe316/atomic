import _xxdata_11

adf11_classes = {
    'acd' : 1, # recombination coefficients
    'scd' : 2, # ionisation coefficients
    'prb' : 4, # continuum radiation power
    'plt' : 8, # line radiation power
    'prc' : 5, # charge-exchange recombination radiation
}

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
    return read_adf11(filename, class_='scd')


def read_acd(filename):
    return read_adf11(filename, class_='acd')

def read_prb(filename):
    return read_adf11(filename, class_='prb')

def read_plt(filename):
    return read_adf11(filename, class_='plt')

def read_prc(filename):
    return read_adf11(filename, class_='prc')

def read_adf11(name, class_):
    if class_ not in adf11_classes:
        raise NotImplementedError('unknown adf11 class: %s' % class_)

    iclass = adf11_classes[class_]
    iunit = _xxdata_11.helper_open_file(name)
    ret =  _xxdata_11.xxdata_11(iunit, iclass, **parameters)
    _xxdata_11.helper_close_file(iunit)
    return convert_to_dictionary(ret)


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
