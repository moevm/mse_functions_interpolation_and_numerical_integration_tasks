from Generator.integration.main import TrapezoidTask
from Generator.integration.main import SimpsonTask
from Generator.integration.main import trapezoid
from Generator.integration.main import simpson
import unittest


class Test(unittest.TestCase):
    def test_Trapezoid(self):
        task = TrapezoidTask().randomize(10)

        message = "First value and second value are not equal!"
        self.assertEqual(10, task.n, message)
        self.assertEqual(0, (task.yValues[0] + task.yValues[-1]) % 2)

    def test_Simpson(self):
        task = SimpsonTask().randomize(10)

        message = "First value and second value are not equal!"
        self.assertEqual(10, task.n, message)
        self.assertEqual(0, (task.yValues[0] + task.yValues[-1]) % 2)

    def test_trapezoid(self):
        message = "First value and second value are not equal!"
        self.assertEqual(0.8, trapezoid([0, 1, 2, 3, 4], 0.1), message)
        self.assertEqual(1, trapezoid([0, 10, -10, 5, 10], 0.1))

    def test_simpson(self):
        message = "First value and second value are not equal!"
        self.assertEqual(4.8, simpson([0, 1, 2, 3, 4], 0.6), message)
        self.assertEqual(10, simpson([0, 10, -10, 5, 10], 0.6))


if __name__ == '__main__':
    unittest.main()
