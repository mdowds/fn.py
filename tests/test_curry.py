import unittest

from fn.func import curried


class Curriedtest(unittest.TestCase):

    def test_curried_wrapper(self):

        @curried
        def _child(a, b, c, d):
            return a + b + c + d

        @curried
        def _moma(a, b):
            return _child(a, b)

        def _assert_instance(expected, acutal):
            self.assertEqual(expected.__module__, acutal.__module__)
            self.assertEqual(expected.__name__, acutal.__name__)

        res1 = _moma(1)
        _assert_instance(_moma, res1)
        res2 = res1(2)
        _assert_instance(_child, res2)
        res3 = res2(3)
        _assert_instance(_child, res3)
        res4 = res3(4)

        self.assertEqual(res4, 10)
