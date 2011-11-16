import numpy as np

import atomic

ad = atomic.AtomicData.from_element('carbon')
eq = atomic.CoronalEquilibrium(ad)


temperature = np.logspace(0, 3, 50)
density = 1e19

y = eq.ionisation_stage_distribution(temperature, density)
line_rad = ad.radiation['line']
cont_rad = ad.radiation['continuum']
cx_rad = ad.radiation['cx']

A = np.zeros((ad.nuclear_charge+1, temperature.shape[0]))
B = np.zeros_like(A)
C = np.zeros_like(A)

epsilon = 1e-4
ne = density
ni = epsilon * ne
for k in xrange(ad.nuclear_charge):
    A[k] = ne * ni * y.y[k] * line_rad(k, temperature, density)
    B[k] = ne * ni * y.y[k] * cont_rad(k, temperature, density)
    #C[k] = ne * ni * y.y[k] * cx_rad(k, temperature, density)

#A /= ne*ni
#B /= ne*ni
#C /= ne*ni

import matplotlib.pyplot as plt

plt.figure(10); plt.clf()
plt.loglog(temperature, A.sum(0), label='cont')
plt.loglog(temperature, B.sum(0), label='line')
plt.loglog(temperature, C.sum(0), label='cx')
plt.loglog(temperature, (A + B + C).sum(0), 'k-', lw=2, label='total')
plt.xlabel(r'$T_\mathrm{e}\ [\mathrm{eV}]$')
plt.ylabel(r'$P/n_\mathrm{i} n_\mathrm{e}\ [\mathrm{W m^3}]$')
plt.legend(loc='best')
#plt.ylim(ymin=1e-35)

plt.draw()
plt.show()


