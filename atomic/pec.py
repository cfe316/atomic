import glob

import numpy as np
from scipy.interpolate import RectBivariateSpline
import scipy.constants as constants

from adf15 import Adf15
from atomic_data import RateCoefficient


class Transition(object):
    def __init__(self, type_, element, nuclear_charge, charge, wavelength,
            temperature, density, pec):
        self.element = element
        self.nuclear_charge = nuclear_charge
        self.charge = charge

        self.wavelength = wavelength
        self.type_ = type_

        self.electron_density = density
        self.electron_temperature = temperature
        self.photon_emissivity = pec

    def interpolate(self, temperature_grid, density_grid):
        x = np.log10(self.electron_temperature)
        y = np.log10(self.electron_density)
        z = np.log10(self.photon_emissivity)

        sp = RectBivariateSpline(x, y, z)
        pec = sp(np.log10(temperature_grid), np.log10(density_grid))
        pec = 10**pec

        return self._on_new_grids(temperature_grid, density_grid, pec)

    def _on_new_grids(self, new_temperature, new_density, new_pec):
        return self.__class__(self.type_, self.element, self.nuclear_charge,
                self.charge, self.wavelength, new_temperature, new_density,
                new_pec)

    @property
    def energy(self):
        h, c = constants.h, constants.c
        lambda_ = self.wavelength
        return h * c / lambda_


class TransitionPool(object):
    def __init__(self, transitions=None):
        if transitions == None: transitions = []

        self.transitions = transitions

    @classmethod
    def from_adf15(cls, files):
        obj = cls()
        obj.append_files(files)
        return obj

    def create_atomic_data(self, ad):
        keys = [('ex', 'line_power'), ('rec', 'continuum_power'),
                ('cx', 'cx_power')]

        coeffs = {}
        for from_, to_ in keys:
            te = ad.coeffs[to_].temperature_grid
            ne = ad.coeffs[to_].density_grid
            fact = CoefficientFactory(ad, self.filter_type(from_))
            c = fact.create(te, ne)
            coeffs[to_] = c

        filtered_ad = ad.copy()
        filtered_ad.coeffs.update(coeffs)
        return filtered_ad

    def append_files(self, files):
        for f in glob.glob(files):
            self.append_file(f)

    def append_file(self, filename):
        f = Adf15(filename).read()
        element = f['element']
        nuclear_charge = f['nuclear_charge']
        charge = f['charge']
        datablocks = f['datablocks']

        for d in datablocks:
            wavelength = d['wavelength']
            temperature = d['temperature']
            density = d['density']
            pec = d['pec']
            type_ = d['type']

            t = Transition(type_, element, nuclear_charge, charge, wavelength,
                    temperature, density, pec)
            self.transitions.append(t)

    def filter_type(self, *type_names):
        names = self._interpret_type(*type_names)
        new_transitions = filter(lambda t: t.type_ in names, self.transitions)
        return self.__class__(new_transitions)

    def filter_energy(self, lo, hi, unit='eV'):
        lo_ = lo * constants.elementary_charge
        hi_ = hi * constants.elementary_charge
        in_roi = lambda t: (lo_ <= t.energy) and (t.energy < hi_)
        new_transitions = filter(in_roi, self.transitions)
        return self.__class__(new_transitions)

    def _interpret_type(self, *type_names):
        return map(self._figure_out_type, type_names)

    def _figure_out_type(self, type_):
        if type_ in ['excitation', 'excit', 'ex']:
            name = 'excit'
        elif type_ in ['recombination', 'recom', 'rec']:
            name = 'recom'
        elif type_ in ['charge_exchange', 'chexc', 'cx']:
            name = 'chexc'
        else:
            raise ValueError('invalid type: %s.' % type_)
        return name

    def sum_transitions(self):
        energies = self.energies
        coeffs = self.coeffs
        energies = energies[:, np.newaxis, np.newaxis]

        power = energies * coeffs
        power = power.sum(0)

        assert power.all() > 0

        return power

    def interpolate(self, temperature_grid, density_grid):
        new_transitions = [t.interpolate(temperature_grid, density_grid) for t
                in self.transitions]

        return self.__class__(new_transitions)

    @property
    def wavelengths(self):
        return np.array([t.wavelength for t in self.transitions])

    @property
    def energies(self):
        return np.array([t.energy for t in self.transitions])

    @property
    def coeffs(self):
        return np.array([t.photon_emissivity for t in self.transitions])

    def __iter__(self):
        return self.transitions.__iter__()

    @property
    def size(self):
        return len(self.transitions)


def P_bremsstrahlung(k, Te, ne):
    """
    W m^3
    """
    return 1.53e-38 * Te**0.5 * (k + 1)**2


from collections import defaultdict
class CoefficientFactory(object):
    def __init__(self, atomic_data, transition_pool):
        self.atomic_data = atomic_data
        self.element = atomic_data.element
        self.nuclear_charge = atomic_data.nuclear_charge
        self.transition_pool = transition_pool
        self.ionisation_stages = {}
        self.rate_coefficients = None

        self.temperature_grid = None
        self.density_grid = None

    def create(self, temperature_grid, density_grid):
        self.temperature_grid = temperature_grid
        self.density_grid = density_grid

        self._sort_by_ionisation_stages()
        self._sum_transitions()

        return self.rate_coefficients

    def _sort_by_ionisation_stages(self):
        d = defaultdict(TransitionPool)
        for t in self.transition_pool:
            if not self._conforming(t): continue

            d[t.charge].transitions.append(t)

        self.ionisation_stages.update(d)

    def _sum_transitions(self):
        coeffs = []
        for i in xrange(self.nuclear_charge):
            c = self.ionisation_stages.get(i, None)
            if c is None:
                pec = np.zeros(self.temperature_grid.shape +
                        self.density_grid.shape)
            else:
                c = c.interpolate(self.temperature_grid, self.density_grid)
                pec = c.sum_transitions()
            coeffs.append(pec)

        coeffs = np.array(coeffs)
        data = {}

        log_temperature = np.log10(self.temperature_grid)
        log_density = np.log10(self.density_grid)
        log_coeff = np.log10(coeffs)

        self.rate_coefficients = RateCoefficient(self.nuclear_charge,
                self.element, log_temperature, log_density, log_coeff)

    def _conforming(self, t):
        return t.nuclear_charge == self.nuclear_charge

