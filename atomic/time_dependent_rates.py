import numpy as np
from scipy.integrate import odeint

from abundance import FractionalAbundance

class RateEquations(object):
    def __init__(self, atomic_data):
        self.atomic_data = atomic_data
        self.nuclear_charge = atomic_data.nuclear_charge

    def _set_temperature_and_density_grid(self, temperature, density):
        self.temperature = temperature
        self.density = density

    def _set_initial_conditions(self):
        self.y_shape = (self.nuclear_charge + 1, len(self.temperature))
        self._init_y()
        self._init_coeffs()

    def _init_y(self):
        y = np.zeros(self.y_shape)
        y[0] = np.ones_like(self.temperature)
        self.y = y.ravel()

    def _init_coeffs(self):
        S = np.zeros(self.y_shape)
        alpha = np.zeros(self.y_shape)

        recombination_coeff = self.atomic_data.recombination_coeff
        ionisation_coeff = self.atomic_data.ionisation_coeff
        for k in xrange(self.nuclear_charge):
            S[k] = ionisation_coeff(k, self.temperature, self.density)
            alpha[k] = recombination_coeff(k, self.temperature, self.density)

        self.S = S
        self.alpha = alpha

    def derivs(self, y_, t0):
        """right hand side of the rate equations"""

        dydt = np.zeros(self.y_shape)
        S = self.S
        alpha = self.alpha
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

    def solve(self, time, temperature, density):
        """
        Integrate the rate equations.

        Parameters
        ----------
        time : array
            A sequence of time points for which to solve.
        temperature : array
            Electron temperature grid to solve on [eV].
        density : array
            Electron density grid to solve on [m-3].
        """

        self._set_temperature_and_density_grid(temperature, density)
        self._set_initial_conditions()
        solution  = odeint(self.derivs, self.y, time)

        abundances = []
        for s in solution.reshape(time.shape + self.y_shape):
            abundances.append(FractionalAbundance(self.atomic_data, s, self.temperature,
                self.density))

        return abundances


if __name__ == '__main__':
    pass

