import operator
import sys
import unittest

from fn import recur


class TrampolineTestCase(unittest.TestCase):

    def test_tco_decorator(self):

        def recur_accumulate(origin, f=operator.add, acc=0):
            n = next(origin, None)
            if n is None:
                return acc
            return recur_accumulate(origin, f, f(acc, n))

        # this works normally
        self.assertEqual(10, recur_accumulate(iter(range(5))))

        limit = sys.getrecursionlimit() * 10
        # such count of recursive calls should fail on CPython,
        # for PyPy we skip this test cause on PyPy the limit is
        # approximative and checked at a lower level
        if not hasattr(sys, 'pypy_version_info'):
            self.assertRaises(
                RuntimeError, recur_accumulate, iter(range(limit))
            )

        # with recur decorator it should run without problems
        @recur.tco
        def tco_accumulate(origin, f=operator.add, acc=0):
            n = next(origin, None)
            if n is None:
                return False, acc
            return True, (origin, f, f(acc, n))

        self.assertEqual(sum(range(limit)), tco_accumulate(iter(range(limit))))

    def test_tco_different_functions(self):

        @recur.tco
        def recur_inc2(curr, acc=0):
            if curr == 0:
                return False, acc
            return recur_dec, (curr-1, acc+2)

        @recur.tco
        def recur_dec(curr, acc=0):
            if curr == 0:
                return False, acc
            return recur_inc2, (curr-1, acc-1)

        self.assertEqual(5000, recur_inc2(10000))
