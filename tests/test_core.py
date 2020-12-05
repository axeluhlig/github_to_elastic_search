import unittest
import pickle
import context

import core as unit


class TestCore(unittest.TestCase):

    def setUp(self):
        with open('sample_issue_data.pkl', 'rb') as f:
            self.sample_issue_data = pickle.load(f)
        super(TestCore, self).setUp()

    def test_config_parsing(self):
        config = unit.parse_config('../sample_config.ini')
        self.assertEqual(config['user'], 'TestUser')
        self.assertEqual(config['token'], 'TestToken')
        self.assertEqual(config['repository'], 'test/repository')
        self.assertEqual(config['url'], 'https://api.github.com')


if __name__ == '__main__':
    unittest.main()
