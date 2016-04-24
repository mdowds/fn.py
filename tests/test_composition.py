import operator
import unittest

from fn import F, _, iters


class CompositionTestCase(unittest.TestCase):

    def test_composition(self):
        def f(x):
            return x * 2

        def g(x):
            return x + 10

        self.assertEqual(30, (F(f) << g)(5))

        def z(x):
            return x * 20
        self.assertEqual(220, (F(f) << F(g) << F(z))(5))

    def test_partial(self):
        # Partial should work if we pass additional arguments to F constructor
        f = F(operator.add, 10) << F(operator.add, 5)
        self.assertEqual(25, f(10))

    def test_underscore(self):
        self.assertEqual(
            [1, 4, 9],
            list(map(F() << (_ ** 2) << _ + 1, range(3)))
        )

    def test_pipe_composition(self):
        def f(x):
            return x * 2

        def g(x):
            return x + 10

        self.assertEqual(20, (F() >> f >> g)(5))

    def test_pipe_partial(self):
        func = F() >> (iters.filter, _ < 6) >> sum
        self.assertEqual(15, func(iters.range(10)))
