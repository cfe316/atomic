import unittest
import atomic
import numpy as np

class TestElectronCooling(unittest.TestCase):
    def setUp(self):
        ad = atomic.element('li')
        eq = atomic.CoronalEquilibrium(ad)

        self.temperature = np.logspace(0, 3, 50)
        self.electron_density = 1e19
        # y is a FractionalAbundance object.
        y = eq.ionisation_stage_distribution(self.temperature,
                self.electron_density)
        self.elc = atomic.ElectronCooling(y, neutral_fraction=1e-2)

    def test_keys(self):
        """Makes sure ElectronCooling has all the right keys"""
        expected = ['ionisation', 'recombination', 
                    'cx_power', 'line_power', 
                    'continuum_power', 'rad_total',
                    'total']
        result = self.elc.power.keys()
        self.assertItemsEqual(expected, result)

    def test_rad_total(self):
        """Tests that rad_total is what I think it is."""
        p = self.elc.power
        expected = p['rad_total'] 
        result = p['line_power'] + p['cx_power'] + p['continuum_power']
        np.testing.assert_allclose(expected, result)

    def test_equilbrium(self):
        """Test that ionisation and recombination powers are opposite.

        Hence, total = rad_total.
        """
        ion = self.elc.power['ionisation']
        negrecomb = -self.elc.power['recombination']
        total = self.elc.power['total']
        rad_total = self.elc.power['rad_total']
        np.testing.assert_allclose(ion, negrecomb)
        np.testing.assert_allclose(total, rad_total)

if __name__ == '__main__':
    unittest.main()
