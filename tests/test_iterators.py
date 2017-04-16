import operator
import unittest

from fn import _, iters


class IteratorsTestCase(unittest.TestCase):

    def test_take(self):
        self.assertEqual([0, 1], list(iters.take(2, range(10))))
        self.assertEqual([0, 1], list(iters.take(10, range(2))))

    def test_drop(self):
        self.assertEqual([3, 4], list(iters.drop(3, range(5))))
        self.assertEqual([], list(iters.drop(10, range(2))))

    def test_first_true(self):
        pred = _ == 5
        self.assertEqual(5, iters.first_true(range(1, 10), pred=pred))
        self.assertEqual(
            999, iters.first_true(range(6, 10), default=999, pred=pred)
        )

    def test_takelast(self):
        self.assertEqual([8, 9], list(iters.takelast(2, range(10))))
        self.assertEqual([0, 1], list(iters.takelast(10, range(2))))

    def test_droplast(self):
        self.assertEqual([0, 1], list(iters.droplast(3, range(5))))
        self.assertEqual([], list(iters.droplast(10, range(2))))

    def test_consume(self):
        # full consuming, without limitation
        r = iters.range(10)
        self.assertEqual(10, len(list(r)))
        itr = iter(r)
        iters.consume(itr)
        self.assertEqual(0, len(list(itr)))

    def test_consume_limited(self):
        r = iters.range(10)
        self.assertEqual(10, len(list(r)))
        itr = iter(r)
        iters.consume(itr, 5)
        self.assertEqual(5, len(list(itr)))

    def test_nth(self):
        self.assertEqual(1, iters.nth(range(5), 1))
        self.assertEqual(None, iters.nth(range(5), 10))
        self.assertEqual("X", iters.nth(range(5), 10, "X"))

    def test_head(self):
        self.assertEqual(0, iters.head([0, 1, 2]))
        self.assertEqual(None, iters.head([]))

        def gen():
            yield 1
            yield 2
            yield 3

        self.assertEqual(1, iters.head(gen()))

    def test_first(self):
        self.assertEqual(iters.first, iters.head)  # Check if same object

    def test_tail(self):
        self.assertEqual([1, 2], list(iters.tail([0, 1, 2])))
        self.assertEqual([], list(iters.tail([])))

        def gen():
            yield 1
            yield 2
            yield 3

        self.assertEqual([2, 3], list(iters.tail(gen())))

    def test_rest(self):
        self.assertEqual(iters.rest, iters.tail)  # Check if same object

    def test_second(self):
        self.assertEqual(2, iters.second([1, 2, 3]))
        self.assertEqual(None, iters.second([]))

        def gen():
            yield 10
            yield 20
            yield 30

        self.assertEqual(20, iters.second(gen()))

    def test_ffirst(self):
        self.assertEqual(1, iters.ffirst([[1, 2], [3, 4]]))
        self.assertEqual(None, iters.ffirst([[], [10, 20]]))

        def gen():
            yield (x * 10 for x in (10, 20, 30,))

        self.assertEqual(100, iters.ffirst(gen()))

    def test_compact(self):
        self.assertEqual([True, 1, 0.1, "non-empty", [""], (0,), {"a": 1}],
                         list(iters.compact([None, False, True, 0, 1, 0.0, 0.1,
                                             "", "non-empty", [], [""],
                                             (), (0,), {}, {"a": 1}])))

    def test_every(self):
        self.assertEqual(True, iters.every(_ % 2 == 0, [2, 4, 6]))
        self.assertEqual(False, iters.every(_ % 2 == 0, [1, 3, 5]))
        self.assertEqual(False, iters.every(_ % 2 == 0, [2, 4, 6, 7]))

    def test_some(self):
        self.assertEqual("one",
                         iters.some(lambda k: {1: "one", 2: "two"}.get(k, ""),
                                    [1, 2]))
        self.assertEqual(None,
                         iters.some(lambda k: {1: "one", 2: "two"}.get(k, ""),
                                    [4, 3]))
        self.assertEqual("two",
                         iters.some(lambda k: {1: "one", 2: "two"}.get(k, ""),
                                    [4, 3, 2]))

    def test_reject(self):
        self.assertEqual(
            [1, 3, 5, 7, 9],
            list(iters.reject(_ % 2 == 0, range(1, 11)))
        )
        self.assertEqual(
            [None, False, 0, 0.0, "", [], (), {}],
            list(
                iters.reject(
                    None, [
                        None, False, True, 0, 1, 0.0, 0.1, "", "non-empty",
                        [], [""], (), (0,), {}, {"a": 1}
                    ])
            )
        )

    def test_iterate(self):
        it = iters.iterate(lambda x: x * x, 2)
        self.assertEqual(2, next(it))  # 2
        self.assertEqual(4, next(it))  # 2 * 2
        self.assertEqual(16, next(it))  # 4 * 4
        self.assertEqual(256, next(it))  # 16 * 16

    def test_padnone(self):
        it = iters.padnone([10, 11])
        self.assertEqual(10, next(it))
        self.assertEqual(11, next(it))
        self.assertEqual(None, next(it))
        self.assertEqual(None, next(it))

    def test_ncycles(self):
        it = iters.ncycles([10, 11], 2)
        self.assertEqual(10, next(it))
        self.assertEqual(11, next(it))
        self.assertEqual(10, next(it))
        self.assertEqual(11, next(it))
        self.assertRaises(StopIteration, next, it)

    def test_repeatfunc(self):
        def f():
            return "test"

        # unlimited count
        it = iters.repeatfunc(f)
        self.assertEqual("test", next(it))
        self.assertEqual("test", next(it))
        self.assertEqual("test", next(it))

        # limited
        it = iters.repeatfunc(f, 2)
        self.assertEqual("test", next(it))
        self.assertEqual("test", next(it))
        self.assertRaises(StopIteration, next, it)

    def test_grouper(self):
        # without fill value (default should be None)
        a, b, c = iters.grouper(3, "ABCDEFG")
        self.assertEqual(["A", "B", "C"], list(a))
        self.assertEqual(["D", "E", "F"], list(b))
        self.assertEqual(["G", None, None], list(c))

        # with fill value
        a, b, c = iters.grouper(3, "ABCDEFG", "x")
        self.assertEqual(["A", "B", "C"], list(a))
        self.assertEqual(["D", "E", "F"], list(b))
        self.assertEqual(["G", "x", "x"], list(c))

    def test_group_by(self):
        # verify grouping logic
        grouped = iters.group_by(len, ['1', '12', 'a', '123', 'ab'])
        self.assertEqual({1: ['1', 'a'], 2: ['12', 'ab'], 3: ['123']}, grouped)

        # verify it works with any iterable - not only lists
        def gen():
            yield '1'
            yield '12'

        grouped = iters.group_by(len, gen())
        self.assertEqual({1: ['1'], 2: ['12']}, grouped)

    def test_roundrobin(self):
        r = iters.roundrobin('ABC', 'D', 'EF')
        self.assertEqual(["A", "D", "E", "B", "F", "C"], list(r))

    def test_partition(self):
        def is_odd(x):
            return x % 2 == 1

        before, after = iters.partition(is_odd, iters.range(5))
        self.assertEqual([0, 2, 4], list(before))
        self.assertEqual([1, 3], list(after))

    def test_splitat(self):
        before, after = iters.splitat(2, iters.range(5))
        self.assertEqual([0, 1], list(before))
        self.assertEqual([2, 3, 4], list(after))

    def test_splitby(self):
        def is_even(x):
            return x % 2 == 0

        before, after = iters.splitby(is_even, iters.range(5))
        self.assertEqual([0], list(before))
        self.assertEqual([1, 2, 3, 4], list(after))

    def test_powerset(self):
        ps = iters.powerset([1, 2])
        self.assertEqual([tuple(), (1,), (2,), (1, 2)], list(ps))

    def test_pairwise(self):
        ps = iters.pairwise([1, 2, 3, 4])
        self.assertEqual([(1, 2), (2, 3), (3, 4)], list(ps))

    def test_iter_except(self):
        d = ["a", "b", "c"]
        it = iters.iter_except(d.pop, IndexError)
        self.assertEqual(["c", "b", "a"], list(it))

    def test_flatten(self):
        # flatten nested lists
        self.assertEqual([1, 2, 3, 4], list(iters.flatten([[1, 2], [3, 4]])))
        self.assertEqual(
            [1, 2, 3, 4, 5, 6],
            list(iters.flatten([[1, 2], [3, [4, 5, 6]]]))
        )
        # flatten nested tuples, sets, and frozen sets
        self.assertEqual(
            [1, 2, 3, 4, 5, 6],
            list(iters.flatten(((1, 2), (3, (4, 5, 6)))))
        )
        self.assertEqual(
            [1, 2, 3],
            list(iters.flatten(set([1, frozenset([2, 3])])))
        )
        # flatten nested generators
        generators = ((num + 1 for num in range(0, n)) for n in range(1, 4))
        self.assertEqual([1, 1, 2, 1, 2, 3], list(iters.flatten(generators)))
        # flat list should return itself
        self.assertEqual([1, 2, 3], list(iters.flatten([1, 2, 3])))
        # Don't flatten strings/unicode, bytes, or bytearrays
        self.assertEqual([2, "abc", 1], list(iters.flatten([2, "abc", 1])))
        self.assertEqual([2, b'abc', 1], list(iters.flatten([2, b'abc', 1])))
        self.assertEqual([2, bytearray(b'abc'), 1],
                         list(iters.flatten([2, bytearray(b'abc'), 1])))
        self.assertEqual(
            [bytearray(b'abc'), b'\xd1\x8f'.decode('utf8'), b'y'],
            list(iters.flatten(
                [bytearray(b'abc'), b'\xd1\x8f'.decode('utf8'), b'y']
            )))

    def test_accumulate(self):
        self.assertEqual(
            [1, 3, 6, 10, 15],
            list(iters.accumulate([1, 2, 3, 4, 5]))
        )
        self.assertEqual(
            [1, 2, 6, 24, 120],
            list(iters.accumulate([1, 2, 3, 4, 5], operator.mul))
        )

    def test_filterfalse(self):
        filtered = iters.filterfalse(lambda x: x > 10, [1, 2, 3, 11, 12])
        self.assertEqual([1, 2, 3], list(filtered))
