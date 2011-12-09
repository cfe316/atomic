import numpy as np
from scipy.interpolate import RectBivariateSpline

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


class TransitionPool(object):
    def __init__(self, transitions=None):
        if transitions == None: transitions = []

        self.transitions = transitions

    def append_file(self, filename):
        f = Adf15(filename).read()
        element = f['element']
        nuclear_charge = f['nuclear_charge']
        charge = f['charge']
        datablocks = f['datablocks']

        for d in datablocks:
            wavelength = d['wavelength'] * 1e-10
            temperature = d['temperature']
            density = d['density'] * 1e6
            pec = d['pec'] * 1e-6
            type_ = d['type']

            t = Transition(type_, element, nuclear_charge, charge, wavelength,
                    temperature, density, pec)
            self.transitions.append(t)

    def filter_type(self, *type_names):
        names = self._interpret_type(*type_names)
        new_transitions = filter(lambda t: t.type_ in names, self.transitions)
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
        energies = wavelength_to_joule(self.wavelengths)
        energies = energies[:, np.newaxis, np.newaxis]
        coeffs = self.coeffs

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
    def electron_densities(self):
        return np.array([t.electron_density for t in self.transitions])

    @property
    def electron_temperatures(self):
        return np.array([t.electron_temperature for t in self.transitions])

    @property
    def coeffs(self):
        return np.array([t.photon_emissivity for t in self.transitions])

    def __iter__(self):
        return self.transitions.__iter__()


def wavelength_to_joule(lambda_):
    from scipy.constants import h, c
    return h * c / lambda_


def P_bremsstrahlung(k, Te, ne):
    """
    W m^3
    """
    return 1.53e-38 * Te**0.5 * k**2


def fetch_pec_data():
    from atomic.adas import OpenAdas
    db = OpenAdas()
    res = db.search_adf15('carbon')
    for r in res:
        db.fetch(r, 'adas_data/pec')


from collections import defaultdict
class CoefficientFactory(object):
    def __init__(self, element, nuclear_charge, transition_pool):
        self.element = element
        self.nuclear_charge = nuclear_charge
        self.transition_pool = transition_pool
        self.ionisation_stages = {}

    def create(self, temperature_grid, density_grid):
        self._sort_by_ionisation_stages()

        coeffs = []
        for i in xrange(self.nuclear_charge):
            c = self.ionisation_stages[i]
            c = c.interpolate(temperature_grid, density_grid)
            pec = c.sum_transitions()
            try:
                assert np.all(pec > 0), '%s' % i
            except AssertionError:
                import pdb; pdb.set_trace()
            coeffs.append(pec)

        coeffs = np.array(coeffs)
        data = {}
        data['charge'] = self.nuclear_charge
        data['element'] = self.element
        data['name'] = 'custom' # FIXME
        data['temperature'] = np.log10(temperature_grid)
        data['density'] = np.log10(density_grid * 1e-6)
        data['coeff_table'] = np.log10(coeffs * 1e6)
    
        return RateCoefficient(data)

    def _sort_by_ionisation_stages(self):
        d = defaultdict(TransitionPool)
        for t in self.transition_pool:
            if not self._conforming(t): continue

            d[t.charge].transitions.append(t)

        self.ionisation_stages.update(d)

    def _conforming(self, t):
        return t.nuclear_charge == self.nuclear_charge


if __name__ == '__main__':
    pec = TransitionPool()

    import glob

    for f in glob.glob('adas_data/pec/pec96#c_pju*.dat'):
        pec.append_file(f)

    te = np.logspace(0, 4)
    ne = np.logspace(18, 20)

    fact = CoefficientFactory('C', 6, pec.filter_type('ex'))
    coeff_line_power = fact.create(te, ne)

    fact = CoefficientFactory('C', 6, pec.filter_type('rec'))
    coeff_cont_power = fact.create(te, ne)

    import atomic
    ad = atomic.element('carbon')
    cont_power = ad.coeffs['continuum_power']
    line_power = ad.coeffs['line_power']

    import matplotlib.pyplot as plt
    plt.figure(1); plt.clf()
    ax = plt.gca()
    ax.set_xlim(1e0, 1e3)

    densities = [1e18, 1e19, 1e20]
    densities = [1e19]
    charge = 1
    for density_index in np.searchsorted(ne, densities):
        c1 = line_power(charge, te, ne[density_index])
        c2 = cont_power(charge, te, ne[density_index])

        mc1 = coeff_line_power(charge, te, ne[density_index])
        mc2 = coeff_cont_power(charge, te, ne[density_index])

        label = r'$n_\mathrm{e} = 10^{%d}\ \mathrm{m^{-3}}$' %\
            np.log10(ne[density_index])

        line, = plt.loglog(te, mc1, '+')
        plt.loglog(te, c1, color=line.get_color(), label=label)

        bremss = P_bremsstrahlung(charge, te, ne[density_index])
        line, = plt.loglog(te, mc2 + bremss, 'o')
        plt.loglog(te, c2, color=line.get_color(), label=label)

    #plt.legend(loc='best')
    plt.draw()
    plt.show()
