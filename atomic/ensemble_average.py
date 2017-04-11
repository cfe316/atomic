import numpy as np
import matplotlib.pyplot as plt

import atomic.atomic as atomic
reload(atomic)


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


def time_dependent_power_z(solution, times, f_imp=1., ensemble_average=False, coronal=False):
    element = solution.atomic_data.element
    if ensemble_average:
        solution = solution.ensemble_average()

    for y in solution.select_times(times):
        rad = atomic.Radiation(y, impurity_fraction=f_imp)

    if coronal:
        z_mean = solution.y_coronal.mean_charge()
        power = atomic.Radiation(solution.y_coronal,
                                 impurity_fraction=f_imp).specific_power['total']
    else:
        z_mean = y.mean_charge()
        power = rad.specific_power['total']

    return {'element': element, '<Z>': z_mean, 'power': power}


def time_dependent_z_Plot(solution, times, ensemble_average=False, plotIT=True, write2HDF=False):
    element = solution.atomic_data.element
    if ensemble_average:
        solution = solution.ensemble_average()
        title = element + r' ensemble averaged $\left<Z\right>$'
    else:
        title = element + r' time dependent $\left<Z\right>$'

    if plotIT:
        ax = plt.gca()

    Z_mean_ntau = {}
    for i, y in enumerate(solution.select_times(times)):
        nam = "Z_ne_taures_"+str(times[i] * solution.density)
        print nam
        Z_mean_ntau[nam] = y.mean_charge()
        if plotIT:
            ax.loglog(solution.temperature, y.mean_charge(), color='black', ls='--')

    if plotIT:
        ax.set_xlabel(r'$T_\mathrm{e}\ \mathrm{(eV)}$')
        ax.set_ylim(0.4, y.atomic_data.nuclear_charge + 4)
        annotate_lines(['$10^{%d}$' % i for i in np.log10(times * solution.density)])

    z_mean_coronal = solution.y_coronal.mean_charge()
    if plotIT:
        ax.loglog(solution.temperature, z_mean_coronal, color='black')
        ax.set_title(title)

    if write2HDF:
        import Misc.hickle.hickle as hkl
        print 'START: HDF5 file save'
        outDICT = {'temperature_arr': solution.temperature, 'coronal_Z': z_mean_coronal,
                   'Z_ntau_DIC': Z_mean_ntau}
        fnam = 'Zmeans_'+element+'.h5'
        hkl.dump(outDICT, fnam)


def time_dependent_power_Plot(solution, times, ensemble_average=False, plotIT=True,
                              write2HDF=False):
    element = solution.atomic_data.element
    if ensemble_average:
        solution = solution.ensemble_average()
        title = element + r' ensemble averaged power'
    else:
        title = element + r' time dependent power'

    if plotIT:
        ax = plt.gca()
    Cooling_ntau = {}
    for i, y in enumerate(solution.select_times(times)):
        nam = "Cooling_ne_taures"+str(times[i] * solution.density)
        print nam
        rad = atomic.Radiation(y)
        Cooling_ntau[nam] = rad.specific_power['total']
        if plotIT:
            ax.loglog(solution.temperature, rad.specific_power['total'], color='black', ls='--')

    if plotIT:
        ax.set_xlabel(r'$T_\mathrm{e}\ \mathrm{(eV)}$')
        ax.set_ylabel(r'$P/n_\mathrm{i} n_\mathrm{e}\ [\mathrm{W m^3}]$')
        annotate_lines(['$10^{%d}$' % i for i in np.log10(times * solution.density)])

    power_coronal = atomic.Radiation(solution.y_coronal).specific_power['total']
    if plotIT:
        ax.loglog(solution.temperature, power_coronal, color='black')
        ax.set_title(title)

    if write2HDF:
        import Misc.hickle.hickle as hkl
        print 'START: HDF5 file save'
        outDICT = {'temperature_arr': solution.temperature, 'P_coronal': power_coronal,
                   'Cooling_ntau_DIC': Cooling_ntau}
        fnam = 'CoolingRate_'+element+'.h5'
        hkl.dump(outDICT, fnam)


if __name__ == '__main__':
    times = np.logspace(-7, 0, 100)
    temperature = np.logspace(0, 4, 100)
    density = 1e20

    rt = atomic.RateEquations(atomic.element('carbon'))
    y = rt.solve(times, temperature, density)

    taus = np.array([1e14, 1e15, 1e16, 1e17, 1e18, 1e19])/density

    plt.figure(1)
    plt.clf()
    time_dependent_z_Plot(y, taus)
    plt.draw()

    plt.figure(2)
    plt.clf()
    time_dependent_power_Plot(y, taus)
    plt.draw()

    plt.figure(3)
    plt.clf()
    time_dependent_z_Plot(y, taus, ensemble_average=True)
    plt.draw()

    plt.figure(4)
    plt.clf()
    time_dependent_power_Plot(y, taus, ensemble_average=True)
    plt.draw()

    plt.show()
