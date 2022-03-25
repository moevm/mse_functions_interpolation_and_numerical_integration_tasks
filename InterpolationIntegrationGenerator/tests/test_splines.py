import unittest
import numpy
from numpy.testing import assert_almost_equal
from InterpolationIntegrationGenerator.Spline.SplineTask import SplineTask


class TestSplines(unittest.TestCase):
    def test_same_seed_same_spline(self):
        spline_task1 = SplineTask(seed=100)
        spline_task2 = SplineTask(seed=100)

        self.assertEqual(spline_task1.x_values, spline_task2.x_values)
        self.assertEqual(spline_task1.y_values, spline_task2.y_values)
        assert_almost_equal(spline_task1.answer, spline_task2.answer)

    def test_center_x_is_in_range(self):
        spline_default_range = SplineTask()
        spline_custom_range = SplineTask(x_range=(-3, 1))

        self.assertTrue(-5 <= spline_default_range.x_values[1] <= 5)
        self.assertTrue(-3 <= spline_custom_range.x_values[1] <= 1)

    def test_y_is_in_range(self):
        spline_default_range = SplineTask()
        spline_custom_range = SplineTask(y_range=(-2.3, 2.5))

        self.assertTrue(all(-20 <= y <= 20 for y in spline_default_range.y_values))
        self.assertTrue(all(-2.3 <= y <= 2.5 for y in spline_custom_range.y_values))

    def test_step_is_correct(self):
        spline_default_step = SplineTask()
        spline_custom_step = SplineTask(step=2)

        self.assertTrue(all(
            spline_default_step.x_values[i] - spline_default_step.x_values[i - 1] == 1 for i in
            range(1, len(spline_default_step.x_values))))
        self.assertTrue(all(
            spline_custom_step.x_values[i] - spline_custom_step.x_values[i - 1] == 2 for i in
            range(1, len(spline_custom_step.x_values))))

    def test_middle_is_zero(self):
        spline_task = SplineTask(middle_is_zero=True)

        self.assertEqual(0, spline_task.x_values[1])

    def test_answer_is_correct(self):
        spline_task1 = SplineTask(None, x_values=[-4, 0, 4], y_values=[3.2, 1.7, 3.8])
        spline_task2 = SplineTask(None, x_values=[1, 2, 3], y_values=[1.8, 2.8, 8.7])
        spline_task3 = SplineTask(None, x_values=[-2, 0, 2], y_values=[1.2, 2.5, 0.3])
        spline_task4 = SplineTask(None, x_values=[-2, 1, 4], y_values=[2.8, 3.1, 1.2])
        spline_task5 = SplineTask(None, x_values=[-1, 0, 1], y_values=[5.1, 3.2, 6.7])
        spline_task6 = SplineTask(None, x_values=[5, 9, 13], y_values=[2.5, 3.8, 5.6])

        assert_almost_equal(numpy.array([1.7, -0.75, -0.09375, 1.7, -0.75, 0.31875]),
                            spline_task1.answer)
        assert_almost_equal(numpy.array([2.8, -2, 1, 14.4, -13.6, 3.9]),
                            spline_task2.answer)
        assert_almost_equal(numpy.array([2.5, 1.3, 0.325, 2.5, 1.3, -1.2]),
                            spline_task3.answer)
        assert_almost_equal(numpy.array([88 / 30, 4 / 30, 1 / 30, 236 / 90, 68 / 90, -25 / 90]),
                            spline_task4.answer)
        assert_almost_equal(numpy.array([3.2, -3.8, -1.9, 3.2, -3.8, 7.3]),
                            spline_task5.answer)
        assert_almost_equal(numpy.array([4.53125, -0.8125, 0.08125, -6.1, 1.55, -0.05]),
                            spline_task6.answer)
