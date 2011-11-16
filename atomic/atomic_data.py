import os

import numpy as np
from scipy.interpolate import RectBivariateSpline

import xxdata_11


argon_data = {
    'element' : 'Ar',
    'ionisation_coeff' : 'scd89_ar.dat',
    'recombination_coeff' : 'acd89_ar.dat',
}

carbon_data = {
    'element' : 'C',
    'ionisation_coeff' : 'scd96_c.dat',
    'recombination_coeff' : 'acd96_c.dat',
}

neon_data = {
    'element' : 'Ne',
    'ionisation_coeff' : 'scd96_ne.dat',
    'recombination_coeff' : 'acd96_ne.dat',
}

def _element_data(element):
    e = element.lower()
    if e in ['ar', 'argon']:
        return argon_data
    elif e in ['c', 'carbon']:
        return carbon_data
    elif e in ['ne', 'neon']:
        return neon_data
    else:
        raise NotImplementedError('unknown element: %s' % element)


def _full_path(file_):
    """ Figure out the location of the atomic datafiles. """
    module_path = os.path.dirname(os.path.realpath( __file__ ))
    return os.path.join(module_path, '..', 'atomic_data', file_)


class AtomicData(object):
    def __init__(self, element, ionisation_coeff, recombination_coeff):
        self.element = element
        self.nuclear_charge = ionisation_coeff.nuclear_charge
        self.ionisation_coeff = ionisation_coeff
        self.recombination_coeff = recombination_coeff

        self._check_consistency()

    def _check_consistency(self):
        if self.ionisation_coeff.nuclear_charge !=\
            self.recombination_coeff.nuclear_charge:
                raise ValueError('inconsistent coefficients.')

    @classmethod
    def from_element(cls, element):
        d = _element_data(element)

        acd_file = d['recombination_coeff']
        scd_file = d['ionisation_coeff']
        alpha = RateCoefficient(xxdata_11.read_acd(_full_path(acd_file)))
        S = RateCoefficient(xxdata_11.read_scd(_full_path(scd_file)))
        return cls(d['element'], S, alpha)


class RateCoefficient(object):
    def __init__(self, adf11_data):
        self.nuclear_charge = adf11_data['charge']
        self.log_temperature = adf11_data['temperature']
        self.log_density = adf11_data['density']
        self.log_coeff = adf11_data['coeff_table']

        self._compute_interpolating_splines()

    def _compute_interpolating_splines(self):
        self.splines = []
        for k in xrange(self.nuclear_charge):
            x = self.log_temperature
            y = self.log_density
            z = self.log_coeff[k]
            self.splines.append(RectBivariateSpline(x, y, z))

    def __call__(self, k, Te, ne):
        """
        Evaulate the ionisation/recombination coefficients of k'th atomic state
        at a given temperature and density.

        Parameters
        ----------
        Te : array_like
            Temperature in [eV].
        ne : array_like
            Density in [m-3].

        Returns
        -------
        c : array_like
            Rate coefficent in [m3/s].
        """
        log_temperature = np.log10(Te)
        log_density = np.log10(ne * 1e-6)

        c = self.splines[k](log_temperature, log_density)
        c = 1e-6 * np.power(10, c).squeeze()
        return c
