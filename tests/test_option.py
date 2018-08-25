import operator
import sys
import unittest

from fn import option


class InstanceChecker(object):
    if sys.version_info[0] == 2 and sys.version_info[1] <= 6:
        def assertIsInstance(self, inst, cls):
            self.assertTrue(isinstance(inst, cls))


class OptionTestCase(unittest.TestCase, InstanceChecker):

    def test_create_option(self):
        self.assertIsInstance(option.Option("A"), option.Full)
        self.assertIsInstance(option.Option(10), option.Full)
        self.assertIsInstance(option.Option(10, lambda x: x > 7), option.Full)
        self.assertIsInstance(option.Option(None), option.Empty)
        self.assertIsInstance(option.Option(False), option.Full)
        self.assertIsInstance(option.Option(0), option.Full)
        self.assertIsInstance(option.Option(False, checker=bool), option.Empty)
        self.assertIsInstance(option.Option(0, checker=bool), option.Empty)
        self.assertIsInstance(option.Option(10, lambda x: x > 70), option.Empty)

    def test_map_filter(self):
        class Request(dict):
            def parameter(self, name):
                return option.Option(self.get(name, None))

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
        self.assertTrue(option.Empty().empty)
        self.assertTrue(option.Option(None).empty)
        self.assertTrue(option.Option.from_call(lambda: None).empty)
        self.assertFalse(option.Option(10).empty)
        self.assertFalse(option.Full(10).empty)

    def test_lazy_orcall(self):
        def from_mimetype(request):
            # you can return both value or Option
            return request.get("mimetype", None)

        def from_extension(request):
            # you can return both value or Option
            return option.Option(request.get("url", None))\
                        .map(lambda s: s.split(".")[-1])

        # extract value from extension
        r = dict(url="myfile.png")
        self.assertEqual(
            "PNG",
            option.Option(
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
            option.Option(
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
            option.Option(
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
            @option.optionable
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
        self.assertEqual("Full(10)", str(option.Full(10)))
        self.assertEqual("Full(in box!)", str(option.Full("in box!")))
        self.assertEqual("Empty()", str(option.Empty()))
        self.assertEqual("Empty()", str(option.Option(None)))

    def test_option_repr(self):
        self.assertEqual("Full(10)", repr(option.Full(10)))
        self.assertEqual("Full(in box!)", repr(option.Full("in box!")))
        self.assertEqual("Empty()", repr(option.Empty()))
        self.assertEqual("Empty()", repr(option.Option(None)))

    def test_static_constructor(self):
        self.assertEqual(option.Empty(), option.Option.from_value(None))
        self.assertEqual(option.Full(10), option.Option.from_value(10))
        self.assertEqual(option.Empty(), option.Option.from_call(lambda: None))
        self.assertEqual(
            option.Full(10),
            option.Option.from_call(operator.add, 8, 2)
        )
        self.assertEqual(
            option.Empty(),
            option.Option.from_call(lambda d, k: d[k],
                                    {"a": 1}, "b", exc=KeyError)
        )

    def test_flatten_operation(self):
        self.assertEqual(option.Empty(), option.Empty(option.Empty()))
        self.assertEqual(option.Empty(), option.Empty(option.Full(10)))
        self.assertEqual(option.Empty(), option.Full(option.Empty()))
        self.assertEqual("Full(20)", str(option.Full(option.Full(20))))
