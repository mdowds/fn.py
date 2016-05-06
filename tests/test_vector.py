import unittest

from fn.immutable import Vector
from fn.uniform import reduce


class VectorTestCase(unittest.TestCase):

    def test_cons_operation(self):
        v = Vector()
        self.assertEqual(0, len(v))
        v1 = v.cons(10)
        self.assertEqual(1, len(v1))
        self.assertEqual(0, len(v))  # previous value didn't change
        up = reduce(lambda acc, el: acc.cons(el), range(513), Vector())
        self.assertEqual(513, len(up))

    def test_assoc_get_operations(self):
        v = Vector()
        v1 = v.assoc(0, 10)
        v2 = v1.assoc(1, 20)
        v3 = v2.assoc(2, 30)
        self.assertEqual(10, v3.get(0))
        self.assertEqual(20, v3.get(1))
        self.assertEqual(30, v3.get(2))
        # check persistence
        v4 = v2.assoc(2, 50)
        self.assertEqual(30, v3.get(2))
        self.assertEqual(50, v4.get(2))
        # long vector
        up = reduce(lambda acc, el: acc.assoc(el, el*2), range(1500), Vector())
        self.assertEqual(2800, up.get(1400))
        self.assertEqual(2998, up.get(1499))

    def test_pop_operations(self):
        v = reduce(lambda acc, el: acc.cons(el), range(2000), Vector())
        self.assertEqual(1999, len(v.pop()))
        self.assertEqual(list(range(1999)), list(v.pop()))

    def test_vector_iterator(self):
        v = reduce(lambda acc, el: acc.assoc(el, el+1), range(1500), Vector())
        self.assertEqual(list(range(1, 1501)), list(v))
        self.assertEqual(1125750, sum(v))

    def test_index_error(self):
        v = reduce(lambda acc, el: acc.assoc(el, el+2), range(50), Vector())
        self.assertRaises(IndexError, v.get, -1)
        self.assertRaises(IndexError, v.get, 50)
        self.assertRaises(IndexError, v.get, 52)

    def test_setitem_should_not_be_implemented(self):
        def f():
            v = Vector().cons(20)
            v[0] = 10
        self.assertRaises(NotImplementedError, f)

    # FIXME: Write this test.
    def test_subvector_operation(self):
        pass
