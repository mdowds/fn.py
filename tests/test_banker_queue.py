import unittest

from fn.immutable import Queue


class BankerQueueTestCase(unittest.TestCase):

    def test_queue_basic_operations(self):
        q1 = Queue()
        q2 = q1.enqueue(1)
        q3 = q2.enqueue(10)
        q4 = q3.enqueue(100)
        self.assertEqual(1, q4.dequeue()[0])
        self.assertEqual(1, q3.dequeue()[0])
        self.assertEqual(1, q2.dequeue()[0])
        v1, q5 = q4.dequeue()
        v2, q6 = q5.dequeue()
        v3, q7 = q6.dequeue()
        self.assertEqual(1, v1)
        self.assertEqual(10, v2)
        self.assertEqual(100, v3)
        self.assertEqual(0, len(q7))

    def test_queue_num_of_elements(self):
        self.assertEqual(0, len(Queue()))
        self.assertEqual(3, len(Queue().enqueue(1).enqueue(2).enqueue(3)))

    def test_queue_is_empty(self):
        self.assertTrue(Queue().is_empty())
        self.assertFalse(Queue().enqueue(1).is_empty())
        self.assertTrue(Queue().enqueue(1).dequeue()[1].is_empty())

    def test_dequeue_from_empty(self):
        self.assertRaises(ValueError, Queue().dequeue)

    def test_iterator(self):
        self.assertEqual([], list(Queue()))
        self.assertEqual(
            [1, 2, 3],
            list(Queue().enqueue(1).enqueue(2).enqueue(3))
        )
        self.assertEqual(60, sum(Queue().enqueue(10).enqueue(20).enqueue(30)))
