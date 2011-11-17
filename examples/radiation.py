import numpy as np
import atomic


ad = atomic.element('carbon')
eq = atomic.CoronalEquilibrium(ad)

temperature = np.logspace(0, 3, 50)
electron_density = 1e19
y = eq.ionisation_stage_distribution(temperature, electron_density)

rad = atomic.Radiation(y, neutral_fraction=1e-2)

import matplotlib.pyplot as plt
plt.figure(10); plt.clf()

customize = True

if customize:
    for key in rad.power.keys():
        rad.power[key] /= rad.electron_density * rad.get_impurity_density()
    lines = rad.plot()
    plt.ylabel(r'$P/n_\mathrm{i} n_\mathrm{e}\ [\mathrm{W m^3}]$')
    plt.ylim(ymin=1e-35)

    # annotation
    s = '$n_0/n_\mathrm{e}$\n'
    if rad.neutral_fraction == 0:
        s += '$0$'
    else:
        ne = rad.electron_density
        n0 = rad.get_neutral_density()
        exponent = np.log10(n0/ne)
        s += '$10^{%d}$' % exponent

    xy = (rad.temperature[-1], rad.power['total'][-1])
    plt.annotate(s, xy, xytext=(1.05, 0.1),
        horizontalalignment='center',
        textcoords='axes fraction')

else:
    lines = rad.plot()

lines[-1].set_linewidth(2)
plt.legend(loc='best')

plt.draw()
plt.show()

