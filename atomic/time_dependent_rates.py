import numpy as np
import scipy.integrate

from abundance import FractionalAbundance
from coronal import CoronalEquilibrium

class RateEquations(object):
    """
    Attributes:
        atomic_data: an AtomicData object that these equations correspond to.
        nuclear_charge: AtomicData's charge.

        -the rest of these attributes are not set until after initializion-
        temperature:
        density:
        y:
        y_shape:
        dydt:

        S:
        alpha:
    """
    def __init__(self, atomic_data):
        self.atomic_data = atomic_data
        self.nuclear_charge = atomic_data.nuclear_charge

    def _set_temperature_and_density_grid(self, temperature, density):
        self.temperature = temperature
        self.density = density

    def _set_initial_conditions(self):
        """Note here that temperature must be at least as long as density:
        having density be an np.array([1e19,1e20,1e21]) while Te = np.array([10])
        is not permissible."""
        self.y_shape = (self.nuclear_charge + 1, len(self.temperature))
        self._init_y()
        self._init_coeffs()

    def _init_y(self):
        y = np.zeros(self.y_shape)
        y[0] = np.ones_like(self.temperature)
        self.y = y.ravel() #functions like MMA's Flatten[] here
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

    def solve(self, time, temperature, density):
        """
        Integrate the rate equations.

        Args:
            time (np.array): A sequence of time points for which to solve.
            temperature (np.array): Electron temperature grid to solve on [eV].
            density (np.array): Electron density grid to solve on [m^-3].

        Returns:
            a RateEquationSolution
        """

        self._set_temperature_and_density_grid(temperature, density)
        self._set_initial_conditions()
        solution  = scipy.integrate.odeint(self.derivs, self.y, time)

        abundances = []
        for s in solution.reshape(time.shape + self.y_shape):
            abundances.append(FractionalAbundance(self.atomic_data, s, self.temperature,
                self.density))

        return RateEquationsSolution(time, abundances)


class RateEquationsWithDiffusion(RateEquations):
    def derivs(self, y, t):
        dydt = super(self.__class__, self).derivs(y, t)

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
        eq = CoronalEquilibrium(self.atomic_data)
        y_coronal = eq.ionisation_stage_distribution(self.temperature,
                self.density)

        self.y_coronal = y_coronal

    # I guess this is halfway to beng an Immutable Container?
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

        tau = self.times[:, np.newaxis, np.newaxis]
        y = [y.y for y in self.abundances]
        y_bar = scipy.integrate.cumtrapz(y, tau, axis=0)
        y_bar /= tau[1:]

        return self._new_from(tau.squeeze(), y_bar)

    def select_times(self, time_instances):
        indices = np.searchsorted(self.times, time_instances)
        f = [self[i] for i in indices]
        times = self.times[indices]

        return self.__class__(times, f)

    # is this implementing the iterator protocol?
    # https://www.ibm.com/developerworks/library/l-pycon/ ??
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

