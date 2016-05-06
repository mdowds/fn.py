import itertools
import operator
import unittest

from fn import F, _, iters, op


class OperatorTestCase(unittest.TestCase):

    def test_currying(self):
        def add(first):
            def add(second):
                return first + second
            return add

        self.assertEqual(1, op.curry(add, 0, 1))

    def test_apply(self):
        self.assertEqual(10, op.apply(operator.add, [2, 8]))

    def test_flip(self):
        self.assertEqual(10, op.flip(operator.sub)(2, 12))
        self.assertEqual(-10, op.flip(op.flip(operator.sub))(2, 12))
        # flipping of flipped function should use optimization
        self.assertTrue(operator.sub is op.flip(op.flip(operator.sub)))

    def test_flip_with_shortcut(self):
        self.assertEqual(10, op.flip(_ - _)(2, 12))

    def test_zipwith(self):
        zipper = op.zipwith(operator.add)
        self.assertEqual(
            [10, 11, 12], list(zipper([0, 1, 2], itertools.repeat(10)))
        )

        zipper = op.zipwith(_ + _)
        self.assertEqual(
            [10, 11, 12], list(zipper([0, 1, 2], itertools.repeat(10)))
        )

        zipper = F() << list << op.zipwith(_ + _)
        self.assertEqual(
            [10, 11, 12], zipper([0, 1, 2], itertools.repeat(10))
        )

    def test_foldl(self):
        self.assertEqual(10, op.foldl(operator.add)([0, 1, 2, 3, 4]))
        self.assertEqual(20, op.foldl(operator.add, 10)([0, 1, 2, 3, 4]))
        self.assertEqual(20, op.foldl(operator.add, 10)(iters.range(5)))
        self.assertEqual(10, op.foldl(_ + _)(range(5)))

    def test_foldr(self):
        summer = op.foldr(operator.add)
        self.assertEqual(10, summer([0, 1, 2, 3, 4]))
        self.assertEqual(20, op.foldr(operator.add, 10)([0, 1, 2, 3, 4]))
        self.assertEqual(20, op.foldr(operator.add, 10)(iters.range(5)))
        # specific case for right-side folding
        self.assertEqual(
            100,
            op.foldr(op.call, 0)([lambda s: s**2, lambda k: k+10])
        )

    def test_unfold_infinite(self):
        doubler = op.unfold(lambda x: (x*2, x*2))
        self.assertEqual(20, next(doubler(10)))
        self.assertEqual(
            [20, 40, 80, 160, 320], list(iters.take(5, doubler(10)))
        )

    def test_unfold_finite(self):
        countdown = op.unfold(lambda x: (x-1, x-2) if x > 1 else None)
        self.assertEqual([9, 7, 5, 3, 1], list(countdown(10)))
