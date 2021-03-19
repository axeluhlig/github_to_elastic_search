#!/usr/bin/env python3

import pickle
import time
from configparser import ConfigParser


from github_to_elastic_search import github, elasticsearch


def fetch_and_push_for_ever(config, gh):
    waiting_time = int(config.get('general', 'waiting_time_between_cycles_in_seconds'))
    while(True):
        commits = gh.get_all_commits_annotated()
        els = elasticsearch.ElasticSearch(config)
        els.push_commits(commits)
        print('Starting next cycle in ' + str(waiting_time) + ' seconds')
        time.sleep(waiting_time)


def main():
    config = ConfigParser()
    config.read('config.ini')
    gh = github.Github(config)
    print('Hello ' + gh.get_user_name())
    fetch_and_push_for_ever(config, gh)


if __name__ == "__main__":
    main()
