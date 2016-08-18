import numpy as np


class FractionalAbundance(object):
    """An array of ionisation stage fractions over density and/or temperature.

    Attributes:
        atomic_data (AtomicData): used by Radiation class
            to get various coefficients.
        y (np.array, 2D): stores the fractional abundance of each
            ionisation stage, k=0 to Z, for each point
            of the given temperatures and densities.
            Shape is (Z+1,x)
        temperature (array_like): list of temperatures [eV]
        density (array_like): list of densities [m^-3]
    """
    def __init__(self, atomic_data, y, temperature, density):
        self.atomic_data = atomic_data
        self.y = y # fractional abundances of each charge state
        self.temperature = temperature
        self.density = density

    def mean_charge(self):
        """
        Compute the mean charge:
            <Z> = sum_k ( y_k * k )

        Assumes that y is a 2D array with shape
        (nuclear_charge+1,# of temperatures)

        Returns:
            An np.array of mean charge.
        """

        # make a 2D array [[0],[1],[2],...]
        k = np.arange(self.y.shape[0])
        k = k[:,np.newaxis]

        z_mean = np.sum(self.y * k, axis=0)
        return z_mean

    def effective_charge(self, impurity_fraction, ion_density=None):
        """
        Compute the effective charge:

                    n_i + n_I <Z**2>
            Z_eff = ----------------
                          n_e

        using the approximation <Z**2> = <Z>**2.

        Assumes the main ion has charge +1.

        Returns:
            An np.array of Zeff
        """
        if ion_density is None:
            ion_density = self.density

        impurity_density = impurity_fraction * self.density

        z_mean = self.mean_charge()
        zeff = (ion_density + impurity_density * z_mean**2) / self.density

        return zeff

    def plot_vs_temperature(self, **kwargs):
        """Use Matplotlib to plot the abundance of each stage at each point.

        If the points all have the same temperature but different density,
        this won't work.
        """

        import matplotlib.pyplot as plt
        ax = kwargs.pop('ax', plt.gca())

        lines = ax.loglog(self.temperature, self.y.T, **kwargs)
        ax.set_xlabel('$T_\mathrm{e}\ [\mathrm{eV}]$')
        ax.set_ylim(0.05, 1.3)
        self.annotate_ionisation_stages(lines)
        plt.draw_if_interactive()

        return lines

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

    def replot_colored(self, line, lines_ref):
        """
        Replot a line, colored according the most abundant state.
        """
        ax = line.axes
        x = line.get_xdata()
        y = line.get_ydata()

        lines = []
        imax = np.argmax(self.y, axis=0)
        for i, line_ref in enumerate(lines_ref):
            mask = imax == i
            lines.append(ax.plot(x[mask], y[mask], color=line_ref.get_color()))

