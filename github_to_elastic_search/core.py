from configparser import ConfigParser


def parse_config(path_to_config):
    config = ConfigParser()
    config.read(path_to_config)
    out = {}
    out['user'] = config.get('github', 'user')
    out['password'] = config.get('github', 'password')
    return out


def foo():
    return 1
