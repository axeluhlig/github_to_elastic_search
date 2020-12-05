import requests

class Github():
    def __init__(self, config):
        self.config = config

    def __query_github(self, api_call):
        url = self.config['url'] + api_call
        r = requests.get(
            url, headers={'Authorization': 'token ' + self.config['token']})
        if r.status_code != 200:
            print('Error while fetching data')
        return r.json()

    def get_user_name(self):
        json_data = self.__query_github('/user')
        return json_data['name']