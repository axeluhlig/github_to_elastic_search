import unittest
import pickle
import context

from github_to_elastic_search import core as unit


class TestCore(unittest.TestCase):

    def test_config_parsing(self):
        config = unit.parse_config('../sample_config.ini')
        self.assertEqual(config['user'], 'TestUser')
        self.assertEqual(config['token'], 'TestToken')
        self.assertEqual(config['repository'], 'test/repository')
        self.assertEqual(config['url'], 'https://api.github.com')


if __name__ == '__main__':
    unittest.main()
