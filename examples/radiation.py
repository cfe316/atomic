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
B2 = np.zeros_like(A)

neutral_fraction = 0.01 # epsilon
impurity_fraction = 0.01
ne = density
ni = impurity_fraction * ne
n0 = neutral_fraction * ne

for k in xrange(ad.nuclear_charge):
    A[k] = ne * ni * y.y[k] * line_rad(k, temperature, ne)
    B[k] = ne * ni * y.y[k] * cont_rad(k, temperature, ne)
    C[k] = n0 * ni * y.y[k] * cx_rad(k, temperature, ne)

    B2[k] = 1.53e-38

A /= ne*ni
B /= ne*ni
C /= ne*ni

A = A.sum(0)
B = B.sum(0)
C = C.sum(0)

D = A + B + C

import matplotlib.pyplot as plt

plt.figure(10); plt.clf()
plt.loglog(temperature, A, label='cont', color='blue')
plt.loglog(temperature, B, label='line', color='green')
plt.loglog(temperature, C, label='cx', color='red')
plt.loglog(temperature, D, 'k-', lw=2, label='total')

# annotation
s = '$\\varepsilon n_0/n_\mathrm{e}$\n'
if neutral_fraction == 0:
    s += '$0$'
else:
    s += '$10^{%d}$' % np.log10(neutral_fraction*n0/ne)
xy = (temperature[-1], D[-1])
plt.annotate(s, xy, xytext=(1.05, 0.1),
        horizontalalignment='center',
        textcoords='axes fraction')

# fancy filling
alpha = 0.5
O = np.ones_like(temperature) * B.min()
plt.fill_between(temperature, A, O, color='blue', alpha=alpha)
plt.fill_between(temperature, B, O, color='green', alpha=alpha)
plt.fill_between(temperature, C, O, color='red', alpha=alpha)
plt.xlabel(r'$T_\mathrm{e}\ [\mathrm{eV}]$')
plt.ylabel(r'$P/n_\mathrm{i} n_\mathrm{e}\ [\mathrm{W m^3}]$')
plt.legend(loc='best')
plt.ylim(ymin=1e-35)

plt.draw()
plt.show()


