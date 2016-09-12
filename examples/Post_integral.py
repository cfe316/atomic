# This tries to copy D. Post's Figure 10, but adding Lithium.
# see
# "Calculations of Energy Losses due to Atomic Processes in
#  Tokamaks with Applications to the ITER Divertor", 1995

import atomic
import numpy as np

from matplotlib import pyplot as plt

from collections import OrderedDict

ne=1e20

elementColors = OrderedDict([
    ('lithium', 'lightgreen'),
    ('Be', 'red'),
    ('B', 'blue'),
    ('C', 'green'),
    ('N', 'blue'),
    ('neon', 'black'),
    ('argon', 'pink'),
])

def plotPostIntegral(ad, color):
    te = atomic.post_integral.temperatureRange(ad)
    y1 = atomic.post_integral.rhs(ad, te, ne)
    line, = plt.loglog(te, y1, c=color, label=ad.element)

plt.close('all')
    
for el, c in elementColors.items(): 
    plotPostIntegral(atomic.element(el), c)

font = {'size'   : 16}

plt.rc('font', **font)
plt.legend(loc=2)
plt.xlim(xmin=1,xmax=1000)
plt.ylim(ymin=3e-3)
plt.grid(True)
plt.title("After D. Post, 1995, Figure 10")
fd = {'size':20}
plt.figtext(0.4,0.6,r'$n_e = 10^{20} \mathrm{m}^{-3}, \tau=\infty$', fontdict=fd)
plt.subplots_adjust(bottom=0.12)
plt.xlabel(r'$T_{e,sep}$ [eV]')
plt.ylabel(r'$q_\parallel$ (GW/m$^2$)/[$n_e (10^{20} \mathrm{m}^{-3})\sqrt{F_z}$]')
plt.show()

# # Comparisons to Post's Table 3 for Be, C, Ne, and Ar
# We compare the output of our integral with Post's table 3. We've added Li.

#def table_compare(toptemp):
#    print "\n==At " + str(toptemp) + "eV=="
#    ne = 1e20
#    for el in ('Li', 'Be', 'C', 'Ne', 'Ar'):
#        te = atomic.post_integral.temperatureRange(atomic.element(el), top=toptemp)
#        val = atomic.post_integral.rhs(atomic.element(el), te, np.array([ne]))[-1]
#        print(el + ' %.3f' % val)
#
## At 85eV, Post's values (5th row of Table 3) are 0.05, 0.2, and 0.25.
#table_compare(85)
#
## At 120eV, these agree well with Post's values (3rd row of Table 3) of 0.09, 0.30, and 0.5.
#table_compare(120)
#
## At 260eV, Post's values (7th row) are 0.2, 0.7, and 2.
#table_compare(260)
#
## At 185eV, Post's values (9th row) are 0.12, 0.4, and 1.06.
#table_compare(185)
#
