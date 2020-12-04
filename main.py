#!/usr/bin/env python3

from github_to_elastic_search import core


def main():
    config = core.parse_config('sample_config.ini')
    print('Hello ' + config['user'] + ', you rock!')


if __name__ == "__main__":
    main()
