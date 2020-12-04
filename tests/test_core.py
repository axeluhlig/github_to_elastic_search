import unittest
import context

import core as unit


class TestCore(unittest.TestCase):

    def test_config_parsing(self):
        config = unit.parse_config('../sample_config.ini')
        self.assertEqual(config['user'], 'TestUser')
        self.assertEqual(config['password'], 'TestPassword')

    def test_foo(self):
        self.assertEqual(1, unit.foo())


if __name__ == '__main__':
    unittest.main()
