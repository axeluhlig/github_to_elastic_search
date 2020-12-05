import requests
import time


class Github():
    def __init__(self, config):
        self.config = config

    def __query_github(self, query):
        url = self.config['url'] + query
        r = requests.get(
            url, headers={'Authorization': 'token ' + self.config['token']})
        if r.status_code != 200:
            print('Error while fetching data')
        return r.json()

    def get_user_name(self):
        json_data = self.__query_github('/user')
        return json_data['name']

    def get_all_commits_raw(self):
        json_data = []
        page = 0
        while (1):
            query = '/repos/' + \
                self.config['repository'] + \
                    '/commits?per_page=50&page=' + str(page)
            new_data = self.__query_github(query)
            if not new_data:
                break
            json_data += new_data
            page += 1
            print('get_all_commits... got page ' + str(page))
            time.sleep(1)  # avoid rate limiting
        return json_data
