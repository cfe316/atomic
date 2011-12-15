import numpy as np
import matplotlib.pyplot as plt
import atomic

from ensemble_average import time_dependent_power


if __name__ == '__main__':
    times = np.logspace(-7, 0, 50)
    temperature = np.logspace(0, 3, 50)
    density = 1e19

    from atomic.pec import TransitionPool
    ad = atomic.element('argon')
    tp = TransitionPool.from_adf15('adas_data/pec/*ar*.dat')
    ad = tp.filter_energy(2e3, 20e3, 'eV').create_atomic_data(ad)

    rt = atomic.RateEquations(ad)
    y = rt.solve(times, temperature, density)

    taus = np.array([ 1e14, 1e15, 1e16, 1e17, 1e18])/density

    plt.figure(1); plt.clf()
    from filter_construction import plot_coeffs
    plot_coeffs(ad, temperature, 5)
    plt.ylim(1e-35, 1e-30)
    plt.draw()

    plt.figure(2); plt.clf()
    time_dependent_power(y, taus)
    plt.draw()

    plt.figure(3); plt.clf()
    time_dependent_power(y, taus, ensemble_average=True)
    plt.draw()


    plt.show()
