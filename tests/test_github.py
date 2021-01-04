import unittest
import context
import requests_mock
import time
import configparser


from github_to_elastic_search import github


class TestGithub(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config['github'] = {'user': 'TestUser', 'token': 'TestToken',
                            'repository': 'test/repository', 'url': 'https://test.url.com'}
        self.unit = github.Github(config, avoid_rate_limiting=False)
        super(TestGithub, self).setUp()

    @requests_mock.Mocker()
    def test_get_user_name(self, mock):
        mock.get('https://test.url.com/user', json={'name': 'TestUser'})
        self.assertEqual(self.unit.get_user_name(), 'TestUser')

    @requests_mock.Mocker()
    def test_get_all_commits_raw(self, mock):
        query_url = 'https://test.url.com/repos/test/repository/commits?per_page=50&page='
        json_response_0 = [{'sha': 1}, {'sha': 2}]
        json_response_1 = [{'sha': 3}, {'sha': 4}]
        json_response_2 = []
        mock.get(query_url + '0', json=json_response_0)
        mock.get(query_url + '1', json=json_response_1)
        mock.get(query_url + '2', json=json_response_2)

        json_data = self.unit.get_all_commits_raw()

        self.assertEqual(json_data, json_response_0 + json_response_1)

    @requests_mock.Mocker()
    def test_get_all_commits_annotated(self, mock):
        query_url = 'https://test.url.com/repos/test/repository/commits?per_page=50&page='
        json_response_0 = [{'sha': 1}, {'sha': 2}]
        json_response_1 = []
        mock.get(query_url + '0', json=json_response_0)
        mock.get(query_url + '1', json=json_response_1)

        json_data = self.unit.get_all_commits_annotated()
        current_time = time.time()

        self.assertEqual(json_data[0]['sha'], 1)
        self.assertEqual(json_data[1]['sha'], 2)
        self.assertEqual(
            json_data[0]['data_hash'], 'd643a8de1b40283ff356dd68ddf5d538487cbb0b1ced53e3dd3a83e6')
        self.assertEqual(
            json_data[1]['data_hash'], 'b53c56b35af074d9cf3532791aa403201c5ae0a0c0974da70daeb2ec')
        # 1 second max time gap
        self.assertTrue(current_time - json_data[0]['last_updated_at'] < 1)
        self.assertTrue(current_time - json_data[1]['last_updated_at'] < 1)


if __name__ == '__main__':
    unittest.main()

# Save test data like this:
# with open('data.json', 'w', encoding='utf-8') as f:
#    json.dump(data, f, ensure_ascii=False, indent=4)

# with open('tests/commits_test_data.json', 'r') as j:
#     contents = json.loads(j.read())
