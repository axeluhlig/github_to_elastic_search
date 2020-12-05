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


if __name__ == '__main__':
    unittest.main()
