import os

import numpy as np
from scipy.interpolate import RectBivariateSpline

from adf11 import Adf11

datatype_abbrevs = {
        'ionisation' : 'scd',
        'recombination' : 'acd',
        'continuum_power' : 'prb',
        'line_power' : 'plt',
        'cx_power' : 'prc',
        'ionisation_potential' : 'ecd',
}

# The system of registering element names, symbols, years,
# and what datatypes they have could certainly be improved. However it works at the moment.

lithium_year = 96
lithium_symbol = 'li'
#it might be nice to get a prc data! doesn't seem to be available

argon_year = 89
argon_symbol = 'ar'
argon_has_cx_power = True

carbon_year = 96
carbon_symbol = 'c'
carbon_has_cx_power = True

nitrogen_year = 96
nitrogen_symbol = 'n'

neon_year = 96
neon_symbol = 'ne'

# imaginary element, for testing purposes
imaginarium_year = 0
imaginarium_data = {}

def _make_filename(el_symbol, el_year, datatype):
    """_make_filename('ne', 96, 'scd') -> 'scd96_ne.dat' """
    return datatype + str(el_year) + '_' + el_symbol + '.dat'

def _element_data_dict(el_symbol, el_year, has_cx_power=False):
    """Give a dictionary of ADF11 file names for the given element and year
       and whether or not it has cx_power
    """
    data_dict = {}
    for key, value in datatype_abbrevs.iteritems():
        data_dict[key] = _make_filename(el_symbol, el_year, value)
    if not has_cx_power:
        data_dict.pop('cx_power', None)
    return data_dict

lithium_data  = _element_data_dict(lithium_symbol,  lithium_year)
argon_data    = _element_data_dict(argon_symbol,    argon_year,  argon_has_cx_power)
carbon_data   = _element_data_dict(carbon_symbol,   carbon_year, carbon_has_cx_power)
nitrogen_data = _element_data_dict(nitrogen_symbol, nitrogen_year)
neon_data     = _element_data_dict(neon_symbol,     neon_year)

def _element_data(element):
    """Give a dictionary of ADF11 file names available for the given element.

    Args:
        element: a string like 'Li' or 'lithium'
    Returns:
        a dictionary of file names.

    {'ionisation' : 'scd96_li.dat',
    'recombination' : 'acd96_li.dat',
    ...
    }

    This could presumably be made more general, especially with automated lookup of files.
    """
    e = element.lower()
    if e in ['li', 'lithium']:
        return lithium_data
    elif e in ['c', 'carbon']:
        return carbon_data
    elif e in ['ar', 'argon']:
        return argon_data
    elif e in ['ne', 'neon']:
        return neon_data
    elif e in ['n', 'nitrogen']:
        return nitrogen_data
    else:
        raise NotImplementedError('unknown element: %s' % element)


def _full_path(file_):
    """ Figure out the location of an atomic datafile.
        Files are all located in adas_data, which is at the same level
        as the package directory, so to get there we must go up one.
    """
    # __file__ is the location of atomic_data.py
    module_path = os.path.dirname(os.path.realpath( __file__ ))
    return os.path.realpath(os.path.join(module_path, '..', 'adas_data', file_))


class AtomicData(object):
    """
    Attributes:
        element (string): the element symbol, like 'Li' or 'C'
        coeffs (dict): a dictionary of RateCoefficient objects
            with keys like 'ionisation'
        nuclear_charge (int) : the element's Z

    """

    def __init__(self, coefficients):
        """
        Args:
            coefficients (dict):
                The rate coefficients, as RateCoefficient objects.
        """
        self.coeffs = coefficients
        self._check_consistency()
        self._make_element_initial_uppercase()

    def copy(self):
        """Make a new object that is a copy of this one.

        This is used in pec.py's TransitionPool.
        """
        new_coeffs = {}
        #iteritems() is a method on dicts that gives an iterator
        for key, value in self.coeffs.iteritems():
            new_coeffs[key] = value.copy()

        return self.__class__(new_coeffs)

    def _check_consistency(self):
        """Add the nuclear_charge and element attributes.

        Each individual RateCoefficient object has its own copy of the
        nuclear_charge, say 3 for Li. Because a set() can only contain one copy
        of the number 3, testing for len == 1 ensures that all the files
        correspond to the same nucleus.
        """
        nuclear_charge = set()
        element = set()
        #coeff are the RateCoefficient objects
        for coeff in self.coeffs.values():
            nuclear_charge.add(coeff.nuclear_charge)
            element.add(coeff.element.lower())

        assert len(nuclear_charge) == 1, 'inconsistent nuclear charge.'
        assert len(element) == 1, 'inconsistent element name.'

        self.nuclear_charge = nuclear_charge.pop()
        self.element = element.pop()

    @classmethod
    def from_element(cls, element):
        """This is a variant constructor.
        It returns an instance of the class for a given element,
        looking up data values automatically. This is in contrast to the regular constructor,
        which requires you to already have the coeffiecients.

        Args:
            element: a string like 'Li' or 'lithium'
        Returns:
            An AtomicData class
        """
        # gets a list of filenames for 'ionisation', 'recombination', etc.
        element_data = _element_data(element)

        coefficients = {}
        for key, value in element_data.iteritems():
            fullfilename = _full_path(value)
            coefficients[key] = RateCoefficient.from_adf11(fullfilename)

        return cls(coefficients)

    def _make_element_initial_uppercase(self):
        e = self.element
        self.element = e[0].upper() + e[1:]

class RateCoefficient(object):
    """Interpolation tables for the rate of some physical process.

    Contains one 2D spline interpolator for each charge state,
    of an element, for one process like 'ionisation', 'recombination'.

    Attributes:
        nuclear_charge (int): The element's Z.
        element (str): Short element name like 'c' or 'ar'.
        adf11_file (str): The /full/filename it came from.
        log_temperature: np.array of log10 of temperature values
        log_density: np.array of log10 of density values
        log_coeff: a 3D np.array with shape (Z, temp, dens)
        splines: list of scipy.interpolate.fitpack2.RectBivariateSpline
            The list has length Z and is interpolations of log_coeff.

    NOTE: With the addition of ionisation_potentials, the RateCoefficient 
    object is also storing tables of the ionisation potentials, even though
    it is not at all the same thing as a rate coefficient. This is a kludge
    for now.
    """
    def __init__(self, nuclear_charge, element, log_temperature, log_density,
            log_coeff, name=None):
        self.nuclear_charge = nuclear_charge
        self.element = element
        self.adf11_file = name

        self.log_temperature = log_temperature
        self.log_density = log_density
        self.log_coeff = log_coeff

        self._compute_interpolating_splines()

    @classmethod
    def from_adf11(cls, name):
        """Instantiate a RateCoefficient by reading in an adf11 file.

        Args:
            name: The /full/name/of/an/adf11 file.
        """
        adf11_data = Adf11(name).read()
        nuclear_charge = adf11_data['charge']
        element = adf11_data['element']
        filename = adf11_data['name']
        #filename is probably redundant:
        assert name == filename

        log_temperature = adf11_data['log_temperature']
        log_density = adf11_data['log_density']
        log_coeff = adf11_data['log_coeff']

        return cls(nuclear_charge, element, log_temperature, log_density,
                log_coeff, name=filename)

    def copy(self):
        log_temperature = self.log_temperature.copy()
        log_density = self.log_density.copy()
        log_coeff = self.log_coeff.copy()
        cls = self.__class__(self.nuclear_charge, self.element, log_temperature,
                log_density, log_coeff, self.adf11_file)
        return cls

    def _compute_interpolating_splines(self):
        self.splines = []
        # if we want to implement metastables there are more sets of coefficients
        # than just for nuclear charge. This should be TODO'd.
        # Also for stuff like ecd: ionisation potentials there is nuclear_charge + 1
        for k in xrange(self.nuclear_charge):
            x = self.log_temperature
            y = self.log_density
            z = self.log_coeff[k]
            self.splines.append(RectBivariateSpline(x, y, z))

    def __call__(self, k, Te, ne):
        """Evaulate the ionisation/recombination coefficients of
        k'th atomic state at a given temperature and density.

        Args:
            k (int): Ionising or recombined ion stage,
                between 0 and k=Z-1, where Z is atomic number.
            Te (array_like): Temperature in [eV].
            ne (array_like): Density in [m-3].

        Returns:
            c (array_like): Rate coefficent in [m3/s].
        """
        c = self.log10(k, Te, ne)
        return np.power(10, c)

    def log10(self, k, Te, ne):
        """Evaulate the logarithm of ionisation/recombination coefficients of
        k'th atomic state at a given temperature and density.

        If asked to evaluate for Te = np.array([1,2,3])
            and ne = np.array([a,b,c]),
            it will return coeffs at (1,a), (2,b), and (3,c),
            not a 3x3 matrix of all the grid points.
            I'm not sure yet if __call__ is typically
            done with 1D or 2D arrays.

        Args:
            k (int): Ionising or recombined ion stage.
                Between 0 and k=Z-1, where Z is atomic number.
            Te (array_like): Temperature in [eV].
            ne (array_like): Density in [m-3].

        Returns:
            c (array_like): log10(rate coefficent in [m3/s])
        """

        Te, ne = np.broadcast_arrays(Te, ne)
        log_temperature = np.log10(Te)
        log_density = np.log10(ne)

        c = self.splines[k](log_temperature, log_density)
        return c.diagonal()

    @property
    def temperature_grid(self):
        """Get a np.array of temperatures in [eV]."""
        return 10**(self.log_temperature)

    @property
    def density_grid(self):
        """Get an np.array of densities in [m^3]."""
        return 10**(self.log_density)

from sys import float_info
class ZeroCoefficient(RateCoefficient):
    """A subclass of RateCoefficient"""
    def __init__(self):
        pass

    def __call__(self, k, Te, ne):
        Te, ne = np.broadcast_arrays(Te, ne)
        return float_info.min * np.ones_like(Te)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
