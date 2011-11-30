import numpy as np
from adf15 import Adf15

class Transition(object):
    def __init__(self, element, nuclear_charge, charge, datablock):
        self.element = element
        self.nuclear_charge = nuclear_charge
        self.charge = charge

        self.wavelength = datablock['wavelength'] * 1e-10
        self.type_ = datablock['type']

        self.electron_density = datablock['density'] * 1e6
        self.electron_temperature = datablock['temperature']
        self.photon_emissivity = datablock['pec'] * 1e-6


class PhotonEmissivity(object):
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
            t = Transition(element, nuclear_charge, charge, d)
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

        return power

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


def wavelength_to_joule(lambda_):
    from scipy.constants import h, c
    return h * c / lambda_


def P_bremsstrahlung(k, Te, ne):
    """
    W m^3
    """
    return 1.53e-38 * Te**0.5 * k**2


if __name__ == '__main__':
    pec = PhotonEmissivity()
    pec.append_file('pec96#c_pju#c3.dat')

    power = pec.filter_type('rec', 'ex').sum_transitions()
    te = pec.transitions[0].electron_temperature
    ne = pec.transitions[0].electron_density

    import atomic
    ad = atomic.element('carbon')
    cont_power = ad.coeffs['continuum_power']
    line_power = ad.coeffs['line_power']
    #line_power = atomic.atomic_data.ZeroCoefficient()
    #cont_power = atomic.atomic_data.ZeroCoefficient()

    import matplotlib.pyplot as plt
    plt.figure(1); plt.clf()
    ax = plt.gca()
    ax.set_xlim(1e0, 1e3)

    densities = [1e18, 1e19, 1e20]
    for density_index in np.searchsorted(ne, densities):
        c1 = line_power(3,te, ne[density_index])
        c2 = cont_power(3,te, ne[density_index])
        c = c1 + c2
        label = r'$n_\mathrm{e} = 10^{%d}\ \mathrm{m^{-3}}$' %\
            np.log10(ne[density_index])
        line, = plt.loglog(te, c, 'o')
        plt.loglog(te, power[:,density_index], color=line.get_color(),
                label=label)
    plt.legend(loc='best')

    plt.draw()
    plt.show()
