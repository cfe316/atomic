from scipy.interpolate import RectBivariateSpline
import xxdata_11

recombination = xxdata_11.read_acd('acd96_c.dat')
ionisation = xxdata_11.read_scd('scd96_c.dat')

#recombination = xxdata_11.read_acd('acd89_ar.dat')
#ionisation = xxdata_11.read_scd('scd89_ar.dat')

nuclear_charge = recombination['charge']

logalpha, logS = [], []
for i in xrange(nuclear_charge):
    d = recombination
    sp = RectBivariateSpline(d['temperature'], d['density'], d['coeff_table'][i])
    logalpha.append(sp)

    d = ionisation
    sp = RectBivariateSpline(d['temperature'], d['density'], d['coeff_table'][i])
    logS.append(sp)


import matplotlib.pyplot as plt
import numpy as np

logdens = 13 # log10(n_e[cm-3])

temperature = np.logspace(0, 3, 300)
logtemp = np.log10(temperature)

y = np.zeros((nuclear_charge+1, len(temperature)))
y[0] = np.ones_like(temperature)
for i in xrange(nuclear_charge):
    alpha = logalpha[i](logtemp, logdens)
    alpha = np.power(10, alpha).squeeze()

    S = logS[i](logtemp, logdens)
    S = np.power(10, S).squeeze()
    y[i+1] = y[i] * S / alpha

y /= y.sum(0) # fractional abundance

plt.figure(1); plt.clf()
ax = plt.gca()

ax.loglog(temperature, y.T)

ax.set_xlabel('$T_\mathrm{e}\ [\mathrm{eV}]$')
ax.set_ylim(0.05, 1)


plt.draw()
plt.show()
