import numpy as np
from scipy.interpolate import RectBivariateSpline

import xxdata_11


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
        c = 1e6 * np.power(10, c).squeeze()
        return c


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

def _element_data(element):
    e = element.lower()
    if e in ['ar', 'argon']:
        return argon_data
    elif e in ['c', 'carbon']:
        return carbon_data


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
        alpha = RateCoefficient(xxdata_11.read_acd(acd_file))
        S = RateCoefficient(xxdata_11.read_scd(scd_file))
        return cls(d['element'], S, alpha)


class CoronalEquilibrium(object):
    def __init__(self, atomic_data):
        self.S = atomic_data.ionisation_coeff
        self.alpha = atomic_data.recombination_coeff
        self.element = atomic_data.element
        self.nuclear_charge = atomic_data.nuclear_charge

    def ionisation_stage_distribution(self, temperature, density):
        y = np.zeros((self.nuclear_charge + 1, len(temperature)))
        y[0] = np.ones_like(temperature)
        for k in xrange(self.nuclear_charge):
            S = self.S(k, temperature, density)
            alpha = self.alpha(k, temperature, density)
            y[k+1] = y[k] * S / alpha

        y /= y.sum(0) # fractional abundance
        return FractionalAbundance(y, temperature, density)


class FractionalAbundance(object):
    def __init__(self, y, temperature, density):
        self.y = y
        self.temperature = temperature
        self.density = density

    def plot_vs_temperature(self):
        from matplotlib.pyplot import gca
        ax = gca()

        ax.loglog(self.temperature, self.y.T)
        ax.set_xlabel('$T_\mathrm{e}\ [\mathrm{eV}]$')
        ax.set_ylim(0.05, 1.3)
        self._annotate_ionisation_stages(ax)

    def _annotate_ionisation_stages(self, ax):
        max_pos = self.y.argmax(axis=-1)
        for i in xrange(self.y.shape[0]):
            index = max_pos[i]
            xy = self.temperature[index], self.y[i, index]
            s = '$%d^+$' % (i,)
            ax.annotate(s, xy, ha='center')


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    ad = AtomicData.from_element('Ar')
    coronal = CoronalEquilibrium(ad)

    temperature = np.logspace(0, 5, 300)
    y = coronal.ionisation_stage_distribution(temperature, density=1e19)

    plt.figure(1); plt.clf()
    y.plot_vs_temperature()

    plt.draw()
    plt.show()
