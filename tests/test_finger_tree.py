import unittest

from fn.immutable import Deque


class FingerTreeDequeTestCase(unittest.TestCase):

    def test_deque_basic_operations(self):
        d1 = Deque()
        d2 = d1.push_back(1)
        d3 = d2.push_back(2)
        d4 = d3.push_back(3)
        d5 = d4.push_front(10)
        d6 = d5.push_front(20)
        self.assertEqual(1, d4.head())
        self.assertEqual(3, d4.last())
        self.assertEqual(20, d6.head())
        self.assertEqual(3, d6.last())

    # FIXME: write this test.
    def test_deque_num_of_elements(self):
        pass

    def test_deque_is_empty(self):
        self.assertTrue(Deque().is_empty())
        self.assertFalse(Deque().push_back(1).is_empty())
        self.assertTrue(Deque().push_back(1).tail().is_empty())

    def test_iterator(self):
        self.assertEqual([], list(Deque()))
        self.assertEqual(
            [1, 2, 3],
            list(Deque().push_back(1).push_back(2).push_back(3))
        )
        self.assertEqual(
            60,
            sum(Deque().push_back(10).push_front(20).push_back(30))
        )
        self.assertEqual(
            sum(range(1, 20)),
            sum(Deque.from_iterable(range(1, 20)))
        )


if __name__ == '__main__':
    unittest.main()
