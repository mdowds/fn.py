#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Fn.py library"""

import unittest

from fn import op
from fn import _
from fn import F 
from fn import iter as iters 

import operator
import itertools

class OperatorTestCase(unittest.TestCase):

    def test_currying(self):
        def add(first):
            def add(second):
                return first + second
            return add

        self.assertEqual(1, op.curry(add, 0, 1))

    def test_apply(self):
        self.assertEqual(10, op.apply(operator.add, [2,8]))

    def test_flip(self):
        self.assertEqual(10, op.flip(operator.sub)(2, 12))

class UnderscoreTestCase(unittest.TestCase):

    def test_identity_default(self):
        self.assertEqual(10, _(10))

    def test_arithmetic(self):
        # operator +
        self.assertEqual(7, (_ + 2)(5))
        self.assertEqual([10,11,12], list(map(_ + 10, [0,1,2])))
        # operator -
        self.assertEqual(3, (_ - 2)(5))
        self.assertEqual(13, (_ - 2 + 10)(5))
        self.assertEqual([0,1,2], list(map(_ - 10, [10,11,12])))
        # operator * 
        self.assertEqual(10, (_ * 2)(5))
        self.assertEqual(50, (_ * 2 + 40)(5))
        self.assertEqual([0,10,20], list(map(_ * 10, [0,1,2])))
        # operator /
        self.assertEqual(5, (_ / 2)(10))
        self.assertEqual(6, (_ / 2 + 1)(10))
        self.assertEqual([1,2,3], list(map(_ / 10, [10,20,30])))
        # operator **
        self.assertEqual(100, (_ ** 2)(10))
        # operator %
        self.assertEqual(1, (_ % 2)(11))
        # operator << 
        self.assertEqual(32, (_ << 2)(8))
        # operator >> 
        self.assertEqual(2, (_ >> 2)(8))
        # operator (-a)
        self.assertEqual(10,  (-_)(-10))
        self.assertEqual(-10, (-_)(10))
        # operator (+a)
        self.assertEqual(10,  (+_)(10))
        self.assertEqual(-10, (+_)(-10))
        # operator (~a)
        self.assertEqual(-11, (~_)(10))

    def test_arithmetic_multiple(self):
        self.assertEqual(10, (_ + _)(5, 5))
        self.assertEqual(0, (_ - _)(5, 5))
        self.assertEqual(25, (_ * _)(5, 5))
        self.assertEqual(1, (_ / _)(5, 5))

    def test_arithmetic_swap(self):
        # operator +
        self.assertEqual(7, (2 + _)(5))
        self.assertEqual([10,11,12], list(map(10 + _, [0,1,2])))
        # operator -
        self.assertEqual(3, (8 - _)(5))
        self.assertEqual(13, (8 - _ + 10)(5))
        self.assertEqual([10,9,8], list(map(10 - _, [0,1,2])))
        # operator * 
        self.assertEqual(10, (2 * _)(5))
        self.assertEqual(50, (2 * _ + 40)(5))
        self.assertEqual([0,10,20], list(map(10 * _, [0,1,2])))
        # operator /
        self.assertEqual(5, (10 / _)(2))
        self.assertEqual(6, (10 / _ + 1)(2))
        self.assertEqual([10,5,2], list(map(100 / _, [10,20,50])))
        # operator **
        self.assertEqual(100, (10**_)(2))
        # operator %
        self.assertEqual(1, (11 % _)(2))
        # operator << 
        self.assertEqual(32, (8 << _)(2))
        # operator >> 
        self.assertEqual(2, (8 >> _)(2))

    def test_bitwise(self):
        # and
        self.assertTrue( (_ & 1)(1))
        self.assertFalse((_ & 1)(0))
        self.assertFalse((_ & 0)(1))
        self.assertFalse((_ & 0)(0))
        # or 
        self.assertTrue( (_ | 1)(1))
        self.assertTrue( (_ | 1)(0))
        self.assertTrue( (_ | 0)(1))
        self.assertFalse((_ | 0)(0))
        # xor
        self.assertTrue( (_ ^ 1)(0))
        self.assertTrue( (_ ^ 0)(1))
        self.assertFalse((_ ^ 1)(1))
        self.assertFalse((_ ^ 0)(0))

    def test_bitwise_swap(self):
        # and
        self.assertTrue( (1 & _)(1))
        self.assertFalse((1 & _)(0))
        self.assertFalse((0 & _)(1))
        self.assertFalse((0 & _)(0))
        # or 
        self.assertTrue( (1 | _)(1))
        self.assertTrue( (1 | _)(0))
        self.assertTrue( (0 | _)(1))
        self.assertFalse((0 | _)(0))
        # xor
        self.assertTrue( (1 ^ _)(0))
        self.assertTrue( (0 ^ _)(1))
        self.assertFalse((1 ^ _)(1))
        self.assertFalse((0 ^ _)(0))

    def test_getattr(self):
        class GetattrTest(object):
            def __init__(self):
                self.doc = "TestCase"

        self.assertEqual("TestCase", (_.doc)(GetattrTest()))
        self.assertEqual("TestCaseTestCase", (_.doc * 2)(GetattrTest()))
        self.assertEqual("TestCaseTestCase", (_.doc + _.doc)(GetattrTest(), GetattrTest()))

    def test_call_method(self):
        self.assertEqual(["test", "case"], (_.call("split"))("test case"))
        self.assertEqual("str", _.__name__(str))

    def test_comparator(self):
        self.assertTrue((_ < 7)(1))
        self.assertFalse((_ < 7)(10))
        self.assertTrue((_ > 20)(25))
        self.assertFalse((_ > 20)(0))
        self.assertTrue((_ <= 7)(6))
        self.assertTrue((_ <= 7)(7))
        self.assertFalse((_ <= 7)(8))
        self.assertTrue((_ >= 7)(8))
        self.assertTrue((_ >= 7)(7))
        self.assertFalse((_ >= 7)(6))
        self.assertTrue((_ == 10)(10))
        self.assertFalse((_ == 10)(9))

    def test_comparator_multiple(self):
        self.assertTrue((_ < _)(1, 2))
        self.assertFalse((_ < _)(2, 1))
        self.assertTrue((_ > _)(25, 20))
        self.assertFalse((_ > _)(20, 25))
        self.assertTrue((_ <= _)(6, 7))
        self.assertTrue((_ <= _)(7, 7))
        self.assertFalse((_ <= _)(8, 7))
        self.assertTrue((_ >= _)(8, 7))
        self.assertTrue((_ >= _)(7, 7))
        self.assertFalse((_ >= _)(6, 7))
        self.assertTrue((_ == _)(10, 10))
        self.assertFalse((_ == _)(9, 10))

    def test_comparator_filter(self):
        self.assertEqual([0,1,2], list(filter(_ < 5, [0,1,2,10,11,12])))

    def test_slicing(self):
        self.assertEqual(0,       (_[0])(range(10)))
        self.assertEqual(9,       (_[-1])(range(10)))
        self.assertEqual([3,4,5], (_[3:])(range(6)))
        self.assertEqual([0,1,2], (_[:3])(range(10)))
        self.assertEqual([1,2,3], (_[1:4])(range(10)))
        self.assertEqual([0,2,4], (_[0:6:2])(range(10)))

    def test_slicing_multiple(self):
        self.assertEqual(0, (_[_])(range(10), 0))
        self.assertEqual(8, (_[_ * (-1)])(range(10), 2))

class CompositionTestCase(unittest.TestCase):

    def test_composition(self):
        def f(x): return x * 2
        def g(x): return x + 10

        self.assertEqual(30, (F(f) << g)(5))

        def z(x): return x * 20
        self.assertEqual(220, (F(f) << F(g) << F(z))(5))

    def test_partial(self):
        # Partial should work if we pass additional arguments to F constructor
        f = F(operator.add, 10) << F(operator.add, 5)
        self.assertEqual(25, f(10))

    def test_underscore(self):
        self.assertEqual([1, 4, 9], list(map(F() << (_ ** 2) << _ + 1, range(3))))    


class IteratorsTestCase(unittest.TestCase):

    def test_zipwith(self):
        zipper = iters.zipwith(operator.add)
        self.assertEqual([10,11,12], list(zipper([0,1,2], itertools.repeat(10))))

        zipper = iters.zipwith(_ + _)
        self.assertEqual([10,11,12], list(zipper([0,1,2], itertools.repeat(10))))

        zipper = F() << list << iters.zipwith(_ + _)
        self.assertEqual([10,11,12], zipper([0,1,2], itertools.repeat(10)))
