#!/usr/bin/env python3

import pickle
from configparser import ConfigParser


from github_to_elastic_search import github


def main():
    config = ConfigParser()
    config.read('config.ini')
    gh = github.Github(config)
    print('Hello ' + gh.get_user_name())
    commits = gh.get_all_commits_annotated()


if __name__ == "__main__":
    main()
