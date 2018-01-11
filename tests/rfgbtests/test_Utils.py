import sys
import unittest

sys.path.append('./src/')
from Utils import Utils

class UtilsTest(unittest.TestCase):

    def test_sigmoid(self):
        self.assertEqual(Utils.sigmoid(-5), 0.006692850924284856)
        self.assertEqual(Utils.sigmoid(-0.001), 0.49975000002083336)
        self.assertEqual(Utils.sigmoid(0), 0.5)
        self.assertEqual(Utils.sigmoid(0.0001), 0.5000249999999792)
        self.assertEqual(Utils.sigmoid(0.01), 0.5024999791668749)
        self.assertEqual(Utils.sigmoid(0.5), 0.6224593312018546)
        self.assertEqual(Utils.sigmoid(1), 0.7310585786300049)
        self.assertEqual(Utils.sigmoid(5), 0.9933071490757152)

if __name__ == '__main__':
    unittest.main()
