import unittest

from fnplus.either import Either


class TestEither(unittest.TestCase):

    def test_init(self):
        either = Either(1, None)
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

    def test_frompartialfunction(self):
        either = Either.frompartialfunction(lambda x: x)(2)
        self.assertEqual(2, either.value)
        self.assertIsNone(either.error)

    def test_frompartialfunction_with_error(self):
        def _raiser(): raise Exception("Foo")

        either = Either.frompartialfunction(_raiser)()
        self.assertIsNone(either.value)
        self.assertEqual("Foo", either.error.args[0])

    def test_frompartialfunction_with_derived_error(self):
        def _raiser(): raise KeyError("Foo")

        either = Either.frompartialfunction(_raiser)()
        self.assertIsNone(either.value)
        self.assertEqual("Foo", either.error.args[0])

    def test_error_type(self):
        self.assertEqual(Exception, Either(None, Exception()).error_type)
        self.assertEqual(KeyError, Either(None, KeyError()).error_type)
        self.assertEqual(type(None), Either(1, None).error_type)

    def test_call(self):
        either = Either(1).call(lambda x: x+1)
        self.assertEqual(2, either.value)
        self.assertIsNone(either.error)

    def test_call_with_error(self):
        either = Either(None, Exception("Foo")).call(lambda x: x+1)
        self.assertIsNone(either.value)
        self.assertEqual("Foo", either.error.args[0])

    def test_try_call_partial(self):
        bound_inc = Either.try_call_partial(lambda x: x + 1)
        self.assertEqual(4, bound_inc(Either(3)).value)
        self.assertIsNone(bound_inc(Either(None, Exception())).value)

    def test_try_call_partial_with_error(self):
        def _raiser(): raise Exception("Foo")
        bound_either = Either.try_call_partial(_raiser)(Either(None, Exception("Bar")))

        self.assertIsNone(bound_either.value)
        self.assertEqual("Bar", bound_either.error.args[0])
