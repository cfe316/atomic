class AnnotateRight(object):
    def __init__(self, lines, texts):
        self.lines = lines
        self.texts = texts

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
        xy_last = self._data_to_axis(line)[-1]
        xy_last += np.array([0.01, 0])
        return xy_last

    def _annotate(self):
        for xy, text in zip(self.coordinates, self.texts):
            self.axes.annotate(text, xy, xycoords='axes fraction',
                va='center', ha='left', size='small')


class TemporalEvolutionGraph(object):
    def __init__(self, ax=None):
        import matplotlib.pyplot as plt

        self.ax = ax or plt.gca()
        self.lines = []

    def loglog(self, *args, **kwargs):
        line, = self.ax.loglog(*args, **kwargs)
        self.lines.append(line)

    def annotate_lines(self, texts):
        AnnotateRight(self.lines, texts)

    def set_title(self, text):
        self.ax.text(0.02, 0.98, text, transform=self.ax.transAxes, va='top')

    @property
    def figure(self):
        return self.ax.figure


import numpy as np
import atomic

def time_dependent_z(element_name, times, temperature, density):
    rt = atomic.RateEquations(atomic.element(element_name))

    y = rt.solve(times, temperature, density)

    ne_tau = np.array([ 1e14, 1e15, 1e16, 1e17, 1e18])
    indices = np.searchsorted(y.times, ne_tau/density)

    g = TemporalEvolutionGraph()

    for i in indices:
        z_mean = y[i].mean_charge()
        g.loglog(temperature, z_mean, color='black', ls='--')

    g.ax.set_xlabel(r'$T_\mathrm{e}\ \mathrm{(eV)}$')
    g.ax.set_ylim(0.4, y.atomic_data.nuclear_charge + 4)
    g.annotate_lines(['$10^{%d}$' % i for i in np.log10(ne_tau)])

    z_mean = y.y_coronal.mean_charge()
    g.loglog(temperature, z_mean, color='black')

    def Uppercase(text):
        return text[0].upper() + text[1:]
    g.set_title(Uppercase(y.atomic_data.element) + r' time dependent $\left<Z\right>$')


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    times = np.logspace(-7, 0, 100)
    temperature = np.logspace(0, 3, 100)
    density = 1e19

    time_dependent_z('carbon', times, temperature, density)

    plt.draw()
    plt.show()
