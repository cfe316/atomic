import numpy as np

from abundance import FractionalAbundance


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


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from atomic_data import AtomicData

    ad = AtomicData.from_element('Ar')
    coronal = CoronalEquilibrium(ad)

    temperature = np.logspace(0, 5, 300)
    y = coronal.ionisation_stage_distribution(temperature, density=1e19)

    plt.figure(1); plt.clf()
    y.plot_vs_temperature()

    plt.draw()
    plt.show()
