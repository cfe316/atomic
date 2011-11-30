import numpy as np
from adf15 import Adf15


class PhotonEmissivity(object):
    def __init__(self, element, nuclear_charge, charge, datablocks):
        self.element = element
        self.nuclear_charge = nuclear_charge
        self.charge = charge
        self.datablocks = datablocks

    @classmethod
    def fromfile(cls, filename):
        f = Adf15(filename).read()
        element = f['element']
        nuclear_charge = f['nuclear_charge']
        charge = f['charge']
        datablocks = f['datablocks']

        return cls(element, charge, nuclear_charge, datablocks)

    def select_transition(self, type_):
        name = self._figure_out_type(type_)

        new_datablocks = []
        for d in self.datablocks:
            if d['transition'] != name: continue
            new_datablocks.append(d)

        return self.__class__(self.element, self.charge, self.nuclear_charge,
                new_datablocks)

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

    @property
    def wavelengths(self):
        return np.array([i['wavelength'] for i in self.datablocks])

    @property
    def density(self):
        return np.array([i['density'] for i in self.datablocks])

    @property
    def temperature(self):
        return np.array([i['temperature'] for i in self.datablocks])

    @property
    def coeffs(self):
        return np.array([i['pec'] for i in self.datablocks])


def wavelength_to_joule(lambda_):
    from scipy.constants import h, c
    return h * c / lambda_


def P_bremsstrahlung(k, Te, ne):
    """
    W m^3
    """
    return 1.53e-38 * Te**0.5 * k**2


if __name__ == '__main__':
    pec = PhotonEmissivity.fromfile('pec96#c_pju#c3.dat')

    import matplotlib.pyplot as plt

    pec = pec.select_transition('ex')
    te_ = pec.temperature
    ne_ = pec.density * 1e6
    coeffs_ = pec.coeffs * 1e-6
    w = pec.wavelengths * 1e-10
    te, ne = te_[0], ne_[0]

    energy = wavelength_to_joule(w)
    power = energy[:, np.newaxis, np.newaxis] * coeffs_
    power = power.sum(0)

    #power_brems =  P_bremsstrahlung(3, te, ne_)
    #power += power_brems[:, None]

    plt.figure(1); plt.clf()
    ax = plt.gca()
    ax.set_xlim(1e0, 1e3)


    import atomic
    ad = atomic.element('carbon')
    cont_power = ad.coeffs['continuum_power']
    line_power = ad.coeffs['line_power']
    #line_power = atomic.atomic_data.ZeroCoefficient()
    cont_power = atomic.atomic_data.ZeroCoefficient()


    for density_index in [10, 16]:
        c1 = line_power(3,te, ne[density_index])
        c2 = cont_power(3,te, ne[density_index])
        c = c1 + c2

        line, = plt.loglog(te, c, lw=2, ls='--', label='adas')
        plt.loglog(te, power[:,density_index], lw=2, color=line.get_color())
    plt.legend(loc='best')

    plt.draw()
    plt.show()
