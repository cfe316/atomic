# This example plots epsilon_cool for several different species,
# for fixed density * tau, but different densities (and taus)
#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

import atomic

elementColors = [
    {'el': 'lithium', 'c': 'green'},
    {'el': 'carbon', 'c': 'black'},
    {'el': 'nitrogen', 'c': 'blue'},
    {'el': 'neon', 'c': 'red'},
    {'el': 'argon', 'c': 'purple'},
]

def num2str(n):
    return str(int(np.log10(n)))

densities = np.array([1e19, 1e20, 1e21])
linewidth = [0.5, 0.9, 1.3]

def plotEps(ad, density, tau, color, lw=1.0):
    """ Solve and rate equations for epsilon and create the lines."""
    rt = atomic.RateEquationsWithDiffusion(ad)
    min_log_temp = ad.coeffs['ionisation'].log_temperature[0]
    temperature = np.logspace(min_log_temp, np.log10(2000), 120)
    times = np.logspace(-7, np.log10(tau)+1, 40)
    times -= times[0]
    yy = rt.solve(times, temperature, density, tau)
    eps = atomic.ElectronCooling(yy.abundances[-1]).epsilon(tau)
    lab = ad.element
    line, = plt.loglog(temperature, eps['total'], color, label=lab, linewidth=lw)

def netauplot(netau):
    """ Create a subplot for given ne * tau."""
    taus = netau / densities

    for i in range(len(densities)):
        density = densities[i]
        tau = taus[i]
        for e in elementColors: 
            plotEps(atomic.element(e['el']), density, tau, e['c'], lw=linewidth[i])

    # make the titles and set boundaries
    netaustring = num2str(netau)
    title1=r'$n_e \tau = 10^{' +netaustring + '} \; [\mathrm{s} \; \mathrm{m}^{-3}]$'
    plt.title(title1)
    plt.ylabel(r'$\epsilon_{cool} \; [\mathrm{eV}]$')
    plt.xlabel(r'$T_e \; [\mathrm{eV}]$')
    plt.ylim(ymin=1e-1, ymax=1e5)
    plt.xlim(xmin=0.4, xmax=2000)

    # create the two legends
    lh = []
    for e in elementColors: 
        lh.append(mlines.Line2D([],[],
                color=e['c'], label=atomic.element(e['el']).element))

    elements_legend = plt.legend(handles=lh, loc=2)
    ax = plt.gca().add_artist(elements_legend)

    lh = []
    for i in range(len(densities)):
        d = num2str(densities[i])
        tau = num2str(taus[i])
        lab = r'$n_e = 10^{' + d + r'},\; \tau = 10^{'+ tau + '}$'
        lh.append(mlines.Line2D([],[],
                               color='k', label=lab, lw=linewidth[i]))

    plt.legend(handles=lh, loc=4)
    plt.grid(True)

plt.close('all')

for i in range(4):
    plt.subplot(2,2,i+1)
    netauplot(np.power(10,14+i))

plt.show()
