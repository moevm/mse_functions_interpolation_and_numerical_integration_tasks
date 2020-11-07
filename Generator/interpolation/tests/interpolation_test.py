from Generator.interpolation.Polynomial import Polynomial
import unittest


class TestSameData(unittest.TestCase):
    # test function to test equality of two value
    def test_negative(self):
        first_polynomial = Polynomial(3, 123)
        second_polynomial = Polynomial(3, 5)
        third_polynomial = Polynomial(3, 123)
        message = "First value and second value are not equal !"
        self.assertEqual(first_polynomial, third_polynomial, message)


if __name__ == '__main__':
    unittest.main()
