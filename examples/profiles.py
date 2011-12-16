"""
typical carbon content is n_c / n_e = 0.05
"""
import numpy as np
import matplotlib.pyplot as plt

import atomic
from ensemble_average import annotate_lines

def parabolic_profile(y0):
    x = np.linspace(1., 0, 50)
    y = 1 - x**2
    y *= y0
    return x, y

r, temperature = parabolic_profile(3e3)
r, density = parabolic_profile(1e19)

try:
    ad
except NameError:
    from atomic.pec import TransitionPool
    ad = atomic.element('argon')
    tp = TransitionPool.from_adf15('adas_data/pec/transport_llu#ar*.dat')
    ad = tp.filter_energy(2e3, 20e3, 'eV').create_atomic_data(ad)

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
ax1 = f.add_subplot(511)
ax2 = f.add_subplot(512, sharex=ax1)
#ax3 = f.add_subplot(513, sharex=ax1)
ax4 = f.add_subplot(513, sharex=ax1)
ax5 = f.add_subplot(514, sharex=ax1)
ax6 = f.add_subplot(515, sharex=ax1)

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


def normalized_gradient(x, y):
    return -np.gradient(y)/np.gradient(x)/y

# fractional abundance, Zeff, Zmean
y_selected = y_bar.select_times(ne_tau)
for y in y_selected:
    #ax3.semilogy(r, y.y[-1,:].T*100, color='black')
    #lines = ax4.plot(r, y.effective_charge(impurity_fraction),
    #        color='black', ls='--')

    rad = atomic.Radiation(y, impurity_fraction=impurity_fraction)
    total_power = rad.power['total']

    ax4.plot(r, total_power)

    radiation_parameter = total_power / (impurity_fraction * density)
    line, = ax5.plot(r, radiation_parameter)

    rlte = normalized_gradient(r, temperature)
    rlrad = normalized_gradient(r, total_power)
    ax6.plot(r, rlrad)

ax6.plot(r, rlte, 'k--')
ax6.set_ylim(0,10)
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
#f.subplots_adjust(hspace=0)
plt.draw()

plt.show()
