#!/usr/bin/env python3

from github_to_elastic_search import core


def main():
    config = core.parse_config('config.ini')
    print('Hello ' + config['user'])
    repo = core.get_repo(config)
    all_issues = core.get_all_issues(config)
    print('Found ' + str(len(all_issues)) + ' issues in ' + repo.name +
          ', out of which ' + core.get_number_of_open_issues(all_issues) + ' are open')


if __name__ == "__main__":
    main()
