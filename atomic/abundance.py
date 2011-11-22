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

        lines = ax.loglog(self.temperature, self.y.T, **kwargs)
        ax.set_xlabel('$T_\mathrm{e}\ [\mathrm{eV}]$')
        ax.set_ylim(0.05, 1.3)
        self.annotate_ionisation_stages(lines)
        plt.draw_if_interactive()

    def annotate_ionisation_stages(self, lines):
        max_pos = self.y.argmax(axis=-1)
        for i, l in enumerate(lines):
            x = l.get_xdata()
            y = l.get_ydata()
            index = y.argmax()
            xy = x[index], y[index]
            s = '$%d^+$' % (i,)
            l.axes.annotate(s, xy, ha='center', color=l.get_color())


