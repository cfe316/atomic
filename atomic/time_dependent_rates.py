import numpy as np
import scipy.integrate

from .abundance import FractionalAbundance
from .collisional_radiative import CollRadEquilibrium


class RateEquations(object):
    """
    Attributes:
        atomic_data: an AtomicData object that these equations correspond to.
        nuclear_charge: AtomicData's charge.
        -the rest of these attributes are not set until after initializion-
        temperature: a list of temperature points at which the rate equations
            will be integrated.
        density: a float represing the density.
        y: an np.array of dimensions self.y_shape.
            Used as initial conditions for the integrator.
        y_shape: (nuclear_charge+1, # temperature points)
        S: ionisation coefficients. Has dimensions of y_shape.
        alpha: recombination coefficients. Has dimensions of y_shape.
            Both have arrays of zeros at their highest index.
        dydt: array with dimensions y_shape. Initialized to zero,
            gets changed by derivs().
    """
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
        """Start with the ions all in the +0 state at t=0."""
        y = np.zeros(self.y_shape)
        y[0] = np.ones_like(self.temperature)
        self.y = y.ravel()  # functions like MMA's Flatten[] here
        self.dydt = np.zeros(self.y_shape)

    def _init_coeffs(self):
        """
        Initialises ionisation and recombination coefficents S and alpha.

        Note that S[-1] and alpha[-1] will both be arrays of zeros.
        (With length of self.temperature)
        """
        S = np.zeros(self.y_shape)
        alpha = np.zeros(self.y_shape)

        recombination_coeff = self.atomic_data.coeffs['recombination']
        ionisation_coeff = self.atomic_data.coeffs['ionisation']
        for k in range(self.nuclear_charge):
            S[k] = ionisation_coeff(k, self.temperature, self.density)
            alpha[k] = recombination_coeff(k, self.temperature, self.density)

        self.S = S
        self.alpha = alpha

    def derivs(self, y_, t0):
        """Construct the r.h.s. of the rate equations.
        This function is executed several times for each odeint step.
        If 100 'times' happen this was executed probably 500 times?
        Also since dydt is an array, the assignment is a copy so
        it gets changed each call.
        """
        dydt = self.dydt
        S = self.S
        alpha_to = self.alpha
        ne = self.density

        # shape the y into a 2D array so that it's easier to apply
        # rate coeffients to specific charge states, then switch it back
        # to a 1D array so that odeint can handle it: y0 must be 1D.
        y = y_.reshape(self.y_shape)
        current = slice(1, -1)  # everything but the first and last
        upper = slice(2, None)
        lower = slice(None, -2)
        dydt[current]  = y[lower] * S[lower]
        dydt[current] += y[upper] * alpha_to[current]
        dydt[current] -= y[current] * S[current]
        dydt[current] -= y[current] * alpha_to[lower]

        current, upper = 0, 1  # neutral and single ionised state
        dydt[current] = y[upper] * alpha_to[current] - y[current] * S[current]

        current, lower = -1, -2  # fully stripped and 1 electron state
        dydt[current] = y[lower] * S[lower] - y[current] * alpha_to[lower]
        dydt *= ne

        return dydt.ravel()

    def solve(self, time, temperature, density):
        """
        Integrate the rate equations.
        Args:
            time (np.array): A sequence of time points for which to solve.
            temperature (np.array): Electron temperature grid to solve on [eV].
            density (float): Electron density grid to solve on [m^-3].
        Returns:
            a RateEquationSolution
        """
        self._set_temperature_and_density_grid(temperature, density)
        self._set_initial_conditions()
        solution = scipy.integrate.odeint(self.derivs, self.y, time)

        abundances = []
        for s in solution.reshape(time.shape + self.y_shape):
            abundances.append(FractionalAbundance(self.atomic_data, s, self.temperature,
                              self.density))

        return RateEquationsSolution(time, abundances)


class RateEquationsWithDiffusion(RateEquations):
    """
    Represents a solution of the rate equations with diffusion
    out of every charge state with a time constant of tau,
    and fueling of neutrals so that the population is constant in time.
    """
    def derivs(self, y, t):
        dydt = super(self.__class__, self).derivs(y, t)

        tau = self.diffusion_time

        dydt -= y/tau
        dydt = dydt.reshape(self.y_shape)
        dydt[0] += 1/tau  # ensures stable population of 1
        return dydt.ravel()

    def solve(self, time, temperature, density, diffusion_time):
        self.diffusion_time = diffusion_time
        return super(self.__class__, self).solve(time, temperature, density)


class RateEquationsSolution(object):
    def __init__(self, times, abundances):
        self.times = times
        self.abundances = abundances

        self._find_parameters()
        self._compute_y_in_collrad()

    def _find_parameters(self):
        y = self.abundances[0]
        self.atomic_data = y.atomic_data
        self.temperature = y.temperature
        self.density = y.density

    def _compute_y_in_collrad(self):
        """
        Compute the corresponding ionisation stage distribution in collrad
        equilibrum.
        """
        eq = CollRadEquilibrium(self.atomic_data)
        y_collrad = eq.ionisation_stage_distribution(self.temperature, self.density)

        self.y_collrad = y_collrad

    # I guess this is halfway to beng an Immutable Container?
    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError('key must be integer.')
        return self.abundances[key]

    def at_temperature(self, temperature_value):
        """
        Finds the time evolution of ionisation states at fixed temperature.

        The temperature is the next one in self.temperature
            that is larger than temperature_value.
        """
        temperature_index = np.searchsorted(self.temperature, temperature_value)

        return np.array([y.y[:, temperature_index] for y in self.abundances])

    def mean_charge(self):
        """Returns an array with shape (len(times), len(temperature))."""
        return np.array([f.mean_charge() for f in self.abundances])

    def steady_state_time(self, rtol=0.01):
        """Find the times at which the ys approach steady-state.

        Returns: an array of steady-state time for each temperature.
        E.g. if it took a 1 eV plasma 1.0s and a 10 eV plasma 0.2s,
        np.array([1.0, 0.2])
        """
        z_mean_ref = self.y_collrad.mean_charge()

        tau_ss = np.zeros_like(self.temperature)
        for t, f in reversed(list(zip(self.times, self.abundances))):
            z_mean = f.mean_charge()
            mask = np.abs(z_mean/z_mean_ref - 1) <= rtol
            tau_ss[mask] = t

        return tau_ss

    def ensemble_average(self):
        tau = self.times[:, np.newaxis, np.newaxis]
        y = [y.y for y in self.abundances]
        # y is a list of np.arrays. len(y) is nTimes, and
        # the contained arrays have shape (nuclear_charge + 1, nTemperatures)
        y_bar = scipy.integrate.cumtrapz(y, x=tau, axis=0)
        y_bar /= tau[1:]
        # y_bar is a 3D np.array with shape
        # (nTimes - 1, nuclear_charge + 1, nTemperatures)
        return self._new_from(tau.squeeze(), y_bar)

    def select_times(self, time_instances):
        indices = np.searchsorted(self.times, time_instances)
        f = [self[int(i)] for i in indices]
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
