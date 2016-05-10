import unittest
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
        """This requires data from ./fetch_adas_data to be in the correct spot."""
        ad = atomic.AtomicData.from_element('Li')
        assert ad

class TestRateCoefficient(unittest.TestCase):
    @unittest.skip("")
    def test___call__(self):
        # rate_coefficient = RateCoefficient(nuclear_charge, element, log_temperature, log_density, log_coeff, name)
        # self.assertEqual(expected, rate_coefficient.__call__(k, Te, ne))
        assert False # TODO: implement your test here

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
    def test_density_grid(self):
        # rate_coefficient = RateCoefficient(nuclear_charge, element, log_temperature, log_density, log_coeff, name)
        # self.assertEqual(expected, rate_coefficient.density_grid())
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

    @unittest.skip("")
    def test_temperature_grid(self):
        # rate_coefficient = RateCoefficient(nuclear_charge, element, log_temperature, log_density, log_coeff, name)
        # self.assertEqual(expected, rate_coefficient.temperature_grid())
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
