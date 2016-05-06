import operator
import sys
import unittest

from fn import monad


class InstanceChecker(object):
    if sys.version_info[0] == 2 and sys.version_info[1] <= 6:
        def assertIsInstance(self, inst, cls):
            self.assertTrue(isinstance(inst, cls))


class OptionTestCase(unittest.TestCase, InstanceChecker):

    def test_create_option(self):
        self.assertIsInstance(monad.Option("A"), monad.Full)
        self.assertIsInstance(monad.Option(10), monad.Full)
        self.assertIsInstance(monad.Option(10, lambda x: x > 7), monad.Full)
        self.assertIsInstance(monad.Option(None), monad.Empty)
        self.assertIsInstance(monad.Option(False), monad.Full)
        self.assertIsInstance(monad.Option(0), monad.Full)
        self.assertIsInstance(monad.Option(False, checker=bool), monad.Empty)
        self.assertIsInstance(monad.Option(0, checker=bool), monad.Empty)
        self.assertIsInstance(monad.Option(10, lambda x: x > 70), monad.Empty)

    def test_map_filter(self):
        class Request(dict):
            def parameter(self, name):
                return monad.Option(self.get(name, None))

        r = Request(testing="Fixed", empty="   ")

        # full chain
        self.assertEqual("FIXED", r.parameter("testing")
                                   .map(operator.methodcaller("strip"))
                                   .filter(len)
                                   .map(operator.methodcaller("upper"))
                                   .get_or(""))

        # breaks on filter
        self.assertEqual("", r.parameter("empty")
                              .map(operator.methodcaller("strip"))
                              .filter(len)
                              .map(operator.methodcaller("upper"))
                              .get_or(""))

        # breaks on parameter
        self.assertEqual("", r.parameter("missed")
                              .map(operator.methodcaller("strip"))
                              .filter(len)
                              .map(operator.methodcaller("upper"))
                              .get_or(""))

    def test_empty_check(self):
        self.assertTrue(monad.Empty().empty)
        self.assertTrue(monad.Option(None).empty)
        self.assertTrue(monad.Option.from_call(lambda: None).empty)
        self.assertFalse(monad.Option(10).empty)
        self.assertFalse(monad.Full(10).empty)

    def test_lazy_orcall(self):
        def from_mimetype(request):
            # you can return both value or Option
            return request.get("mimetype", None)

        def from_extension(request):
            # you can return both value or Option
            return monad.Option(request.get("url", None))\
                        .map(lambda s: s.split(".")[-1])

        # extract value from extension
        r = dict(url="myfile.png")
        self.assertEqual(
            "PNG",
            monad.Option(
                r.get("type", None)
            ).or_call(
                from_mimetype, r
            ).or_call(
                from_extension, r
            ).map(
                operator.methodcaller("upper")
            ).get_or("")
        )

        # extract value from mimetype
        r = dict(url="myfile.svg", mimetype="png")
        self.assertEqual(
            "PNG",
            monad.Option(
                r.get("type", None)
            ).or_call(
                from_mimetype, r
            ).or_call(
                from_extension, r
            ).map(
                operator.methodcaller("upper")
            ).get_or("")
        )

        # type is set directly
        r = dict(url="myfile.jpeg", mimetype="svg", type="png")
        self.assertEqual(
            "PNG",
            monad.Option(
                r.get("type", None)
            ).or_call(
                from_mimetype, r
            ).or_call(
                from_extension, r
            ).map(
                operator.methodcaller("upper")
            ).get_or("")
        )

    def test_optionable_decorator(self):
        class Request(dict):
            @monad.optionable
            def parameter(self, name):
                return self.get(name, None)

        r = Request(testing="Fixed", empty="   ")

        # full chain
        self.assertEqual("FIXED", r.parameter("testing")
                                   .map(operator.methodcaller("strip"))
                                   .filter(len)
                                   .map(operator.methodcaller("upper"))
                                   .get_or(""))

    def test_stringify(self):
        self.assertEqual("Full(10)", str(monad.Full(10)))
        self.assertEqual("Full(in box!)", str(monad.Full("in box!")))
        self.assertEqual("Empty()", str(monad.Empty()))
        self.assertEqual("Empty()", str(monad.Option(None)))

    def test_option_repr(self):
        self.assertEqual("Full(10)", repr(monad.Full(10)))
        self.assertEqual("Full(in box!)", repr(monad.Full("in box!")))
        self.assertEqual("Empty()", repr(monad.Empty()))
        self.assertEqual("Empty()", repr(monad.Option(None)))

    def test_static_constructor(self):
        self.assertEqual(monad.Empty(),  monad.Option.from_value(None))
        self.assertEqual(monad.Full(10), monad.Option.from_value(10))
        self.assertEqual(monad.Empty(),  monad.Option.from_call(lambda: None))
        self.assertEqual(
            monad.Full(10),
            monad.Option.from_call(operator.add, 8, 2)
        )
        self.assertEqual(
            monad.Empty(),
            monad.Option.from_call(lambda d, k: d[k],
                                   {"a": 1}, "b", exc=KeyError)
        )

    def test_flatten_operation(self):
        self.assertEqual(monad.Empty(), monad.Empty(monad.Empty()))
        self.assertEqual(monad.Empty(), monad.Empty(monad.Full(10)))
        self.assertEqual(monad.Empty(), monad.Full(monad.Empty()))
        self.assertEqual("Full(20)", str(monad.Full(monad.Full(20))))
