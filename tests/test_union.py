import unittest

from fn.immutable import PairingHeap, SkewHeap


class UnionBasedHeapsTestCase(unittest.TestCase):

    def _heap_basic_operations(self, cls):
        # Create new heap with 3 elements
        s1 = cls(10)
        s2 = s1.insert(30)
        s3 = s2.insert(20)

        # Extract elements one-by-one
        el1, sx1 = s3.extract()
        el2, sx2 = sx1.extract()
        el3, sx3 = sx2.extract()

        # Check elements ordering
        self.assertEqual(10, el1)
        self.assertEqual(20, el2)
        self.assertEqual(30, el3)

        # Check that previous heap are persistent
        el22, _ = sx1.extract()
        self.assertEqual(20, el22)

    def _heap_iterator(self, cls):
        # Create new heap with 5 elements
        h = cls(10)
        h = h.insert(30)
        h = h.insert(20)
        h = h.insert(5)
        h = h.insert(100)

        # Convert to list using iterator
        self.assertEqual([5, 10, 20, 30, 100], list(h))

    def _heap_custom_compare(self, cls):
        h = cls(cmp=lambda a, b: len(a) - len(b))
        h = h.insert("give")
        h = h.insert("few words")
        h = h.insert("about")
        h = h.insert("union heaps")
        h = h.insert("implementation")

        # Convert to list using iterator
        self.assertEqual(["give",
                          "about",
                          "few words",
                          "union heaps",
                          "implementation"], list(h))

    def _heap_compare_with_keyfunc(self, cls):
        from operator import itemgetter

        # Create new heap with 5 elements
        h = cls(key=itemgetter(1))
        h = h.insert((10, 10))
        h = h.insert((30, 15))
        h = h.insert((20, 110))
        h = h.insert((40, -10))
        h = h.insert((50, 100))

        # Convert to list using iterator
        self.assertEqual(
            [(40, -10), (10, 10), (30, 15), (50, 100), (20, 110)],
            list(h)
        )

    def test_skew_heap_basic(self):
        self._heap_basic_operations(SkewHeap)

    def test_pairing_heap_basic(self):
        self._heap_basic_operations(PairingHeap)

    def test_skew_heap_iterator(self):
        self._heap_iterator(SkewHeap)

    def test_pairing_heap_iterator(self):
        self._heap_iterator(PairingHeap)

    def test_skew_heap_key_func(self):
        self._heap_compare_with_keyfunc(SkewHeap)

    def test_pairing_heap_key_func(self):
        self._heap_compare_with_keyfunc(PairingHeap)

    def test_skew_heap_cmp_func(self):
        self._heap_custom_compare(SkewHeap)

    def test_pairing_heap_cmp_func(self):
        self._heap_custom_compare(PairingHeap)
