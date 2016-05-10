import unittest

class TestRateEquations(unittest.TestCase):
    @unittest.skip("")
    def test___init__(self):
        # rate_equations = RateEquations(atomic_data)
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_derivs(self):
        # rate_equations = RateEquations(atomic_data)
        # self.assertEqual(expected, rate_equations.derivs(y_, t0))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_derivs_optimized(self):
        # rate_equations = RateEquations(atomic_data)
        # self.assertEqual(expected, rate_equations.derivs_optimized(y_, t0))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_derivs_optimized_2(self):
        # rate_equations = RateEquations(atomic_data)
        # self.assertEqual(expected, rate_equations.derivs_optimized_2(y_, t0))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_solve(self):
        # rate_equations = RateEquations(atomic_data)
        # self.assertEqual(expected, rate_equations.solve(time, temperature, density))
        assert False # TODO: implement your test here

class TestRateEquationsWithDiffusion(unittest.TestCase):
    @unittest.skip("")
    def test_derivs_optimized(self):
        # rate_equations_with_diffusion = RateEquationsWithDiffusion()
        # self.assertEqual(expected, rate_equations_with_diffusion.derivs_optimized(y, t))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_solve(self):
        # rate_equations_with_diffusion = RateEquationsWithDiffusion()
        # self.assertEqual(expected, rate_equations_with_diffusion.solve(time, temperature, density, diffusion_time))
        assert False # TODO: implement your test here

class TestRateEquationsSolution(unittest.TestCase):
    @unittest.skip("")
    def test___getitem__(self):
        # rate_equations_solution = RateEquationsSolution(times, abundances)
        # self.assertEqual(expected, rate_equations_solution.__getitem__(key))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test___init__(self):
        # rate_equations_solution = RateEquationsSolution(times, abundances)
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test___iter__(self):
        # rate_equations_solution = RateEquationsSolution(times, abundances)
        # self.assertEqual(expected, rate_equations_solution.__iter__())
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_at_temperature(self):
        # rate_equations_solution = RateEquationsSolution(times, abundances)
        # self.assertEqual(expected, rate_equations_solution.at_temperature(temperature_value))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_ensemble_average(self):
        # rate_equations_solution = RateEquationsSolution(times, abundances)
        # self.assertEqual(expected, rate_equations_solution.ensemble_average())
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_mean_charge(self):
        # rate_equations_solution = RateEquationsSolution(times, abundances)
        # self.assertEqual(expected, rate_equations_solution.mean_charge())
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_select_times(self):
        # rate_equations_solution = RateEquationsSolution(times, abundances)
        # self.assertEqual(expected, rate_equations_solution.select_times(time_instances))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_steady_state_time(self):
        # rate_equations_solution = RateEquationsSolution(times, abundances)
        # self.assertEqual(expected, rate_equations_solution.steady_state_time(rtol))
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
