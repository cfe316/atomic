# This example plots epsilon_cool for several different species,
# for a fixed density and tau.
#
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

import atomic

elementColors = OrderedDict([
    ('carbon', 'black'),
    ('nitrogen', 'blue'),
    ('neon', 'red'),
    ('lithium', 'green'),
])

def plotEps(ad, color):
    rt = atomic.RateEquationsWithDiffusion(ad)
    min_log_temp = ad.coeffs['ionisation'].log_temperature[0]
    temperature = np.logspace(min_log_temp, np.log10(2000), 40)
    yy = rt.solve(times, temperature, density, tau)
    elc = atomic.ElectronCooling(yy.abundances[-1])
    eps = elc.epsilon(tau)
    y1 = eps['total']
    lab = ad.element
    line, = plt.loglog(temperature, y1, color, label=lab)

tau = 1e-5
density = 1e20
times = np.logspace(-7, np.log10(tau) + 1, 120)

for el, c in elementColors.items(): 
    print el
    plotEps(atomic.element(el), c)

plt.title(r'$n_e = \; '+ str(density)+ r'\; [m^{-3}]$, $ \tau = 1e'+str(int(np.log10(tau)))+'\;[s]$, dashed=rad only, solid=with ionization')
plt.ylabel(r'$\epsilon_{cool} \; [\mathrm{eV}]$')
plt.xlabel(r'$T_e \; [\mathrm{eV}]$')
plt.ylim(ymin=1e-0, ymax=1e5)
plt.xlim(xmin=0.4, xmax=2000)
plt.legend(loc='best')
plt.grid(True)
plt.show()

