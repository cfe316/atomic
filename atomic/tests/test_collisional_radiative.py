import unittest
import numpy as np
import atomic

class TestCollRadEquilibrium(unittest.TestCase):
    def setUp(self):
        """This is more of an Integration Test than a unit test."""
        self.ad = atomic.element('Li')
        self.eq = atomic.CollRadEquilibrium(self.ad)

    def test___init__(self):
        assert self.eq
        self.assertIsInstance(self.eq.atomic_data, atomic.AtomicData)
        self.assertEqual(self.eq.nuclear_charge, 3)
        ionc = self.eq.ionisation_coeff
        recc = self.eq.ionisation_coeff
        rc_class = atomic.atomic_data.RateCoefficient
        self.assertIsInstance(ionc, rc_class)
        self.assertIsInstance(recc, rc_class)

    def test_ionisation_stage_distribution_cold(self):
        """Test that a very cold plasma will be almost entirely neutrals.
        """
        Te = np.array([0.1])
        ne = np.array([1e19])
        fab = self.eq.ionisation_stage_distribution(Te, ne)
        expected = 1.0
        #self.assertAlmostEqual(fab.y[0], expected, 3)
        np.testing.assert_array_almost_equal(fab.y[0], expected, 3)

    def test_ionisation_stage_distribution_hot(self):
        """Test that a very hot plasma will be almost entirely fully ionized.
        """
        Te = np.array([1e5])
        ne = np.array([1e19])
        fab = self.eq.ionisation_stage_distribution(Te, ne)
        expected = 1.0
        #self.assertAlmostEqual(fab.y[-1], expected, 3)
        np.testing.assert_array_almost_equal(fab.y[-1], expected, 3)

    def test_ionisation_stage_distribution_normalized(self):
        Te = np.array([1e1])
        ne = np.array([1e19])
        fab = self.eq.ionisation_stage_distribution(Te, ne)
        self.assertEqual(1.0, np.sum(fab.y))

    # four similar tests; could probably be combined somehow.
    # Maybe with http://feldboris.alwaysdata.net/blog/unittest-template.html
    # or with http://stackoverflow.com/questions/347109/how-do-i-concisely-implement-multiple-similar-unit-tests-in-the-python-unittest
    # but honestly I don't think it's worth the effort here.
    def test_ionisation_stage_distribution_one_point(self):
        """Test that it works with a 1x1 array."""
        Te = np.array([1e1])
        ne = np.array([1e19])
        stages = 1 + self.eq.nuclear_charge
        fab = self.eq.ionisation_stage_distribution(Te, ne)
        self.assertEqual((stages, 1), fab.y.shape)

    def test_ionisation_stage_distribution_Te_multiple(self):
        """Test with multiple temperatures and one density."""
        Te = np.array([1e0, 1e1, 1e2])
        ne = np.array([1e19])
        stages = 1 + self.eq.nuclear_charge
        fab = self.eq.ionisation_stage_distribution(Te, ne)
        self.assertEqual((stages, len(Te)), fab.y.shape)

    def test_ionisation_stage_distribution_ne_multiple(self):
        """Test that it works with multiple densities and one temperature."""
        Te = np.array([1e1])
        ne = np.array([1e19, 1e20, 1e21])
        stages = 1 + self.eq.nuclear_charge
        fab = self.eq.ionisation_stage_distribution(Te, ne)
        self.assertEqual((stages, len(ne)), fab.y.shape)

    def test_ionisation_stage_distribution_te_ne_multiple(self):
        """Test that it works with multiple temperatures and densities."""
        Te = np.array([1e1, 1e2, 1e3])
        ne = np.array([1e19, 1e20, 1e21])
        stages = 1 + self.eq.nuclear_charge
        fab = self.eq.ionisation_stage_distribution(Te, ne)
        self.assertEqual((stages, len(ne)), fab.y.shape)


if __name__ == '__main__':
    unittest.main()
