import numpy as np

from atomic_data import ZeroCoefficient


class Radiation(object):
    def __init__(self, ionisation_stage_distribution, impurity_fraction=1.,
            neutral_fraction=0.):
        self.y = ionisation_stage_distribution
        self.atomic_data = ionisation_stage_distribution.atomic_data

        self.temperature = self.y.temperature
        self.electron_density = self.y.density

        self.neutral_fraction = neutral_fraction
        self.impurity_fraction = impurity_fraction

        self.power = self._compute_power()

    def get_impurity_density(self):
        return self.impurity_fraction * self.electron_density

    def get_neutral_density(self):
        return self.neutral_fraction * self.electron_density

    def _get_power_coeffs(self):
        power_coeffs = {}
        for key in ['line_power', 'continuum_power', 'cx_power']:
            power_coeffs[key] = self.atomic_data.coeffs.get(key,
                    ZeroCoefficient())
        return power_coeffs

    def _compute_power(self):
        """
        Compute radiation power density in [W/m3].
        """
        shape_ = self.atomic_data.nuclear_charge, self.temperature.shape[0]

        power_coeffs = self._get_power_coeffs()
        radiation_power = {}
        for key in power_coeffs.keys():
            radiation_power[key] = np.zeros(shape_)

        ne = self.electron_density
        ni = self.get_impurity_density()
        n0 = self.get_neutral_density()
        y = self.y

        for k in xrange(self.atomic_data.nuclear_charge):
            for key in radiation_power.keys():
                coeff = power_coeffs[key](k, self.temperature,
                        self.electron_density)

                if key in ['continuum_power', 'line_power']:
                    scale = ne * ni * y.y[k]
                elif key in ['cx_power']:
                    scale = n0 * ni * y.y[k]

                radiation_power[key][k] = scale * coeff

        # compute the total power
        radiation_power['total'] = reduce(lambda x,y: x+y,
                radiation_power.values())

        # sum over all ionisation stages
        for key in radiation_power.keys():
            radiation_power[key] = radiation_power[key].sum(0)

        return radiation_power

    def plot(self, **kwargs):
        import matplotlib.pyplot as plt
        ax = kwargs.get('ax', plt.gca())

        lines = []
        for key in ['line_power', 'continuum_power', 'cx_power', 'total']:
            p = self.power[key]
            l, = ax.loglog(self.temperature, p, label=self._get_label(key))
            lines.append(l)

        plt.xlabel(r'$T_\mathrm{e}\ [\mathrm{eV}]$')
        plt.ylabel(r'$P\ [\mathrm{W/m^3}]$')

        self._decorate_plot(ax, lines)
        plt.draw_if_interactive()

        return lines

    def _decorate_plot(self, ax, lines):
        alpha = 0.5 # transparency for fancy filling
        min_ = ax.get_ylim()[0]
        baseline = min_ * np.ones_like(self.temperature)

        for line in lines[:-1]:
            x = line.get_xdata()
            y = line.get_ydata()
            ax.fill_between(x, y, baseline, color=line.get_color(), alpha=alpha)
        lines[-1].set_color('black')

    def _get_label(self, key):
        labels = {
            'continuum_power' : 'continuum',
            'line_power' : 'line',
            'cx_power' : 'charge-exchange',
            'total' : 'total',
        }
        return labels.get(key, None)

