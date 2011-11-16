import numpy as np
from scipy.integrate import odeint


class RateEquations(object):
    def __init__(self, atomic_data):
        self.S = atomic_data.ionisation_coeff
        self.alpha = atomic_data.recombination_coeff
        self.element = atomic_data.element
        self.nuclear_charge = atomic_data.nuclear_charge

        self.temperature = np.logspace(0, 3, 300)
        self.density = 1e19

        self.y_shape = (self.nuclear_charge + 1, len(self.temperature))
        self._init_y()
        self._init_coeffs()


    def _init_y(self):
        y = np.zeros(self.y_shape)
        y[0] = np.ones_like(self.temperature)
        self.y = y.ravel()

    def _init_coeffs(self):
        S_ = np.zeros(self.y_shape)
        alpha_ = np.zeros(self.y_shape)
        for k in xrange(self.nuclear_charge):
            S_[k] = self.S(k, self.temperature, self.density)
            alpha_[k] = self.alpha(k, self.temperature, self.density)

        self.S_ = S_
        self.alpha_ = alpha_

    def derivs(self, y_, t0):
        """right hand side of the rate equations"""

        dydt = np.zeros(self.y_shape)
        S = self.S_
        alpha = self.alpha_
        ne = self.density

        y = y_.reshape(self.y_shape)

        for k in xrange(self.nuclear_charge + 1): #FIXME: number of charge states
            if k == 0:
                gain = y[k+1]*alpha[k]
                loss = y[k] * S[k]
            elif k == self.nuclear_charge:
                gain = y[k-1]*S[k-1]
                loss = y[k] * alpha[k-1]
            else:
                # eq 2 with alpha[k+1] => alpha[k] substitiution
                gain = y[k-1]*S[k-1] + y[k+1]*alpha[k]
                loss = y[k] * (S[k] + alpha[k-1])

            dydt[k] = ne * (gain - loss)

        return dydt.ravel()

    def solve(self, time):
        solution  = odeint(self.derivs, self.y, time)
        return solution.reshape(time.shape + self.y_shape)


if __name__ == '__main__':
    from atomic_data import AtomicData
    ad = AtomicData.from_element('carbon')
    rt = RateEquations(ad)

    tau_ss = 1e20 / rt.density
    tau_ss *= 1e4
    t = np.linspace(0, 3, 50) * tau_ss
    yy = rt.solve(t)

    from coronal import FractionalAbundance
    import matplotlib.pyplot as plt

    f = FractionalAbundance(yy[-1], rt.temperature, rt.density)

    plt.figure(2); plt.clf()
    f.plot_vs_temperature()
    plt.draw()
    plt.show()
