# This is meant to remake Pitcher 1997's Figure 11, 
# Radiated power coefficient L_Z for carbon as a function of electron
# temperature T_e for different values of residence parameter n_e \tau_res
#
# This appears to be the same (or nearly the same) as 
# Post 1995a (Journal of Nuclear Materials) "A review of recent
# developments in atomic processes for divertors and edge plasmas"
# Figure 17.

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


def time_dependent_z(solution, times):
    element = solution.atomic_data.element
    title = element + r' time dependent $\left<Z\right>$'

    ax = plt.gca()
    for y in solution.select_times(times):
        ax.loglog(solution.temperature, y.mean_charge(), color='black', ls='--')

    ax.set_xlabel(r'$T_\mathrm{e}\ \mathrm{(eV)}$')
    ax.set_ylim(0.4, y.atomic_data.nuclear_charge + 4)
    annotate_lines(['$10^{%d}$' % i for i in np.log10(times * solution.density)])

    z_mean = solution.y_collrad.mean_charge()
    ax.loglog(solution.temperature, z_mean, color='black')

    ax.set_title(title)


def Lz_radiated_power(rate_equations, taus):
    ax = plt.gca()
    for tau in taus:
        y = rt.solve(times, temperature, density, tau)
        rad = atomic.Radiation(y.abundances[-1])
        ax.loglog(temperature, rad.specific_power['total'],
                color='black', ls='--')

    annotate_lines(['$10^{%d}$' % i for i in np.log10(taus * rt.density)])

    power_collrad = atomic.Radiation(y.y_collrad).specific_power['total']
    ax.loglog(rate_equations.temperature, power_collrad, color='black')
    AnnotateRight(ax.lines[-1:], ['$\infty$'])

    element = 'Carbon'
    title = element + r' Lz radiated power'
    ax.set_xlabel(r'$T_\mathrm{e}\ \mathrm{(eV)}$')
    ax.set_ylabel(r'$L_z [\mathrm{W m^3}]$')
    ax.set_title(title)


if __name__ == '__main__':
    times = np.logspace(-7, 0, 100)
    temperature = np.logspace(np.log10(0.8), np.log10(3e3), 100)
    density = 1e19

    rt = atomic.RateEquationsWithDiffusion(atomic.element('carbon'))

    taus = np.logspace(13,18,6)/density

    plt.figure(1); plt.clf()
    plt.xlim(xmin=0.2, xmax=1e4)
    plt.ylim(ymin=1e-35, ymax=1e-30)
    Lz_radiated_power(rt, taus)
    plt.text(2e3,3e-31,r'$n_e \tau \; [\mathrm{m}^{-3} \, \mathrm{s}]$')
    plt.draw()

#    plt.figure(2); plt.clf()
#    time_dependent_power(y, taus)
#    plt.draw()

    plt.show()
