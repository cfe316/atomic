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

plt.figure(1); plt.clf()
axL = plt.gca()
axR = axL.twinx()

axL.plot(r,density/1e19, r, temperature/1e3, lw=2, color='black')
lines = axR.semilogy(r, y.y.T*100)

axR.set_ylim(0.3, 130)

major_formatter = FormatStrFormatter('$%d\%%$')
axR.yaxis.set_major_formatter(major_formatter)
y.annotate_ionisation_stages(lines)

plt.draw()
plt.show()
