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
        self.unit.ic = FakeIndicesClient()
        self.unit.es = FakeElasticSearch()
        super(TestElasticSearch, self).setUp()

    def test_push_commits_index_creation_needed(self):
        # Arrange
        commits = [{'sha': 'arbitrary sha', 'data': 'arbitrary data'}]

        # Act
        self.unit.push_commits(commits)
        
        # Assert
        self.assertTrue('commits' in self.unit.ic.indices)

    def test_push_commits_index_creation_not_needed(self):
        # Arrange
        self.unit.ic = FakeIndicesClient(initial_indices=['commits'])
        commits = [{'sha': 'arbitrary sha', 'data': 'arbitrary data'}]
        
        # Act
        self.unit.push_commits(commits)

        # Assert
        self.assertTrue(self.unit.ic.indices == ['commits'])

    def test_push_commits_no_sha(self):
        # Arrange
        self.unit.ic = FakeIndicesClient(initial_indices=['commits'])
        commits = [{'no_sha': 'arbitrary_string', 'data': 'arbitrary data'}]
        
        # Act and Assert
        with self.assertRaises(KeyError):
            self.unit.push_commits(commits)

    def test_push_commits_new_commit(self):
        # Arrange
        self.unit.ic = FakeIndicesClient(initial_indices=['commits'])
        commits = [{'sha': 'arbitrary sha', 'data': 'arbitrary data'}]
        expected_els_data = [{'body': {'data': 'arbitrary data', 'sha': 'arbitrary sha'}, 'id': 'arbitrary sha', 'index': 'commits'}]
        
        # Act
        self.unit.push_commits(commits)
        
        # Assert
        self.assertTrue(self.unit.es.data == expected_els_data)

    def test_push_commits_already_existing_commit(self):
        # Arrange
        self.unit.ic = FakeIndicesClient(initial_indices=['commits'])
        expected_els_data = [{'body': {'data': 'arbitrary data',
                                       'sha': 'arbitrary sha'}, 'id': 'arbitrary sha', 'index': 'commits'}]
        self.unit.es = FakeElasticSearch(initial_data=expected_els_data)
        commits = [{'sha': 'arbitrary sha', 'data': 'arbitrary data'}]
        
        # Act
        self.unit.push_commits(commits)

        # Assert
        self.assertTrue(self.unit.es.data == expected_els_data)


if __name__ == '__main__':
    unittest.main()
