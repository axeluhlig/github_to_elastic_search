import unittest
import context
import requests_mock
import configparser

from github_to_elastic_search import elasticsearch


class FakeIndicesClient():
    def __init__(self, initial_indices=None):
        self.indices = initial_indices
        if initial_indices is None:
            self.indices = []

    def exists(self, index):
        return index in self.indices

    def create(self, index):
        self.indices.append(index)


class FakeElasticSearch():
    def create(self, index, id, body):
        return True


class TestElasticSearch(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config['elasticsearch'] = {'url': 'localhost:9200'}
        self.unit = elasticsearch.ElasticSearch(config)
        super(TestElasticSearch, self).setUp()

    def test_push_commits_index_creation_needed(self):
        fake_indices_client = FakeIndicesClient()
        self.unit.ic = fake_indices_client
        self.unit.es = FakeElasticSearch()
        commits = [{'sha': 'random sha', 'data': 'random data'}]
        self.unit.push_commits(commits)
        self.assertTrue('commits' in fake_indices_client.indices)

    def test_push_commits_no_sha(self):
        commits = [{'no_sha': 'random_string', 'data': 'radnom data'}]
        with self.assertRaises(KeyError):
            self.unit.push_commits(commits)

    # use mocks instead of els
    # test new commit
    # test already existing commmit
    # test updating exitining but outdated commit
    # test fail if no share


if __name__ == '__main__':
    unittest.main()
