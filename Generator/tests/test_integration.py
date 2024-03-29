from Generator.Tasks.IntegrationTask import TrapezoidTask, SimpsonTask, \
    trapezoid, simpson, createDocs, initDocs
import unittest


class Test(unittest.TestCase):
    def test_Trapezoid(self):
        task = TrapezoidTask().randomize(10)

        self.assertEqual(10, task.n)
        self.assertEqual(0, (task.yValues[0] + task.yValues[-1]) % 2)

    def test_Simpson(self):
        task = SimpsonTask().randomize(10)

        self.assertEqual(10, task.n)
        self.assertEqual(0, (task.yValues[0] + task.yValues[-1]) % 2)

    def test_trapezoid(self):
        self.assertEqual(0.8, trapezoid([0, 1, 2, 3, 4], 0.1))
        self.assertEqual(1, trapezoid([0, 10, -10, 5, 10], 0.1))

    def test_simpson(self):
        self.assertEqual(4.8, simpson([0, 1, 2, 3, 4], 0.6))
        self.assertEqual(10, simpson([0, 10, -10, 5, 10], 0.6))

    def test_incorrectDotsCnt(self):
        taskT = TrapezoidTask().randomize("hello")
        taskT2 = TrapezoidTask().randomize(2.8)

        taskS = SimpsonTask().randomize("hello")
        taskS2 = SimpsonTask().randomize(2.8)

        self.assertIsNone(taskT)
        self.assertIsNone(taskT2)
        self.assertIsNone(taskS)
        self.assertIsNone(taskS2)

    def test_sameSeeds(self):
        taskT = TrapezoidTask(3).randomize(10)
        taskT2 = TrapezoidTask(3).randomize(10)

        taskS = SimpsonTask(15).randomize(15)
        taskS2 = SimpsonTask(15).randomize(15)

        self.assertEqual(taskS.xValues, taskS2.xValues)
        self.assertEqual(taskS.yValues, taskS2.yValues)
        self.assertEqual(taskT.xValues, taskT2.xValues)
        self.assertEqual(taskT.yValues, taskT2.yValues)

    def test_notSameSeeds(self):
        taskT = TrapezoidTask(3).randomize(10)
        taskT2 = TrapezoidTask(4).randomize(10)

        taskS = SimpsonTask(15).randomize(15)
        taskS2 = SimpsonTask(16).randomize(15)

        self.assertNotEqual(taskS.xValues, taskS2.xValues)
        self.assertNotEqual(taskS.yValues, taskS2.yValues)
        self.assertNotEqual(taskT.xValues, taskT2.xValues)
        self.assertNotEqual(taskT.yValues, taskT2.yValues)

    def docs_with_same_seed_are_same(self):
        answerDoc1, taskDoc1 = initDocs()
        createDocs(answerDoc1, taskDoc1, 30, 11, 9, None, seed=100)
        answerDoc2, taskDoc2 = initDocs()
        createDocs(answerDoc2, taskDoc2, 30, 11, 9, None, seed=100)
        answerDoc3, taskDoc3 = initDocs()
        createDocs(answerDoc3, taskDoc3, 30, 11, 9, None, seed=200)

        self.assertEqual(taskDoc1, taskDoc2)
        self.assertEqual(answerDoc1, answerDoc2)
        self.assertNotEqual(taskDoc1, taskDoc3)
        self.assertNotEqual(answerDoc1, answerDoc3)


if __name__ == '__main__':
    unittest.main()
