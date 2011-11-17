import numpy as np


class FractionalAbundance(object):
    def __init__(self, atomic_data, y, temperature, density):
        self.atomic_data = atomic_data
        self.y = y
        self.temperature = temperature
        self.density = density

    def mean_charge(self):
        """
        Compute the mean charge:
            <Z> = sum_k ( y_k * k )
        """

        k = np.arange(self.y.shape[0])
        k = k[:,np.newaxis]

        z_mean = np.sum(self.y * k, axis=0)
        return z_mean

    def plot_vs_temperature(self, **kwargs):
        import matplotlib.pyplot as plt
        ax = plt.gca()

        ax.loglog(self.temperature, self.y.T, **kwargs)
        ax.set_xlabel('$T_\mathrm{e}\ [\mathrm{eV}]$')
        ax.set_ylim(0.05, 1.3)
        self._annotate_ionisation_stages(ax)
        plt.draw_if_interactive()

    def _annotate_ionisation_stages(self, ax):
        max_pos = self.y.argmax(axis=-1)
        for i in xrange(self.y.shape[0]):
            index = max_pos[i]
            xy = self.temperature[index], self.y[i, index]
            s = '$%d^+$' % (i,)
            ax.annotate(s, xy, ha='center')


