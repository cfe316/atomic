import unittest
import atomic
import numpy as np

class TestRadiation(unittest.TestCase):
    def setUp(self):
        ad1 = atomic.element('carbon')
        ad2 = atomic.element('li')
        eq1 = atomic.CoronalEquilibrium(ad1)
        eq2 = atomic.CoronalEquilibrium(ad2)

        te = np.logspace(0, 3, 50)
        ne = 1e19
        self.y1 = eq1.ionisation_stage_distribution(te, ne)
        self.y2 = eq2.ionisation_stage_distribution(te, ne)

    # The tests of get_impurity_density and get_neutral_density could
    # be rewritten more as unit tests, by mocking up a y.
    def test_get_impurity_density_finite(self):
        rad = atomic.Radiation(self.y1, impurity_fraction=0.1)
        expected = 1e18
        result = rad.get_impurity_density()
        self.assertEqual(expected, result)

    def test_get_impurity_density_finite2(self):
        """There are 10 times as many impurities as main ions."""
        rad = atomic.Radiation(self.y1, impurity_fraction=10)
        expected = 1e20
        result = rad.get_impurity_density()
        self.assertEqual(expected, result)

    def test_get_impurity_density_default_1(self):
        rad = atomic.Radiation(self.y1)
        expected = 1e19
        result = rad.get_impurity_density()
        self.assertEqual(expected, result)

    def test_get_impurity_density_zero(self):
        rad = atomic.Radiation(self.y1, impurity_fraction=0)
        expected = 0
        result = rad.get_impurity_density()
        self.assertEqual(expected, result)

    def test_get_neutral_density(self):
        rad = atomic.Radiation(self.y1, neutral_fraction=1e-2)
        expected = 1e17
        result = rad.get_neutral_density()
        self.assertEqual(expected, result)

    def test_get_neutral_density_default_zero(self):
        rad = atomic.Radiation(self.y1)
        expected = 0.
        result = rad.get_neutral_density()
        self.assertEqual(expected, result)

    @unittest.skip("")
    def test_power(self):
        rad = atomic.Radiation(self.y1)
        power = rad.power


    @unittest.skip("")
    def test_specific_power(self):
        # radiation = Radiation(ionisation_stage_distribution, impurity_fraction, neutral_fraction)
        # self.assertEqual(expected, radiation.specific_power())
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
