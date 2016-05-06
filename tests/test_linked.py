import unittest

from fn.immutable import LinkedList, Stack


class LinkedListsTestCase(unittest.TestCase):

    def test_linked_list_basic_operations(self):
        l1 = LinkedList()
        l2 = l1.cons(1)
        l3 = l2.cons(2)
        self.assertEqual(None, l1.head)
        self.assertEqual(1, l2.head)
        self.assertEqual(2, l3.head)
        self.assertEqual(1, l3.tail.head)
        self.assertEqual(None, l3.tail.tail.head)

    def test_linked_list_num_of_elements(self):
        self.assertEqual(0, len(LinkedList()))
        self.assertEqual(3, len(LinkedList().cons(10).cons(20).cons(30)))

    def tests_linked_list_iterator(self):
        self.assertEqual(
            [30, 20, 10],
            list(LinkedList().cons(10).cons(20).cons(30))
        )

    def test_from_iterable(self):
        expected = [10, 20, 30]
        actual = list(LinkedList.from_iterable(expected))
        self.assertEqual(actual, expected)

        actual = LinkedList.from_iterable(tuple(expected))
        self.assertEqual(list(actual), expected)

        actual = LinkedList.from_iterable(iter(expected))
        self.assertEqual(list(actual), expected)

        actual = LinkedList.from_iterable(
            LinkedList().cons(30).cons(20).cons(10)
        )
        self.assertEqual(list(actual), expected)

    def test_stack_push_pop_ordering(self):
        s1 = Stack()
        s2 = s1.push(1)
        s3 = s2.push(10)
        s4 = s3.push(100)
        (sv4, s5) = s4.pop()
        (sv3, s6) = s5.pop()
        self.assertEqual(100, sv4)
        self.assertEqual(10, sv3)
        self.assertEqual(100, s4.pop()[0])

    def test_stack_length(self):
        self.assertEqual(0, len(Stack()))
        self.assertEqual(3, len(Stack().push(1).push(2).push(3)))

    def test_stack_is_empty_check(self):
        self.assertTrue(Stack().push(100))
        self.assertFalse(Stack().push(100).is_empty())
        self.assertTrue(Stack().is_empty())

    def test_pop_empty_stack_exception(self):
        self.assertRaises(ValueError, Stack().pop)

    def test_stack_iterator(self):
        self.assertEqual([10, 5, 1], list(Stack().push(1).push(5).push(10)))
        self.assertEqual(6, sum(Stack().push(1).push(2).push(3)))
