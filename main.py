#!/usr/bin/env python3

import pickle

from github_to_elastic_search import core, github


def main():
    config = core.parse_config('config.ini')
    gh = github.Github(config)
    print('Hello ' + gh.get_user_name())
    commits = gh.get_all_commits_annotated()


if __name__ == "__main__":
    main()
