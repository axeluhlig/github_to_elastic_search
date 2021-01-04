from elasticsearch import Elasticsearch as ES
from elasticsearch.client import IndicesClient


class ElasticSearch():
    def __init__(self, config):
        self.config = config
        self.index_names = {'commits': 'commits'}
        self.es = ES(hosts=[config.get('elasticsearch', 'url')])
        self.ic = IndicesClient(self.es)

    def push_commits(self, commits):
        self.__ensure_index_exists(self.index_names['commits'])
        for commit in commits:
            self.__push_commit(commit)
        print('push of all commits to elasticsearch successful')

    def __push_commit(self, commit):
        self.es.index(
            index=self.index_names['commits'], id=commit['sha'], body=commit)

    def __ensure_index_exists(self, index_name):
        if not self.ic.exists(index=index_name):
            self.ic.create(index_name)


# es.push_commits()
# -> for every commit
# -> push to es, using sha as _id
