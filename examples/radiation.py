# This example plots the radiation rate coefficients for a 
# collisional-radiative model with Carbon at different temperatues,
# an electron density of 1e19 m^(-3), and with infinite particle lifetime
# (\tau = infinity).
# This uses the ADAS scd and acd files to determine the ionisation stage
# abundances, and then uses the plt, prb, and prc files to give the amount
# of line radiation, recombination / brehmstrahlung, and charge-exchange 
# radiation for the computed ionisation stage abundances, temperatures,
# and densities. 
# Note that the neutral_fraction which specifies the amount of neutral H
# present effects the radiation (via cx_power), but charge exchange
# processes on the ionisation stage balance are not modeled.

import numpy as np
import atomic


ad = atomic.element('carbon')
eq = atomic.CoronalEquilibrium(ad)

temperature = np.logspace(0, 3, 50)
electron_density = 1e19
# y is a FractionalAbundance object.
y = eq.ionisation_stage_distribution(temperature, electron_density)

rad = atomic.Radiation(y, neutral_fraction=1e-2)

import matplotlib.pyplot as plt
plt.figure(10); plt.clf()

lines = rad.plot()

customize = True

if customize:
    plt.ylabel(r'$P/n_\mathrm{i} n_\mathrm{e}\ [\mathrm{W m^3}]$')
    plt.ylim(ymin=1e-35)
    
    # annotation
    s = '$n_0/n_\mathrm{e}$\n'
    if rad.neutral_fraction == 0:
        s += '$0$'
    else:
        # writes only 10^-1 or 10^-2, not 5.12 x 10^-1
        ne = rad.electron_density
        n0 = rad.get_neutral_density()
        exponent = np.log10(n0/ne)
        s += '$10^{%d}$' % exponent
    
    xy = (rad.temperature[-1], rad.specific_power['total'][-1])
    plt.annotate(s, xy, xytext=(1.05, 0.1),
        horizontalalignment='center',
        textcoords='axes fraction')

lines[-1].set_linewidth(2)
plt.legend(loc='best')

plt.draw()
plt.show()

