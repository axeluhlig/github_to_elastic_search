import requests
import time
import hashlib
import json
import time


class Github():
    def __init__(self, config, avoid_rate_limiting=True):
        self.config = config
        self.avoid_rate_limiting = avoid_rate_limiting

    def __query_github(self, query):
        url = self.config.get('github', 'url') + query
        r = requests.get(
            url, headers={'Authorization': 'token ' + self.config.get('github', 'token')})
        if r.status_code != 200:
            print('Error while fetching data')
        return r.json()

    def get_user_name(self):
        json_data = self.__query_github('/user')
        return json_data['name']

    def get_all_commits_raw(self):
        json_data = []
        page = 0
        while (True):
            query = '/repos/' + \
                self.config.get('github', 'repository') + \
                    '/commits?per_page=50&page=' + str(page)
            new_data = self.__query_github(query)
            if not new_data:
                break
            json_data += new_data
            page += 1
            print('get_all_commits... got page ' + str(page))
            if self.avoid_rate_limiting:
                time.sleep(1)
        return json_data

    def get_all_commits_annotated(self):
        timestamp = time.ctime()
        raw_commits = self.get_all_commits_raw()
        annotated_commits = []
        for commit in raw_commits:
            annotated_commits.append(self.__annotate_commit(commit, timestamp))
        return annotated_commits

    def __annotate_commit(self, commit_json, timestamp):
        data_hash = hashlib.sha224(json.dumps(
            commit_json, sort_keys=True).encode('utf-8')).hexdigest()
        commit_json['data_hash'] = data_hash
        commit_json['last_updated_at'] = timestamp
        return commit_json
