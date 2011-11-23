import numpy as np
import matplotlib.pyplot as plt

import atomic
    
ad = atomic.element('carbon')

temperature = np.logspace(0, 3, 50)
density = 1e19
tau = 1e19 / density

t_normalized = np.logspace(-4, 0, 50)
t_normalized -= t_normalized[0]
times = t_normalized * tau

rt = atomic.RateEquations(ad)
yy = rt.solve(times, temperature, density)

# solution after the last timestep
y_final = yy[-1]

# time evolution of ionisation states at a certain temperature
y_fixed_temperature = yy.at_temperature(4)

# steady state time
tau_ss = yy.steady_state_time()

plt.figure(2); plt.clf()
y_final.plot_vs_temperature()
yy.y_coronal.plot_vs_temperature(ls='--')
plt.draw()


fig = plt.figure(3); plt.clf()
ax = fig.add_subplot(111)
ax.semilogx(times/tau, y_fixed_temperature)
plt.draw()


fig = plt.figure(4); fig.clf()
ax = fig.add_subplot(111)

ax.loglog(temperature, tau_ss * density)
ax.set_xlabel(r'$T_\mathrm{e}\ [\mathrm{eV}]$')
ax.set_ylabel(r'$n_\mathrm{e} \tau_\mathrm{ss}\ [\mathrm{m^{-3} s}]$')
plt.draw()

plt.show()
