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
    def __init__(self, initial_data=None):
        self.data = initial_data
        if initial_data is None:
            self.data = []

    def index(self, index, id, body):
        new_data = {'index': index, 'id': id, 'body': body}
        if self.data != new_data:
            self.data.append(new_data)


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

    def test_push_commits_index_creation_not_needed(self):
        fake_indices_client = FakeIndicesClient(initial_indices=['commits'])
        self.unit.ic = fake_indices_client
        self.unit.es = FakeElasticSearch()
        commits = [{'sha': 'arbitrary sha', 'data': 'arbitrary data'}]
        self.unit.push_commits(commits)
        self.assertTrue(fake_indices_client.indices == ['commits'])

    def test_push_commits_no_sha(self):
        commits = [{'no_sha': 'arbitrary_string', 'data': 'arbitrary data'}]
        with self.assertRaises(KeyError):
            self.unit.push_commits(commits)

    def test_push_commits_new_commit(self):
        self.unit.ic = FakeIndicesClient(initial_indices=['commits'])
        self.unit.es = FakeElasticSearch()
        commits = [{'sha': 'arbitrary sha', 'data': 'arbitrary data'}]
        self.unit.push_commits(commits)
        expected_els_data = [{'body': {'data': 'arbitrary data',
                                       'sha': 'arbitrary sha'}, 'id': 'arbitrary sha', 'index': 'commits'}]
        self.assertTrue(self.unit.es.data == expected_els_data)

    def test_push_commits_already_existing_commit(self):
        expected_els_data = [{'body': {'data': 'arbitrary data',
                                       'sha': 'arbitrary sha'}, 'id': 'arbitrary sha', 'index': 'commits'}]
        self.unit.ic = FakeIndicesClient(initial_indices=['commits'])
        self.unit.es = FakeElasticSearch(initial_data=expected_els_data)
        commits = [{'sha': 'arbitrary sha', 'data': 'arbitrary data'}]
        self.unit.push_commits(commits)
        self.assertTrue(self.unit.es.data == expected_els_data)

    # for debugging only
    # def test_push_commits_not_faked(self):
    #     commits = [{'sha': 'arbitrarySha', 'data': 'arbitrary data'}]
    #     self.unit.push_commits(commits)
    #     self.assertTrue(1, 1)


if __name__ == '__main__':
    unittest.main()
