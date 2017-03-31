import atomic
import numpy as np
import matplotlib.pyplot as plt


ad = atomic.element('carbon')
temperature = np.logspace(0, 4, 100)
density = 1e19

S = ad.coeffs['ionisation']
alpha = ad.coeffs['recombination']


def annotate(element, lines, ind=-1):
    for i, l in enumerate(lines):
        ax = l.axes
        xy = l.get_xydata()[ind]
        s = '$\mathrm{%s}^{%d+}$' % (element, i)
        ax.annotate(s, xy, color=l.get_color(), va='center')


plt.figure(1); plt.clf()
for i in xrange(ad.nuclear_charge):
    plt.loglog(temperature, S(i, temperature, density))
plt.xlabel(r'$T_\mathrm{e}\ [\mathrm{eV}]$')
plt.ylabel(r'$S\ [\mathrm{m^3 s^{-1}}]$')
plt.ylim(ymin=1e-20)

lines = plt.gca().lines
annotate(ad.element, lines)
plt.draw()


plt.figure(2); plt.clf()
for i in xrange(ad.nuclear_charge):
    plt.loglog(temperature, alpha(i, temperature, density))
plt.xlabel(r'$T_\mathrm{e}\ [\mathrm{eV}]$')
plt.ylabel(r'$\alpha\,[\mathrm{m^3 s^{-1}}]$')
plt.ylim(ymin=1e-20)

lines = plt.gca().lines
annotate(ad.element, lines, 0)
plt.draw()

plt.show()

