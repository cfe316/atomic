import atomic
import numpy as np

import matplotlib.pyplot as plt

from collections import OrderedDict

te = np.logspace(0,3,500)
ne=1e20

elm_colors=[]

elementColors = OrderedDict([
    ('lithium', 'lightgreen'),
    ('Be', 'red'),
    ('B', 'blue'),
    ('C', 'green'),
    ('neon', 'black'),
    ('argon', 'pink'),
])

def plotPostIntegral(ad, color):
    y1 = atomic.post_integral.rhs(ad, te, ne)
    line, = plt.loglog(te, y1, c=color, label=ad.element)

plt.close('all')
    
for el, c in elementColors.items(): 
    plotPostIntegral(atomic.element(el), c)

plt.legend(loc='best')
plt.ylim(ymin=1e-4)
plt.grid(True)
plt.title("Regenerating Post 1995's Figure 10 with Li added")
plt.xlabel(r'$T_e$ [eV]')
plt.ylabel(r'$Q_\parallel$ (GW/m$^2$)/[$n_e (10^{20} \mathrm{m}^{-3})\sqrt{F_z}$]')
plt.show()

# # Comparisons to Post's Table 3 for Be, C, Ne, and Ar
# We compare the output of our integral with Post's table 3. We've added Li.

def table_compare(toptemp):
    print "\n==At " + str(toptemp) + "eV=="
    ne = 1e20
    te = np.logspace(0,np.log10(toptemp),200)
    for el in ('Li', 'Be', 'C', 'Ne', 'Ar'):
        val = atomic.post_integral.rhs(atomic.element(el), te, np.array([ne]))[-1]
        print(el + ' %.3f' % val)

# At 85eV, Post's values (5th row of Table 3) are 0.05, 0.2, and 0.25.
table_compare(85)

# At 120eV, these agree well with Post's values (3rd row of Table 3) of 0.09, 0.30, and 0.5.
table_compare(120)

# At 260eV, Post's values (7th row) are 0.2, 0.7, and 2.
table_compare(260)

# At 185eV, Post's values (9th row) are 0.12, 0.4, and 1.06.
table_compare(185)

