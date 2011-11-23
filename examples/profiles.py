"""
typical carbon content is n_c / n_e = 0.05
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import atomic

def parabolic_profile(y0):
    x = np.linspace(1., 0, 500)
    y = 1 - x**2
    y *= y0
    return x, y

r, temperature = parabolic_profile(2e3)
r, density = parabolic_profile(1e19)

ad = atomic.element('neon')
eq = atomic.CoronalEquilibrium(ad)
y = eq.ionisation_stage_distribution(temperature, density)

try:
    tau_ss
except NameError:
    t_normalized = np.logspace(-4, 0, 500)
    t_normalized -= t_normalized[0]
    times = t_normalized

    rt = atomic.RateEquations(ad)
    yy = rt.solve(times, temperature, density)
    tau_ss = yy.steady_state_time()


# prepare plots
f = plt.figure(1); f.clf()
ax_profiles = f.add_subplot(311)
ax_abundance = f.add_subplot(312, sharex=ax_profiles)
ax_tau_ss = f.add_subplot(313, sharex=ax_profiles)

# density and temperature profiles
ax_profiles.plot(r,density/1e19, r, temperature/1e3)
ax_profiles.set_xlabel(r'$\rho$')


# fractional abundance
lines_abundance = ax_abundance.semilogy(r, y.y.T*100)
ax_abundance.set_ylim(0.3, 200)

major_formatter = FormatStrFormatter('$%d\%%$')
ax_abundance.yaxis.set_major_formatter(major_formatter)
y.annotate_ionisation_stages(lines_abundance)

# steady state time
line, = ax_tau_ss.semilogy(r, tau_ss, visible=False)
ax_tau_ss.set_ylabel(r'$\tau_\mathrm{ss}\ [s]$')
ax_tau_ss.set_ylim(ymax=2)

yy.y_coronal.replot_colored(line, lines_abundance)

for ax in f.axes:
    if not ax.is_last_row(): ax.get_xaxis().label.set_visible(False)
    ax.label_outer()
f.subplots_adjust(hspace=0)
plt.draw()
plt.show()
