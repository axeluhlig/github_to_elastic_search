import unittest
import context

import core as unit


class TestCore(unittest.TestCase):

    def test_foo(self):
        self.assertEqual(1, unit.foo())


if __name__ == '__main__':
    unittest.main()
