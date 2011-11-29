"""
typical carbon content is n_c / n_e = 0.05
"""
import numpy as np
import matplotlib.pyplot as plt

import atomic
from time_dependent_z import annotate_lines

def parabolic_profile(y0):
    x = np.linspace(1., 0, 50)
    y = 1 - x**4
    y *= y0
    return x, y

r, temperature = parabolic_profile(2e3)
r, density = parabolic_profile(1e19)

ad = atomic.element('carbon')
eq = atomic.CoronalEquilibrium(ad)
y = eq.ionisation_stage_distribution(temperature, density)

ne_tau = np.array([1e-1, 1e-2, 1e-3])
impurity_fraction = 0.05


texts = ['$10^{%d}$' % i for i in np.log10(ne_tau)]

try:
    tau_ss
except NameError:
    t_normalized = np.logspace(-4, 0, 500)
    t_normalized -= t_normalized[0]
    times = t_normalized

    rt = atomic.RateEquations(ad)
    yy = rt.solve(times, temperature, density)
    tau_ss = yy.steady_state_time()

y_bar = yy.ensemble_average()

# prepare plots
f = plt.figure(1); f.clf()
ax1 = f.add_subplot(411)
ax2 = f.add_subplot(412, sharex=ax1)
#ax3 = f.add_subplot(513, sharex=ax1)
ax4 = f.add_subplot(413, sharex=ax1)
ax5 = f.add_subplot(414, sharex=ax1)

# density and temperature profiles
ax = ax1
ax.plot(r,density/1e19, r, temperature/1e3)
ax.set_xlabel(r'$\rho$')


# steady state time
ax = ax2
line, = ax.semilogy(r, tau_ss)
ax.set_ylabel(r'$\tau_\mathrm{ss}\ [s]$')
ax.set_ylim(ymax=2)


# fractional abundance
#ax = ax3
#lines_abundance = ax.semilogy(r, y.y.T*100)
#ax.set_ylim(0.3, 400)
#yy.y_coronal.replot_colored(line, lines_abundance)


# fractional abundance, Zeff, Zmean
y_selected = y_bar.select_times(ne_tau)
for y in y_selected:
    #ax3.semilogy(r, y.y[-1,:].T*100, color='black')
    lines = ax4.plot(r, y.effective_charge(impurity_fraction),
            color='black', ls='--')

    rad = atomic.Radiation(y, impurity_fraction=impurity_fraction)
    total_power = rad.power['total']

    #mask = temperature < 1e3
    #total_power -= total_power[mask].mean()
    #total_power = total_power.clip(0)
    #radiation_parameter = total_power / (density * impurity_fraction * density)
    ax5.plot(r, total_power)


#from matplotlib.ticker import FormatStrFormatter
#ax = ax3
#major_formatter = FormatStrFormatter('$%d\%%$')
#ax.yaxis.set_major_formatter(major_formatter)
#y.annotate_ionisation_stages(lines_abundance)


from matplotlib.ticker import MaxNLocator
ax = ax4
locator = MaxNLocator(4)
ax.set_ylabel(r'$Z_\mathrm{eff}$')
ax.yaxis.set_major_locator(locator)

lo, hi = ax.get_ylim()
ax.set_ylim(lo, 1.1 * hi)

annotate_lines(texts, ha='left', va='bottom', ax=ax)


# radiation profile
ax = ax5
ax.set_yticks(ax.get_yticks()[:-1:2])
annotate_lines(texts, ha='left', va='bottom', ax=ax)

locator = MaxNLocator(4)
ax.yaxis.set_major_locator(locator)


# position subplots
for ax in f.axes:
    if not ax.is_last_row(): ax.get_xaxis().label.set_visible(False)
    ax.label_outer()
f.subplots_adjust(hspace=0)
plt.draw()

plt.show()
