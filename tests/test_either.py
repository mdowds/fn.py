import unittest

from fn.either import Either


class TestEither(unittest.TestCase):

    def test_init(self):
        either = Either(1)
        self.assertEqual(1, either.value)
        self.assertIsNone(either.error)

        error_either = Either(None, Exception("Foo"))
        self.assertIsNone(error_either.value)
        self.assertEqual("Foo", error_either.error.args[0])

    def test_fromfunction(self):
        either = Either.fromfunction(lambda x: x, 2)
        self.assertEqual(2, either.value)
        self.assertIsNone(either.error)

    def test_fromfunction_with_error(self):
        def _raiser(): raise Exception("Foo")
        either = Either.fromfunction(_raiser)
        self.assertIsNone(either.value)
        self.assertEqual("Foo", either.error.args[0])

    def test_error_type(self):
        self.assertEqual(Exception, Either(None, Exception()).error_type)
        self.assertEqual(KeyError, Either(None, KeyError()).error_type)
        self.assertEqual(type(None), Either(1, None).error_type)

    def test_is_error(self):
        self.assertFalse(Either(1).is_error)
        self.assertTrue(Either(None, Exception()).is_error)

    def test_bind(self):
        either = Either(1).bind(lambda x: x + 1)
        self.assertEqual(2, either.value)
        self.assertIsNone(either.error)

    def test_bind_using_rshift(self):
        either = Either(1) >> (lambda x: x + 1)
        self.assertEqual(2, either.value)
        self.assertIsNone(either.error)

    def test_bind_with_error(self):
        either = Either(None, Exception("Foo")).bind(lambda x: x + 1)
        self.assertIsNone(either.value)
        self.assertEqual("Foo", either.error.args[0])

    def test_bind_with_error_func(self):
        def _raiser(x): raise Exception("Foo")
        either = Either(1).bind(_raiser)
        self.assertIsNone(either.value)
        self.assertEqual("Foo", either.error.args[0])
