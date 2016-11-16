# This example makes plots similar to 
# Figure 10 in D. Post's 1995 paper, but with 
# an impurity diffusion term with time constant tau.

# This program will output many plots, one for each combination
# of density and tau. It's probably not strictly necessary, since 
# the plots mostly depend on only the product n_e * tau.

import atomic
import numpy as np

from matplotlib import pyplot as plt

from collections import OrderedDict
import itertools

densities = np.logspace(19,21,3)
taus = np.append(np.logspace(-6,-1,6), np.inf)

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

def num2estr(n):
    if n == np.inf:
        return str(n)
    else:
        return '1e' + exp2str(n)

def plotPostIntegral(ad, color):
    te = atomic.post_integral.temperatureRange(ad, top=500)
    y1 = atomic.post_integral.rhs(ad, te, ne, tau=tau)
    line, = plt.loglog(te, y1, c=color, label=ad.element)

for ne, tau in itertools.product(densities, taus):
    plt.close('all')
        
    for el, c in elementColors.items(): 
        plotPostIntegral(atomic.element(el), c)

    d, ta = map(num2latex, [ne, tau])
    lab = r'$n_e = ' + d + r'\,\mathrm{m}^{-3},\; \tau = ' + ta + '\,\mathrm{s}$'

    font = {'size'   : 16}
    plt.rc('font', **font)
    plt.legend(loc=2)
    plt.xlim(xmin=10,xmax=500)
    plt.ylim(ymin=1e-4, ymax=1e2)
    plt.grid(True)
    plt.figtext(0.5,0.2, lab, fontdict={'size':20})
    plt.subplots_adjust(bottom=0.12)
    plt.xlabel(r'$T_{e,sep}$ [eV]')
    plt.ylabel(r'$q_\parallel$ (GW/m$^2$)/[$n_e (10^{20} \mathrm{m}^{-3})\sqrt{F_z}$]')

    d, ta = map(num2estr, [ne, tau])
    plt.savefig('PostPlot_' + d + '_' + ta + '.png')