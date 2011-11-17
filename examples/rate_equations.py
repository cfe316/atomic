import numpy as np
import matplotlib.pyplot as plt

import atomic
    
ad = atomic.element('carbon')

temperature = np.logspace(0, 3, 50)
density = 1e19
tau_ss = 1e19 / density

t_normalized = np.logspace(-4, 0, 50)
t_normalized -= t_normalized[0]
times = t_normalized * tau_ss

rt = atomic.RateEquations(ad)
yy = rt.solve(times, temperature, density)

eq = atomic.CoronalEquilibrium(ad)
f_coronal = eq.ionisation_stage_distribution(temperature, density)


plt.figure(2); plt.clf()
yy[-1].plot_vs_temperature()
f_coronal.plot_vs_temperature(ls='--')
plt.draw()


fig = plt.figure(3); plt.clf()
temperature_index = np.searchsorted(rt.temperature, 4)
ax = fig.add_subplot(111)
ax.plot(times/tau_ss, [y.y[:, temperature_index] for y in yy])
plt.draw()


fig = plt.figure(4); fig.clf()
ax = fig.add_subplot(111)

# calculate steady state time
mean_charge = np.array([ f.mean_charge() for f in yy])
z_mean_ref = f_coronal.mean_charge()
tau_ss = np.zeros_like(temperature)
for t, f in reversed(zip(times, yy)):
    z_mean = f.mean_charge()
    mask = np.abs(z_mean/z_mean_ref - 1) <= 0.01
    tau_ss[mask] = t

ax.loglog(temperature, tau_ss * density)
ax.set_xlabel(r'$T_\mathrm{e}\ [\mathrm{eV}]$')
ax.set_ylabel(r'$n_\mathrm{e} \tau_\mathrm{ss}\ [\mathrm{m^{-3} s}]$')
plt.draw()

plt.show()
