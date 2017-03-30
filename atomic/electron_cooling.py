import numpy as np
import matplotlib.pyplot as plt
from atomic_data import ZeroCoefficient
from radiation import Radiation

# This class is almost a copy of Radiation; only 
# _get_staging_coeffs / _get_power_coeffs and _compute_power are different.
class ElectronCooling(object):
    """
    Electron cooling power is radiation + ionisation - recombination.

    This class calculates electron cooling power for an ionisation 
    stage distribution at given electron densities and temperatures.

    In collisional radiative equilibrium, ElectronCooling.power will
    equal Radiation.power, since the same amount of ions are being 
    ionised and recombined each second.

    Attributes:
        rad: a Radiation object.
        y: a FractionalAbundance object.
        atomic_data: that FrAb's atomic data.
        temperature (np.array): that FrAb's temperature list.
        electron_density (np.array or float): that FrAb's density list.
        impurity_fraction: ???
            n_impurity = n_e * impurity_fraction
        neutral_fraction: fraction of neutral hydrogen, for cx_power.
            n_n = n_e * neutral_fraction
    """
    def __init__(self, ionisation_stage_distribution, impurity_fraction=1.,
            neutral_fraction=0.):
        self.y = ionisation_stage_distribution
        self.atomic_data = ionisation_stage_distribution.atomic_data

        self.temperature = self.y.temperature
        self.electron_density = self.y.density

        self.impurity_fraction = impurity_fraction
        self.neutral_fraction = neutral_fraction

        self.eV = 1.6e-19

        self.rad = Radiation(ionisation_stage_distribution, impurity_fraction,
            neutral_fraction)


    @property
    def power(self):
        return self._compute_power()

    @property
    def specific_power(self):
        """Power per electron per impurity nucleus, [W m^3]"""
        power = self.power
        for key in power.keys():
            power[key] /= self.electron_density * self.get_impurity_density()
        return power

    def epsilon(self, tau):
        """Electron cooling energy per ion [eV], given the lifetime tau."""
        eps = {}
        for k in 'rad_total', 'total':
            eps[k] = self.specific_power[k] * self.electron_density * tau / self.eV
        return eps

    def get_impurity_density(self):
        return self.impurity_fraction * self.electron_density

    def get_neutral_density(self):
        return self.neutral_fraction * self.electron_density

    def _get_staging_coeffs(self):
        """Get a dict of RateCoefficient objects.

        Returns:
            {'ionisation':          : <RateCoefficient object>,
             'recombination'        : <RateCoefficient object>,
             'ionisation_potential' : <RateCoefficient object>}
        """
        staging_coeffs = {}
        for key in ['ionisation', 'recombination', 'ionisation_potential']:
            staging_coeffs[key] = self.atomic_data.coeffs.get(key,
                    ZeroCoefficient())
        return staging_coeffs

    def _compute_power(self):
        """
        Compute electron cooling power density in [W/m3].
        """

        shape_ = self.atomic_data.nuclear_charge, self.temperature.shape[0]

        staging_coeffs = self._get_staging_coeffs()
        staging_power = {}
        staging_power_keys = 'ionisation', 'recombination'
        for key in staging_power_keys:
            staging_power[key] = np.zeros(shape_)

        ne = self.electron_density
        ni = self.get_impurity_density()
        y = self.y # a FractionalAbundance

        for k in xrange(self.atomic_data.nuclear_charge):
            # in joules per ionisation stage transition
            # note that the temperature and density don't matter for the potential.
            potential = self.eV * staging_coeffs['ionisation_potential'](k, self.temperature, self.electron_density)
            for key in staging_power_keys:
                coeff = staging_coeffs[key](k, self.temperature,
                        self.electron_density)

                # somewhat ugly...
                if key == 'recombination':
                    sign, shift = -1, 1
                else:
                    sign, shift = 1, 0

                scale = ne * ni * y.y[k+shift] * potential

                staging_power[key][k] = sign * scale * coeff

        # sum over all ionisation stages
        for key in staging_power.keys():
            staging_power[key] = staging_power[key].sum(0)

        # now get the radiation power.
        # gets a dict with keys line, continuum, cx, total
        rad_power = self.rad._compute_power() 
        # save rad_total for later
        rad_total = rad_power.pop('total')

        # this is a Bad Idea on how to merge two dicts but oh well
        # http://stackoverflow.com/questions/38987/how-can-i-merge-two-python-dictionaries-in-a-single-expression
        cooling_power = dict(rad_power.items() + staging_power.items())
        cooling_power['total'] = reduce(lambda x,y: x+y,
                cooling_power.values())
        cooling_power['rad_total'] = rad_total

        return cooling_power
