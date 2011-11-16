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


