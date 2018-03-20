import numpy as np
import matplotlib.pyplot as plt

import atomic_neu.atomic as at
from atomic_neu.atomic.collisional_radiative import CollRadEquilibrium

elements = ['Li', 'C', 'N', 'Ne', 'Si']
elements = ['Si']

temperature_ranges = {
    'Li': np.logspace(-1, 3, 300),
    'C': np.logspace(0, 3, 300),
    'N': np.logspace(0, 3, 300),
    'Ne': np.logspace(0, 4, 300),
    'Si': np.logspace(0, 5, 300),
}

for element in elements:
    ad = at.element(element)
    collrad = CollRadEquilibrium(ad)

    temperature = temperature_ranges.get(element, np.logspace(0, 3, 300))
    y = collrad.ionisation_stage_distribution(temperature, density=1e19)

    plt.figure()
    y.plot_vs_temperature()
    # plt.savefig('collrad_equilibrium_%s.pdf' % element)

plt.show()
