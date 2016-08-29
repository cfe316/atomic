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

    def test_element_data_dict_no_cx_power(self):
        data1 = atomic.atomic_data._element_data_dict('li', 96)
        expected = {'recombination': 'acd96_li.dat',
                    'line_power': 'plt96_li.dat',
                    'ionisation': 'scd96_li.dat',
                    'continuum_power': 'prb96_li.dat'}
        self.assertEqual(data1, expected)

    def test_element_data_dict_cx_power(self):
        data1 = atomic.atomic_data._element_data_dict('ar', 89, has_cx_power=True)
        self.assertEqual(data1['cx_power'], 'prc89_ar.dat')

    def test_element_data_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            atomic.atomic_data._element_data('adamantium')

    def test_from_element(self):
        """Requires data from ./fetch_adas_data to be in the correct spot."""
        ad = atomic.AtomicData.from_element('Li')
        self.assertEqual(ad.nuclear_charge,3)
        self.assertEqual(ad.element,'Li')
        rc = ad.coeffs['ionisation']
        self.assertIsInstance(rc, atomic.atomic_data.RateCoefficient)

    def test_make_element_initial_uppercase(self):
        ad = atomic.AtomicData.from_element('c')
        self.assertEqual(ad.element,'C')

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

    def test_log10_one_one(self):
        tp = self.rc.temperature_grid[0]
        dp = self.rc.density_grid[0]
        log_rc = self.rc.log10(0, tp, dp)
        expected = np.array([-22.8983])
        np.testing.assert_allclose(expected, log_rc)

    def test_log10_many_many(self):
        tg = self.rc.temperature_grid
        dg = self.rc.density_grid
        log_rcs = self.rc.log10(0,tg[:len(dg)], dg)
        expected = np.array([-22.8983 , -19.74759, -17.24704, -15.99432, -15.06829, -13.54429,
                             -13.24645, -13.07121, -12.95795, -12.73103, -12.60551, -12.28684,
                             -12.20186, -12.11832, -12.11021, -12.08091])
        np.testing.assert_allclose(expected, log_rcs)

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
