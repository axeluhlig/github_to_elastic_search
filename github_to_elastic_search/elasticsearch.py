from elasticsearch import Elasticsearch as ES
from elasticsearch.client import IndicesClient


class ElasticSearch():

    COMMIT_INDEX_NAME = 'commits'

    def __init__(self, config):
        self.config = config
        self.es = ES(hosts=[config.get('elasticsearch', 'url')])
        self.ic = IndicesClient(self.es)

    def push_commits(self, commits):
        self.__ensure_index_exists(self.COMMIT_INDEX_NAME)
        for commit in commits:
            self.__push_commit(commit)
        print('push of all commits to elasticsearch successful')

    def __push_commit(self, commit):
        self.es.index(self.COMMIT_INDEX_NAME, id=commit['sha'], body=commit)

    def __ensure_index_exists(self, index_name):
        if not self.ic.exists(index=index_name):
            self.ic.create(index_name)

