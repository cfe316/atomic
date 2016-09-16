# This example constructs three plots related to 
#   the time-evolution of a species ionising and radiating in a plasma.
# These plots assume coronal-like conditions, where 
#   time can be exchanged for density, i.e. only the product
#   n_e * tau is important.
# The first plot shows how under conditions of constant temperature and density,
#   a species injected as neutrals will ionise over time, changing its charge
#   state distribution.
# The second plot shows as a function of temperature, the n_e * tau required to 
#   get to a steady-state of charge distribution, and also the dominant charge 
#   state then.
# The third plot is a little tricky. 
#   Given a fixed temperature, if an impurity species is exposed to the plasma
#   for a certain amount of n_e * time, and then the simulation is halted, 
#   what will have been the average charge state distribution for that period?
#   I haven't checked to be certain, but I don't think this model is exactly the 
#   same as a diffusion/impurity confinement time/tau model, since in that model
#   impurities would stay in the plasma for varying amounts of time (with
#   a decreasing exponential abundances) vs in this model all the impurity is 
#   'baked in the plasma oven' for a certain amount of time together.

import numpy as np
import matplotlib.pyplot as plt

import atomic

ad = atomic.element('carbon')

temperature = np.logspace(0, 3, 200)
density = 1e20
tau = 1e19 / density # 1e-1 s

t_normalized = np.logspace(-7, 0, 120)
t_normalized -= t_normalized[0]
times = t_normalized * tau # so from 1e-8 to 1e-1 s

rt = atomic.RateEquations(ad)
yy = rt.solve(times, temperature, density)
# yy is a RateEquationsSolution object.
# len(yy.abundances) = 120
# yy.abundances is a list of FractionalAbundance objects.
# yy.abundances[0].temperature is the same as the temperature above.
# yy.abundances[0].y is a numpy array with shape (7,200)
# yy.abundances[0].y[0] is all 1's and .y[1...6] are all 0.
# so yy is a list of FractionalAbundance objects,
# and each one corresponds to a time point (for ALL the temperatures)?
# so we are running 200 different integrations at once,
# each for a different temperature.

# time evolution of ionisation states at a certain temperature
y_fixed_temperature = yy.at_temperature(38) # has shape (nTimes, nuclear_charge+1) = (120,7)

# steady state time
tau_ss = yy.steady_state_time()

fig = plt.figure(1); plt.clf()
ax = fig.add_subplot(111)
lines_ref = ax.loglog(times/tau, y_fixed_temperature)
ax.set_xlabel(r'$t\ [\mathrm{s}]$')
ax.set_ylim(ymin=1e-3)
ax.set_xlim(xmin=1e-8, xmax=1e-1)
plt.draw()


fig = plt.figure(2); fig.clf()
ax = fig.add_subplot(111)

line, = ax.loglog(temperature, tau_ss * density, visible=False)
yy[-1].replot_colored(line, lines_ref)
ax.set_xlabel(r'$T_\mathrm{e}\ [\mathrm{eV}]$')
ax.set_ylabel(r'$n_\mathrm{e} \tau_\mathrm{ss}\ [\mathrm{m^{-3} s}]$')
plt.draw()


fig = plt.figure(3); fig.clf()

tau = np.array([ 1e18, 1e15, 1e14]) / density
log_netau = np.log10(density * tau)

ybar = yy.ensemble_average()
for iax, y in enumerate(ybar.select_times(tau)):
    ax = fig.add_subplot(3,1, iax + 1)

    lines = ax.loglog(temperature, y.y.T, '-')
    y.annotate_ionisation_stages(lines)
    ax.set_ylim(0.04, 1.4)

    s = r'$n_\mathrm{e} \tau = 10^{%d}\ \mathrm{m^3 s}$' % log_netau[iax]
    ax.text(0.95, 0.95, s, transform=ax.transAxes, va='top',
        ha='right')
    ax.label_outer()


fig.subplots_adjust(hspace=0)
fig.axes[-1].set_xlabel(r'$T_\mathrm{e}\ [\mathrm{eV}]$')
plt.draw()

plt.show()
