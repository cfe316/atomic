import numpy as np


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

    def plot_vs_temperature(self, **kwargs):
        from matplotlib.pyplot import gca
        ax = gca()

        ax.loglog(self.temperature, self.y.T, **kwargs)
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
    from atomic_data import AtomicData

    ad = AtomicData.from_element('Ar')
    coronal = CoronalEquilibrium(ad)

    temperature = np.logspace(0, 5, 300)
    y = coronal.ionisation_stage_distribution(temperature, density=1e19)

    plt.figure(1); plt.clf()
    y.plot_vs_temperature()

    plt.draw()
    plt.show()
