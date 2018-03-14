import unittest
import numpy as np
import atomic_neu as atomic

class TestFractionalAbundance(unittest.TestCase):
    def setUp(self):
        self.ad = atomic.element('Li')

    def test_mean_charge_zero(self):
        y = np.array([[1,0,0,0]]).T
        Te = np.array([1])
        ne = np.array([1])
        fab = atomic.abundance.FractionalAbundance(self.ad, y, Te, ne)
        assert fab.mean_charge() == 0

    def test_mean_charge_max(self):
        y = np.array([[0,0,0,1]]).T
        Te = np.array([1])
        ne = np.array([1])
        fab = atomic.abundance.FractionalAbundance(self.ad, y, Te, ne)
        assert fab.mean_charge() == 3

    def test_mean_charge_multiple(self):
        y = np.array([[1,0,0,0],[0,0,0,1]]).T
        Te = np.array([1])
        ne = np.array([1])
        fab = atomic.abundance.FractionalAbundance(self.ad, y, Te, ne)
        result = fab.mean_charge()
        expected = np.array([0,3])
        assert np.array_equal(result, expected)

    @unittest.skip("")
    def test_effective_charge(self):
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
