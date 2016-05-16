import unittest
import numpy as np
import atomic

class TestAtomicData(unittest.TestCase):
    def test_element_data_names_abbreviated_and_long(self):
        """This does not require that the user has downloaded data"""
        data1 = atomic.atomic_data._element_data('Li')
        data2 = atomic.atomic_data._element_data('lithium')
        self.assertEqual(data1['recombination'],'acd96_li.dat')
        self.assertEqual(data2['recombination'],'acd96_li.dat')

    def test_element_data_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            atomic.atomic_data._element_data('imaginarium')

    def test_from_element(self):
        """Requires data from ./fetch_adas_data to be in the correct spot."""
        ad = atomic.AtomicData.from_element('Li')
        self.assertEqual(ad.nuclear_charge,3)
        self.assertEqual(ad.element,'Li')
        rc = ad.coeffs['ionisation']
        self.assertIsInstance(rc, atomic.atomic_data.RateCoefficient)

class TestRateCoefficient(unittest.TestCase):
    def setUp(self):
        data = atomic.atomic_data._element_data('Li')
        self.ionis = atomic.atomic_data._full_path(data['ionisation'])
        self.rc = atomic.atomic_data.RateCoefficient.from_adf11(self.ionis)

    def test_density_grid(self):
        length = 16
        self.assertEqual(length, len(self.rc.density_grid))
        min_density = 1.0e14
        self.assertEqual(min_density, self.rc.density_grid[0])

    def test_temperature_grid(self):
        """Test that temperature_grid returns values in [eV]"""
        length = 25
        self.assertEqual(length, len(self.rc.temperature_grid))
        min_temperature = 2.0009e-1
        result = self.rc.temperature_grid[0]
        self.assertAlmostEqual(min_temperature, result, 4)

    def test___call__(self):
        """Units are in [m^3/s]"""
        expected = np.array([2.068e-13])
        result = self.rc(0, 10, 1e19)
        self.assertAlmostEqual(expected, result, 3)

    @unittest.skip("")
    def test___init__(self):
        # rate_coefficient = RateCoefficient(nuclear_charge, element, log_temperature, log_density, log_coeff, name)
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_copy(self):
        # rate_coefficient = RateCoefficient(nuclear_charge, element, log_temperature, log_density, log_coeff, name)
        # self.assertEqual(expected, rate_coefficient.copy())
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_from_adf11(self):
        # rate_coefficient = RateCoefficient(nuclear_charge, element, log_temperature, log_density, log_coeff, name)
        # self.assertEqual(expected, rate_coefficient.from_adf11(name))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_log10(self):
        # rate_coefficient = RateCoefficient(nuclear_charge, element, log_temperature, log_density, log_coeff, name)
        # self.assertEqual(expected, rate_coefficient.log10(k, Te, ne))
        assert False # TODO: implement your test here


class TestZeroCoefficient(unittest.TestCase):
    @unittest.skip("")
    def test___call__(self):
        # zero_coefficient = ZeroCoefficient()
        # self.assertEqual(expected, zero_coefficient.__call__(k, Te, ne))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test___init__(self):
        # zero_coefficient = ZeroCoefficient()
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
