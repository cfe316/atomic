import unittest
import numpy as np
import atomic

class TestRateEquations(unittest.TestCase):
    def setUp(self):
        self.ad = atomic.element('lithium')
        self.temperature = np.logspace(0, 3, 50)
        self.density = 1e19
        self.times = np.logspace(-7, 0, 120)
        self.times -= self.times[0]
        self.rt = atomic.RateEquations(self.ad)

    def test_S(self):
        """Tests that that RateEquations are using the right ionisation coefficients."""
        self.rt._set_temperature_and_density_grid(self.temperature, self.density)
        self.rt._set_initial_conditions()
        S = self.rt.S
        for k in range(self.ad.nuclear_charge):
            expected = S[k,0]
            result = self.ad.coeffs['ionisation'](k,self.temperature[0],self.density)
            self.assertAlmostEqual(expected, result, 3)
        # test that highest part of S is zero. S[-1] and alpha[-1] are zeros and are
        # never accessed.
        expected = np.zeros(self.rt.y_shape[1])
        result = S[-1]
        np.testing.assert_equal(expected, result)

    @unittest.skip("")
    def test_derivs(self):
        # rate_equations = RateEquations(atomic_data)
        # self.assertEqual(expected, rate_equations.derivs(y_, t0))
        assert False # TODO: implement your test here

    @unittest.skip("")
    def test_solve(self):
        # rate_equations = RateEquations(atomic_data)
        # self.assertEqual(expected, rate_equations.solve(time, temperature, density))
        assert False # TODO: implement your test here

class TestRateEquationsWithDiffusion(unittest.TestCase):
    def test_diffusion(self):
        """Tests that the total number of particles stays constant at 1.0."""
        ad = atomic.element('carbon')
        temperature = np.logspace(0, 3, 100)
        density = 1e19
        tau = 1e-3
        times = np.logspace(-7, 0, 120)
        times -= times[0]
        rt = atomic.RateEquationsWithDiffusion(ad)
        yy = rt.solve(times, temperature, density, tau)
        expected = np.ones(len(times))
        result = [np.sum(yy.abundances[i].y)/len(temperature) for i in range(len(times))]
        np.testing.assert_array_almost_equal(expected, result)

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
