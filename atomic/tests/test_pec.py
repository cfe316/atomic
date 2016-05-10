import unittest

class TestTransition(unittest.TestCase):
    @unittest.skip("")
    def test___init__(self):
        # transition = Transition(type_, element, nuclear_charge, charge, wavelength, temperature, density, pec)
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_energy(self):
        # transition = Transition(type_, element, nuclear_charge, charge, wavelength, temperature, density, pec)
        # self.assertEqual(expected, transition.energy())
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_interpolate(self):
        # transition = Transition(type_, element, nuclear_charge, charge, wavelength, temperature, density, pec)
        # self.assertEqual(expected, transition.interpolate(temperature_grid, density_grid))
        assert False # TODO: implement your test here

class TestTransitionPool(unittest.TestCase):
    @unittest.skip("")
    def test___init__(self):
        # transition_pool = TransitionPool(transitions)
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test___iter__(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.__iter__())
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_append_file(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.append_file(filename))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_append_files(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.append_files(files))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_coeffs(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.coeffs())
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_create_atomic_data(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.create_atomic_data(ad))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_energies(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.energies())
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_filter_energy(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.filter_energy(lo, hi, unit))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_filter_type(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.filter_type(*type_names))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_from_adf15(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.from_adf15(files))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_interpolate(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.interpolate(temperature_grid, density_grid))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_size(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.size())
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_sum_transitions(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.sum_transitions())
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_wavelengths(self):
        # transition_pool = TransitionPool(transitions)
        # self.assertEqual(expected, transition_pool.wavelengths())
        assert False # TODO: implement your test here

class TestPBremsstrahlung(unittest.TestCase):
    @unittest.skip("")
    def test_p_bremsstrahlung(self):
        # self.assertEqual(expected, P_bremsstrahlung(k, Te, ne))
        assert False # TODO: implement your test here

class TestCoefficientFactory(unittest.TestCase):
    @unittest.skip("")
    def test___init__(self):
        # coefficient_factory = CoefficientFactory(atomic_data, transition_pool, clip_limit)
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_create(self):
        # coefficient_factory = CoefficientFactory(atomic_data, transition_pool, clip_limit)
        # self.assertEqual(expected, coefficient_factory.create(temperature_grid, density_grid))
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
