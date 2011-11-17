import numpy as np

from abundance import FractionalAbundance


class CoronalEquilibrium(object):
    def __init__(self, atomic_data):
        self.atomic_data = atomic_data
        self.ionisation_coeff = atomic_data.ionisation_coeff
        self.recombination_coeff = atomic_data.recombination_coeff
        self.nuclear_charge = atomic_data.nuclear_charge

    def ionisation_stage_distribution(self, temperature, density):
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

