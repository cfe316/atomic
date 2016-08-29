import numpy as np
import matplotlib.pyplot as plt

import atomic

ad = atomic.element('carbon')

temperature = np.logspace(0, 3, 50)
density = 1e19
tau = 1e19 / density

t_normalized = np.logspace(-7, 0, 120)
t_normalized -= t_normalized[0]
times = t_normalized * tau

rt = atomic.RateEquations(ad)
yy = rt.solve(times, temperature, density)
# yy is a RateEquationsSolution object.
# len(yy.abundances) = 60
# yy.abundances is a list of FractionalAbundance objects.
# yy.abundances[0].temperature is the same as the temperature above.
# yy.abundances[0].y is a numpy array with shape (7,50)
# yy.abundances[0].y[0] is all 1's and .y[1...6] are all 0.
# so yy is a list of FractionalAbundance objects,
# and each one corresponds to a time point (for ALL the temperatures)?
# so like, we're essentially running 50 different integrations at once,
# each for a different temperature?

# time evolution of ionisation states at a certain temperature
y_fixed_temperature = yy.at_temperature(10) # has shape (nTimes, nuclear_charge+1) = (120,7)

# steady state time
tau_ss = yy.steady_state_time()

fig = plt.figure(1); plt.clf()
ax = fig.add_subplot(111)
lines_ref = ax.semilogx(times/tau, y_fixed_temperature)
ax.set_xlabel(r'$t\ [\mathrm{s}]$')
ax.set_ylim(ymin=0)
ax.set_xlim(xmin=0)
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
