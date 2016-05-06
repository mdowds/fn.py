import unittest

from fn import Stream, iters


class StreamTestCase(unittest.TestCase):

    def test_from_list(self):
        s = Stream() << [1, 2, 3, 4, 5]
        self.assertEqual([1, 2, 3, 4, 5], list(s))
        self.assertEqual(2, s[1])
        self.assertEqual([1, 2], list(s[0:2]))

    def test_from_iterator(self):
        s = Stream() << range(6) << [6, 7]
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7], list(s))

    def test_from_generator(self):
        def gen():
            yield 1
            yield 2
            yield 3

        s = Stream() << gen << (4, 5)
        assert list(s) == [1, 2, 3, 4, 5]

    def test_lazy_slicing(self):
        s = Stream() << iters.range(10)
        self.assertEqual(s.cursor(), 0)

        s_slice = s[:5]
        self.assertEqual(s.cursor(), 0)
        self.assertEqual(len(list(s_slice)), 5)

    def test_lazy_slicing_recursive(self):
        s = Stream() << iters.range(10)
        sf = s[1:3][0:2]

        self.assertEqual(s.cursor(), 0)
        self.assertEqual(len(list(sf)), 2)

    def test_fib_infinite_stream(self):
        from operator import add

        f = Stream()
        fib = f << [0, 1] << iters.map(add, f, iters.drop(1, f))

        self.assertEqual(
            [0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
            list(iters.take(10, fib))
        )
        self.assertEqual(6765, fib[20])
        self.assertEqual(
            [832040, 1346269, 2178309, 3524578, 5702887],
            list(fib[30:35])
        )
        # 35 elements should be already evaluated
        self.assertEqual(fib.cursor(), 35)

    def test_origin_param(self):
        self.assertEqual([100], list(Stream(100)))
        self.assertEqual([1, 2, 3], list(Stream(1, 2, 3)))
        self.assertEqual(
            [1, 2, 3, 10, 20, 30],
            list(Stream(1, 2, 3) << [10, 20, 30])
        )

    def test_origin_param_string(self):
        self.assertEqual(["stream"], list(Stream("stream")))
