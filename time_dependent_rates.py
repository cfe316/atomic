import numpy as np
from scipy.integrate import odeint


class RateEquations(object):
    def __init__(self, atomic_data):
        self.S = atomic_data.ionisation_coeff
        self.alpha = atomic_data.recombination_coeff
        self.element = atomic_data.element
        self.nuclear_charge = atomic_data.nuclear_charge

        self.temperature = np.logspace(0, 3, 300)
        self.temperature = 5e1
        self.density = 1e19

        self._init_y()
        self._init_coeffs()

    def _init_y(self):
        #y = np.zeros((self.nuclear_charge + 1, len(self.temperature)))
        #y[0] = np.ones_like(self.temperature)
        y = np.zeros(self.nuclear_charge + 1)
        y[0] = 1
        self.y = y

    def _init_coeffs(self):
        S_ = np.zeros(self.nuclear_charge + 1)
        alpha_ = np.zeros(self.nuclear_charge + 1)
        for k in xrange(self.nuclear_charge):
            S_[k] = self.S(k, self.temperature, self.density)
            alpha_[k] = self.alpha(k, self.temperature, self.density)

        self.S_ = S_
        self.alpha_ = alpha_

    def derivs(self, y, t0):
        """right hand side of the rate equations"""

        dydt = np.zeros_like(y)
        S = self.S_
        alpha = self.alpha_
        ne = self.density

        for k in xrange(self.nuclear_charge + 1):
            if k == 0:
                gain = y[k-1]*S[k-1] + y[k+1]*alpha[k]
                loss = y[k] * S[k]
            elif k == self.nuclear_charge:
                gain = y[k-1]*S[k-1]
                loss = y[k] * (S[k] + alpha[k-1])
            else:
                # eq 2 with alpha[k+1] => alpha[k] substitiution
                gain = y[k-1]*S[k-1] + y[k+1]*alpha[k]
                loss = y[k] * (S[k] + alpha[k-1])

            dydt[k] = (gain - loss)

        return dydt

    def solve(self, time):
        return odeint(self.derivs, self.y, time)


if __name__ == '__main__':
    from atomic_data import AtomicData
    ad = AtomicData.from_element('carbon')
    rt = RateEquations(ad)

    tau_ss = 1e18 / rt.density * 4e6
    t = np.linspace(0, 3, 150) * tau_ss
    yy = rt.solve(t)


    import matplotlib.pyplot as plt

    plt.figure(1); plt.clf()
    plt.plot(t/tau_ss, yy)
    plt.xlabel(r'$t/\tau_\mathrm{ss}$')
    plt.ylim(ymin=0)
    plt.draw()
    plt.show()
