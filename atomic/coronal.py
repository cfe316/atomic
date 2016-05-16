import numpy as np

from abundance import FractionalAbundance


class CoronalEquilibrium(object):
    def __init__(self, atomic_data):
        self.atomic_data = atomic_data
        self.ionisation_coeff = atomic_data.coeffs['ionisation']
        self.recombination_coeff = atomic_data.coeffs['recombination']
        self.nuclear_charge = atomic_data.nuclear_charge

    def ionisation_stage_distribution(self, temperature, density):
        """Compute ionisation stage fractions for coronal equilibrium.

        This case only includes ionisation and recombination.
        It does not include charge exchange, or any time-dependent effects.

        Args:
            temperature (array_like): temperatures [eV].
            density (array_like): densities [m^-3].

        Returns:
            A FractionalAbundance object
        """
        if len(temperature) == 1 and len(density) > 1:
            temperature = temperature * np.ones_like(density)
        y = np.zeros((self.nuclear_charge + 1, len(temperature)))
        y[0] = np.ones_like(temperature)
        for k in xrange(self.nuclear_charge):
            S = self.ionisation_coeff(k, temperature, density)
            alpha = self.recombination_coeff(k, temperature, density)
            y[k+1] = y[k] * S / alpha

        y /= y.sum(0) # fractional abundance
        return FractionalAbundance(self.atomic_data, y, temperature, density)


if __name__ == '__main__':
    pass

