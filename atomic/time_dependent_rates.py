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

    def derivs_optimized(self, y_, t0):
        """
        Optimised version of derivs using array slicing.  It should give the
        same as derivs().
        """

        dydt = self.dydt
        S = self.S
        alpha_to = self.alpha
        ne = self.density

        y = y_.reshape(self.y_shape)
        current = slice(1, -1)
        upper = slice(2, None)
        lower = slice(None, -2)
        dydt[current]  = y[lower] * S[lower]
        dydt[current] += y[upper] * alpha_to[current]
        dydt[current] -= y[current] * S[current]
        dydt[current] -= y[current] * alpha_to[lower]

        current, upper = 0, 1 # neutral and single ionised state
        dydt[current] = y[upper] * alpha_to[current] - y[current] * S[current]

        current, lower = -1, -2 # fully stripped and 1 electron state
        dydt[current] = y[lower] * S[lower] - y[current] * alpha_to[lower]
        dydt *= ne

        return dydt.ravel()

    def derivs_optimized_2(self, y_, t0):
        """
        Optimised version of derivs using the roll function.  Probably
        consumes more memory than derivs_optimized().  However it is kept
        here for eduactional purposes.
        """

        dydt = self.dydt
        S = self.S
        alpha_to = self.alpha
        ne = self.density

        y = y_.reshape(self.y_shape)

        y_lower = np.roll(y, +1, axis=0)
        y_upper = np.roll(y, -1, axis=0)
        S_lower = np.roll(S, +1, axis=0)
        alpha_to_lower = np.roll(alpha_to, +1, axis=0)

        dydt  = y_lower * S_lower
        dydt += y_upper * alpha_to
        dydt -= y * S
        dydt -= y * alpha_to_lower

        current, upper = 0, 1 # neutral and single ionised state
        dydt[current] = y[upper] * alpha_to[current] - y[current] * S[current]

        current, lower = -1, -2 # fully stripped and 1 electron state
        dydt[current] = y[lower] * S[lower] - y[current] * alpha_to[lower]
        dydt *= ne

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
        solution  = odeint(self.derivs_optimized, self.y, time)

        abundances = []
        for s in solution.reshape(time.shape + self.y_shape):
            abundances.append(FractionalAbundance(self.atomic_data, s, self.temperature,
                self.density))

        return RateEquationsSolution(time, abundances)


class RateEquationsWithDiffusion(RateEquations):
    def derivs_optimized(self, y, t):
        dydt = super(self.__class__, self).derivs_optimized(y, t)

        ne = self.density
        tau = self.diffusion_time

        dydt -= y/tau
        return dydt

    def solve(self, time, temperature, density, diffusion_time):
        self.diffusion_time = diffusion_time
        return super(self.__class__, self).solve(time, temperature, density)


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

    def ensemble_average(self):
        from scipy.integrate import cumtrapz

        tau = self.times[:, np.newaxis, np.newaxis]
        y = [y.y for y in self.abundances]
        y_bar = cumtrapz(y, tau, axis=0)
        y_bar /= tau[1:]

        return self._new_from(tau.squeeze(), y_bar)

    def select_times(self, time_instances):
        indices = np.searchsorted(self.times, time_instances)
        f = [self[i] for i in indices]
        times = self.times[indices]

        return self.__class__(times, f)

    def __iter__(self):
        for y in self.abundances:
            yield y

    def _new_from(self, times, concentrations):
        new_concentrations = []
        for y in concentrations:
            f = FractionalAbundance(self.atomic_data, y, self.temperature,
                    self.density)
            new_concentrations.append(f)
        return self.__class__(times, new_concentrations)


if __name__ == '__main__':
    pass

