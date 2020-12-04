from configparser import ConfigParser
from github import Github


def parse_config(path_to_config):
    config = ConfigParser()
    config.read(path_to_config)
    out = {}
    out['user'] = config.get('github', 'user')
    out['token'] = config.get('github', 'token')
    out['repository'] = config.get('github', 'repository')
    return out


def get_repo(config):
    g = Github(config['user'], config['token'])
    return g.get_repo(config['repository'])


def get_all_issues(config):
    g = Github(config['user'], config['token'])
    all_issues = []
    issues = g.get_repo(config['repository']).get_issues(state='all')
    for issue in issues:
        all_issues.append(issue)
    return all_issues
