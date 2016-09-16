# This example makes plots related to 
# Figure 10 in D. Post's 1995 paper.

# For an upstream temperature of 250eV,
# (and a target temperature of 1/2 the first ionisation energy of a species)
# what parallel power could be radiated for a certain impurity fraction,
# as a function of (a constant along the SOL) n_e * tau?

# This script can take a bit of time to run since the axis being plotted 
# over (density, basically) is not vectorized like temperature is.
# Also the running time could be improved by doing a steady-state diffusion
# calculation instead of time-dependent ones.

# Note that compared to Kallenbach (2013)'s paper, the Post calculation ignores
# the lowered conductivity due to higher Z_eff, which ends up lowering the total 
# radiated power.

import atomic
import numpy as np

from matplotlib import pyplot as plt

from collections import OrderedDict
import itertools

ne = np.array([1e20])
taus = np.logspace(-6,-1,20)
netaus = ne * taus

elementColors = OrderedDict([
    ('argon', 'pink'),
    ('neon', 'black'),
    ('N', 'blue'),
    ('C', 'green'),
#    ('B', 'blue'),
    ('Be', 'red'),
    ('lithium', 'lightgreen'),
])

def exp2str(n):
    return str(int(np.log10(n)))

def num2latex(n):
    if n == np.inf:
        return r'\infty'
    else:
        return r'10^{' + exp2str(n) + '}'

def num2sslatex(n):
    return r'$\mathregular{' + num2latex(n) + '}$'

def plotPostIntegral(ad, color):
    te = atomic.post_integral.temperatureRange(ad, top=250)
    y = []
    for netau in netaus:
        y.append(atomic.post_integral.rhs(ad, te, ne, tau=netau/ne)[-1])
    line, = ax1.loglog(taus, y, c=color, label=ad.element)

plt.close('all')
    
d = num2latex(ne)
lab = r'$n_e = ' + d +'\,\mathrm{m}^{-3}, \; T_{e,sep} = 250 \mathrm{eV}$'

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

for el, c in elementColors.items(): 
    plotPostIntegral(atomic.element(el), c)

font = {'size'   : 16}
plt.rc('font', **font)
ax1.legend(loc='best')
ax1.set_ylim(ymin=1e-2, ymax=1e1)
ax1.grid(True)
ax1.text(4e-5,0.03, lab, fontdict={'size':20})
fig.subplots_adjust(bottom=0.12)
ax1.set_xlabel(r'$\tau \; [s]$')
ax1.set_ylabel(r'$q_\parallel$ (GW/m$^2$)/[$n_e (10^{20} \mathrm{m}^{-3})\sqrt{F_z}$]')

# second x axis 
ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())
ax2.set_xscale('log')
ax2.set_xlabel(r'$n_e \tau \; [m^{-3} \;s]$')
new_tick_locations = np.logspace(-5,-1,5) # hack
new_tick_labels = [num2sslatex(i) for i in new_tick_locations * ne]
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(new_tick_labels)

# remove doubled frame due to the second axes
for loc in ['top', 'right', 'bottom', 'left']:
    ax2.spines[loc].set_visible(False)

plt.show()
