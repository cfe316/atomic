# This example demonstrates the RateEquationsWithDiffusion class.
# This solves the rate equations for the ionisation stages of
# a given species evolving at different constant temperatures and
# fixed density. There is diffusion of all ionisation stages out of the system,
# and replacement by neutrals, such that the total number of
# ions stays fixed over time at 1.0.
#
# plots are shown of the time history of the stages at roughly 10eV,
# and also of the final state (after 1 second) of the ions for the various temperatures.
#
import numpy as np
import matplotlib.pyplot as plt

import atomic

ad = atomic.element('carbon')

temperature = np.logspace(0, 3, 100)
density = 1e19
tau = 1e-3

times = np.logspace(-7, 0, 120)
times -= times[0]

rt = atomic.time_dependent_rates.RateEquationsWithDiffusion(ad)
yy = rt.solve(times, temperature, density, tau)

# time evolution of ionisation states at 10eV
y_fixed_temperature = yy.at_temperature(10)  # has shape (nTimes, nuclear_charge+1) = (120,7)

fig = plt.figure(1)
plt.clf()
ax = fig.add_subplot(111)
lines_ref = ax.semilogx(times, y_fixed_temperature)
ax.set_xlabel(r'$t\ [\mathrm{s}]$')
ax.set_ylim(ymin=0)
ax.set_xlim(xmin=0)
plt.draw()

# fractional abundances at various temperatures at the last timestep.
plt.figure()
frab = yy.abundances[-1]
frab.plot_vs_temperature()

plt.show()
