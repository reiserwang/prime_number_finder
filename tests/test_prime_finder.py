import unittest
import sys
import os

# Add parent directory to path so we can import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import prime_number_finder_pool_map as finder

class TestPrimeFinder(unittest.TestCase):
    def test_is_prime(self):
        # Known primes
        self.assertTrue(finder.is_prime(2))
        self.assertTrue(finder.is_prime(3))
        self.assertTrue(finder.is_prime(5))
        self.assertTrue(finder.is_prime(7))
        self.assertTrue(finder.is_prime(11))
        self.assertTrue(finder.is_prime(13))
        self.assertTrue(finder.is_prime(17))
        self.assertTrue(finder.is_prime(19))
        self.assertTrue(finder.is_prime(29))
        self.assertTrue(finder.is_prime(31))

        # Known non-primes
        self.assertFalse(finder.is_prime(1))
        self.assertFalse(finder.is_prime(4))
        self.assertFalse(finder.is_prime(6))
        self.assertFalse(finder.is_prime(9))
        self.assertFalse(finder.is_prime(15))
        self.assertFalse(finder.is_prime(25))
        self.assertFalse(finder.is_prime(49))

    def test_find_primes(self):
        if hasattr(finder, 'find_primes'):
            # Test up to 20
            primes = finder.find_primes(20, 1)
            expected = [2, 3, 5, 7, 11, 13, 17, 19]
            self.assertEqual(primes, expected)

            # Test up to 10
            primes = finder.find_primes(10, 2)
            expected = [2, 3, 5, 7]
            self.assertEqual(primes, expected)
        else:
            print("find_primes not implemented yet")

if __name__ == '__main__':
    unittest.main()
