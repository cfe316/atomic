from scipy.interpolate import RectBivariateSpline
import xxdata_11

recombination = xxdata_11.read_acd('acd96_c.dat')
ionisation = xxdata_11.read_scd('scd96_c.dat')


logalpha, logS = [], []
for i in xrange(6):
    d = recombination
    sp = RectBivariateSpline(d['temperature'], d['density'], d['coeff_table'][i])
    logalpha.append(sp)

    d = ionisation
    sp = RectBivariateSpline(d['temperature'], d['density'], d['coeff_table'][i])
    logS.append(sp)


import matplotlib.pyplot as plt
import numpy as np

logdens = 13 # log10(n_e[cm-3])

temperature = np.logspace(0,3,300)
logtemp = np.log10(temperature)

y = np.zeros((7, len(temperature)))
y[0] = np.ones_like(temperature)
for i in xrange(1,7):
    alpha = logalpha[i-1](logtemp, logdens)
    alpha = np.power(10, alpha).squeeze()

    S = logS[i-1](logtemp, logdens)
    S = np.power(10, S).squeeze()
    y[i] = y[i-1] * S / alpha 


plt.figure(1); plt.clf()
ax = plt.gca()

#ax.plot(temperature, y0)
y_all = y.sum(0)
ax.loglog(temperature, y.T/y_all[:,np.newaxis] )

ax.set_xlabel('$T_\mathrm{e}\ [\mathrm{eV}]$')
ax.set_ylim(0.05, 1)

plt.draw()
plt.show()
