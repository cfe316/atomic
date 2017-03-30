import unittest
import atomic

class TestAdf11(unittest.TestCase):
    def setUp(self):
        data = atomic.atomic_data._element_data('Li')
        self.ionis = atomic.atomic_data._full_path(data['ionisation'])

    def test___init__not_found_error(self):
        with self.assertRaises(IOError):
            atomic.adf11.Adf11('/asdf')

    def test_read(self):
        adf11 = atomic.adf11.Adf11(self.ionis)
        ret = adf11.read()
        self.assertEqual(3, ret['charge'])
        self.assertEqual(16, len(ret['log_density']))
        min_log_dens = 14
        max_log_dens = 21
        self.assertEqual(min_log_dens, ret['log_density'][0])
        self.assertEqual(max_log_dens, ret['log_density'][-2])

        self.assertEqual(3, ret['number_of_charge_states'])
        self.assertEqual((3,25,16), ret['log_coeff'].shape)

        # check that the instance variables come out correctly
        self.assertEqual('scd', adf11.class_)
        self.assertEqual('li', adf11.element.lower())
        self.assertEqual(self.ionis, adf11.name)

class TestSniffer(unittest.TestCase):
    @unittest.skip("")
    def test___init__(self):
        # sniffer = Sniffer(file_)
        assert False # TODO: implement your test here

if __name__ == '__main__':
    unittest.main()
