import numpy as np
import matplotlib.pyplot as plt
import atomic


class AnnotateRight(object):
    def __init__(self, lines, texts, loc='last', ha=None, va='center'):
        self.lines = lines
        self.texts = texts
        self.location = loc

        self.ha = ha
        self.va = va

        self.axes = lines[0].axes

        self._compute_coordinates()
        self._avoid_collision()
        self._annotate()

    def _data_to_axis(self, line):
        ax = line.axes
        xy = line.get_xydata()

        xy_fig = ax.transData.transform(xy)
        xy_ax = ax.transAxes.inverted().transform(xy_fig)

        return xy_ax

    def _compute_coordinates(self):
        self.coordinates = [self._get_last_xy(l) for l in self.lines]

    def _avoid_collision(self):
        rtol = 0.02

        new_texts = []
        new_coordinates = []

        xy_last = None
        for xy, text in zip(self.coordinates, self.texts):
            if (xy_last is None) or (abs(xy_last[1] - xy[1]) > rtol):
                new_texts.append(text)
                new_coordinates.append(xy)
            else:
                new_texts[-1] = ','.join((new_texts[-1], text))
            xy_last = xy

        self.coordinates = new_coordinates
        self.texts = new_texts

    def _get_last_xy(self, line):
        if self.location == 'last':
            index = -1
        if self.location == 'first':
            index = 0
        xy_last = self._data_to_axis(line)[index]
        return xy_last

    def _annotate(self):
        deltax = 0.01
        for xy, text in zip(self.coordinates, self.texts):
            if xy[0] < 0.1:
                ha = self.ha or 'right'
            else:
                ha = self.ha or 'left'

            if ha == 'right':
                xy = xy[0] - deltax, xy[1]
            elif ha == 'left':
                xy = xy[0] + deltax, xy[1]

            va = self.va

            self.axes.annotate(text, xy, xycoords='axes fraction',
                va=va, ha=ha, size='small')


def annotate_lines(texts, **kwargs):
    ax = kwargs.pop('ax', plt.gca())
    AnnotateRight(ax.lines, texts, **kwargs)


def time_dependent_z(solution, times, ensemble_average=False):
    element = solution.atomic_data.element
    if ensemble_average:
        solution = solution.ensemble_average()
        title = element + r' ensemble averaged $\left<Z\right>$'
    else:
        title = element + r' time dependent $\left<Z\right>$'

    ax = plt.gca()
    for y in solution.select_times(times):
        ax.loglog(temperature, y.mean_charge(), color='black', ls='--')

    ax.set_xlabel(r'$T_\mathrm{e}\ \mathrm{(eV)}$')
    ax.set_ylim(0.4, y.atomic_data.nuclear_charge + 4)
    annotate_lines(['$10^{%d}$' % i for i in np.log10(times * solution.density)])

    z_mean = solution.y_coronal.mean_charge()
    ax.loglog(temperature, z_mean, color='black')

    ax.set_title(title)


def time_dependent_power(solution, times, ensemble_average=False):
    element = solution.atomic_data.element
    if ensemble_average:
        solution = solution.ensemble_average()
        title = element + r' ensemble averaged power'
    else:
        title = element + r' time dependent power'

    ax = plt.gca()
    for y in solution.select_times(times):
        rad = atomic.Radiation(y)
        ax.loglog(temperature, rad.specific_power['total'],
                color='black', ls='--')

    ax.set_xlabel(r'$T_\mathrm{e}\ \mathrm{(eV)}$')
    ax.set_ylabel(r'$P/n_\mathrm{i} n_\mathrm{e}\ [\mathrm{W m^3}]$')
    annotate_lines(['$10^{%d}$' % i for i in np.log10(times * solution.density)])

    power_coronal = atomic.Radiation(solution.y_coronal).specific_power['total']
    ax.loglog(temperature, power_coronal, color='black')

    ax.set_title(title)


if __name__ == '__main__':
    times = np.logspace(-7, 0, 100)
    temperature = np.logspace(0, 3, 100)
    density = 1e19

    rt = atomic.RateEquations(atomic.element('carbon'))
    y = rt.solve(times, temperature, density)

    taus = np.array([ 1e14, 1e15, 1e16, 1e17, 1e18])/density

    plt.figure(1); plt.clf()
    time_dependent_z(y, taus)
    plt.draw()

    plt.figure(2); plt.clf()
    time_dependent_power(y, taus)
    plt.draw()

    plt.figure(3); plt.clf()
    time_dependent_z(y, taus, ensemble_average=True)
    plt.draw()

    plt.figure(4); plt.clf()
    time_dependent_power(y, taus, ensemble_average=True)
    plt.draw()

    plt.show()
