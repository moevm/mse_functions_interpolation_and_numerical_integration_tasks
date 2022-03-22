from InterpolationIntegrationGenerator.interpolation.PolynomialHelper import PolynomialHelper
from InterpolationIntegrationGenerator.interpolation.Tasks import Tasks
import unittest


class Test(unittest.TestCase):
    def test_equals_with_same_seeds(self):
        polynomial_1 = PolynomialHelper.generatePolynomial(3, 123)
        polynomial_2 = PolynomialHelper.generatePolynomial(3, 5)
        polynomial_3 = PolynomialHelper.generatePolynomial(3, 123)
        polynomial_4 = PolynomialHelper.generatePolynomial(3, 5)

        message = "First value and second value are not equal!"
        self.assertEqual(polynomial_1, polynomial_3, message)
        self.assertEqual(polynomial_2, polynomial_4)

    def test_not_equals_with_different_seeds(self):
        polynomial_1 = PolynomialHelper.generatePolynomial(3, 123)
        polynomial_2 = PolynomialHelper.generatePolynomial(3, 5)
        polynomial_3 = PolynomialHelper.generatePolynomial(4, 143)
        polynomial_4 = PolynomialHelper.generatePolynomial(4, 342)

        message = "First value and second value are equal!"
        self.assertNotEqual(polynomial_1, polynomial_2, message)
        self.assertNotEqual(polynomial_3, polynomial_4, message)

    def test_none_polynomial(self):
        polynomial_1 = PolynomialHelper.generatePolynomial(-1, 23)
        polynomial_2 = PolynomialHelper.generatePolynomial(-1.3, 23)
        polynomial_3 = PolynomialHelper.generatePolynomial(-1.3, "fasd")
        polynomial_4 = PolynomialHelper.generatePolynomial(3, 2.34)
        polynomial_5 = PolynomialHelper.generatePolynomial(5, -42134)

        message = "Object in not none!"
        self.assertIsNone(polynomial_1, message)
        self.assertIsNone(polynomial_2, message)
        self.assertIsNone(polynomial_3, message)
        self.assertIsNone(polynomial_4, message)
        self.assertIsNone(polynomial_5, message)

    def test_not_none_polynomial(self):
        polynomial_1 = PolynomialHelper.generatePolynomial(3, 234)
        polynomial_2 = PolynomialHelper.generatePolynomial(4, 0)
        polynomial_3 = PolynomialHelper.generatePolynomial(5, 2**32-1)
        polynomial_4 = PolynomialHelper.generatePolynomial(6, 7543)

        self.assertIsNotNone(polynomial_1, message)
        self.assertIsNotNone(polynomial_2, message)
        self.assertIsNotNone(polynomial_3, message)
        self.assertIsNotNone(polynomial_4, message)

    def docs_with_same_seed_are_same(self):
        answerDoc, taskDoc = initDocs()
        createDocs(answerDoc, taskDoc, taskCnt, trapezoidTasks, simpsonTasks, surnames, seed)

        message_1 = "Same seeds generates different docs!"
        message_2 = "Different seeds generates same docs!"
        self.assertEqual(docs_1.tasks, docs_2.tasks, message_1)
        self.assertEqual(docs_1.answers, docs_2.answers, message_1)
        self.assertNotEqual(docs_1.tasks, docs_3.tasks, message_2)
        self.assertNotEqual(docs_1.answers, docs_3.answers, message_2)


if __name__ == '__main__':
    unittest.main()
