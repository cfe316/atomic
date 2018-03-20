import numpy as np
import matplotlib.pyplot as plt

import atomic_neu.atomic as at
import atomic_neu.atomic.coronal as cor

elements = ['C', 'Li', 'Si']
elements = ['Si']

temperature_ranges = {
                     'C': np.logspace(0, 3, 300),
                     'Li': np.logspace(0, 4, 300),
                     'Si': np.logspace(0, 5, 300),
                     }

for element in elements:
    ad = at.element(element)
    coronal = cor.CoronalEquilibrium(ad)

    temperature = temperature_ranges.get(element)
    y = coronal.ionisation_stage_distribution(temperature, density=1e19)

    plt.figure()
    y.plot_vs_temperature()
    # plt.savefig('coronal_equilibrium_%s.pdf' % element)

plt.show()
