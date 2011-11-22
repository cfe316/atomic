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
        for i, l in enumerate(lines):
            x = l.get_xdata()
            y = l.get_ydata()
            ax = l.axes

            maxpos = y.argmax()
            xy = x[maxpos], y[maxpos]
            xy = self._reposition_annotation(ax, xy)
            s = '$%d^+$' % (i,)
            ax.annotate(s, xy, ha='left', va='bottom', color=l.get_color())

    def _reposition_annotation(self, ax, xy):
            xy_fig = ax.transData.transform_point(xy)
            xl, yl = ax.transAxes.inverted().transform(xy_fig)

            min_x, max_x = 0.01, 0.95
            if xl < min_x:
                xy = ax.transAxes.transform_point((min_x, yl))
                xy = ax.transData.inverted().transform_point(xy)
            if xl > max_x:
                xy = ax.transAxes.transform_point((max_x, yl))
                xy = ax.transData.inverted().transform_point(xy)

            return xy


