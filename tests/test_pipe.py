import unittest

from fn.monad import Pipe


class TestPipe(unittest.TestCase):

    def test_init(self):
        pipe = Pipe(1)
        self.assertEqual(1, pipe.value)

    def test_bind(self):
        pipe = Pipe(1).bind(lambda x: x + 1)
        self.assertEqual(2, pipe.value)

    def test_bind_using_rshift(self):
        pipe = Pipe(1) >> (lambda x: x + 1)
        self.assertEqual(2, pipe.value)
