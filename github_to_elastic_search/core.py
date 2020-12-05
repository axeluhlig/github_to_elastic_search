from configparser import ConfigParser


def parse_config(path_to_config):
    config = ConfigParser()
    config.read(path_to_config)
    out = {}
    out['user'] = config.get('github', 'user')
    out['token'] = config.get('github', 'token')
    out['repository'] = config.get('github', 'repository')
    out['url'] = config.get('github', 'url')
    return out
