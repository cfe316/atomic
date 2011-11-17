import numpy as np
import matplotlib.pyplot as plt

import atomic

elements = ['C', 'Ne', 'Ar']

temperature_ranges = {
    'C'  : np.logspace(0,3, 300),
    'Ne' : np.logspace(0,4, 300),
    'Ar' : np.logspace(0,5, 300),
}

for element in elements:
    ad = atomic.element(element)
    coronal = atomic.CoronalEquilibrium(ad)

    temperature = temperature_ranges.get(element, np.logspace(0, 3, 300))
    y = coronal.ionisation_stage_distribution(temperature, density=1e19)

    plt.figure();
    y.plot_vs_temperature()
    #plt.savefig('coronal_equilibrium_%s.pdf' % element)

plt.show()
