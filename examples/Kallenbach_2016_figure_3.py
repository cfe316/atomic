# In this example I try to reproduce Figure 3 from 
# Kallenbach 2016, "Analytical calculations for impurity
# seeded partially detached divertor conditions"

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from collections import OrderedDict

import atomic

elementColors = OrderedDict([
    ('argon', 'green'),
    ('neon', 'magenta'),
    ('nitrogen', 'black'),
    ('lithium', 'lightgreen'),
])

def Lz_radiated_power(rate_equations, taus, color):
    linestyles = ['dashed', 'solid', 'dashed']
    for i, tau in enumerate(taus):
        print tau * 1e3
        times = np.logspace(-7, np.log10(tau*10), 20)
        y = rt.solve(times, temperature, density, tau)
        rad = atomic.Radiation(y.abundances[-1])
        plt.loglog(temperature, rad.specific_power['total'],
                color=color, ls=linestyles[i])


if __name__ == '__main__':
    temperature = np.logspace(0, np.log10(2e2), 20)
    density = 1e20
    taus = np.array([0.2,0.5,2]) * 1e-3

    plt.figure(1); plt.clf()
    plt.xlim(xmin=1, xmax=2e2)
    plt.ylim(ymin=1e-35, ymax=1e-30)

    legend_handles = []
    for elem, col in elementColors.items():
        rt = atomic.RateEquationsWithDiffusion(atomic.element(elem))
        Lz_radiated_power(rt, taus, col)
        legend_handles.append(mlines.Line2D([],[],
                               color=col, label=rt.atomic_data.element))

    plt.xlabel(r'$T_e \; [\mathrm{eV}]$')
    plt.ylabel(r'$L_z [\mathrm{W m^3}]$')
    plt.legend(handles=legend_handles, loc='best')
    plt.grid(True)
    plt.show()
