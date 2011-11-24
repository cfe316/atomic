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
        self.dydt = np.zeros(self.y_shape)

    def _init_coeffs(self):
        S = np.zeros(self.y_shape)
        alpha = np.zeros(self.y_shape)

        recombination_coeff = self.atomic_data.coeffs['recombination']
        ionisation_coeff = self.atomic_data.coeffs['ionisation']
        for k in xrange(self.nuclear_charge):
            S[k] = ionisation_coeff(k, self.temperature, self.density)
            alpha[k] = recombination_coeff(k, self.temperature, self.density)

        self.S = S
        self.alpha = alpha

    def derivs(self, y_, t0):
        """right hand side of the rate equations"""

        dydt = self.dydt
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

        return RateEquationsSolution(time, abundances)


class RateEquationsSolution(object):
    def __init__(self, times, abundances):
        self.times = times
        self.abundances = abundances

        self._find_parameters()
        self._compute_y_in_coronal()

    def _find_parameters(self):
        y = self.abundances[0]
        self.atomic_data = y.atomic_data
        self.temperature = y.temperature
        self.density = y.density

    def _compute_y_in_coronal(self):
        """
        Compute the corresponding ionisation stage distribution in coronal
        equilibrum.
        """
        from coronal import CoronalEquilibrium
        eq = CoronalEquilibrium(self.atomic_data)
        y_coronal = eq.ionisation_stage_distribution(self.temperature,
                self.density)

        self.y_coronal = y_coronal

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError('key must be integer.')
        return self.abundances[key]

    def at_temperature(self, temperature_value):
        temperature_index = np.searchsorted(self.temperature,
                temperature_value)

        return np.array([y.y[:, temperature_index] for y in self.abundances])

    def mean_charge(self):
        return np.array([f.mean_charge() for f in self.abundances])

    def steady_state_time(self, rtol=0.01):
        z_mean_ref = self.y_coronal.mean_charge()

        tau_ss = np.zeros_like(self.temperature)
        for t, f in reversed(zip(self.times, self.abundances)):
            z_mean = f.mean_charge()
            mask = np.abs(z_mean/z_mean_ref - 1) <= rtol
            tau_ss[mask] = t

        return tau_ss


if __name__ == '__main__':
    pass

