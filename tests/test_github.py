import unittest
import context
import requests_mock

from github_to_elastic_search import github


class TestGithub(unittest.TestCase):

    def setUp(self):
        self.unit = github.Github({'user': 'TestUser', 'token': 'TestToken',
                                   'repository': 'test/repository', 'url': 'https://test.url.com'})
        super(TestGithub, self).setUp()

    @requests_mock.Mocker()
    def test_get_user_name(self, m):
        m.get('https://test.url.com/user', json={'name': 'TestUser'})
        self.assertEqual(self.unit.get_user_name(), 'TestUser')

    @requests_mock.Mocker()
    def test_get_all_commits_raw(self, m):
        query_url = 'https://test.url.com/repos/test/repository/commits?per_page=50&page='
        json_response_0 = [{'sha': 1}, {'sha': 2}]
        json_response_1 = [{'sha': 3}, {'sha': 4}]
        json_response_2 = []
        m.get(query_url + '0', json=json_response_0)
        m.get(query_url + '1', json=json_response_1)
        m.get(query_url + '2', json=json_response_2)
        
        json_data = self.unit.get_all_commits_raw()

        self.assertEqual(json_data, json_response_0 + json_response_1)


if __name__ == '__main__':
    unittest.main()
