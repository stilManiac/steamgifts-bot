import configparser
from configparser import ConfigParser

import log

logger = log.get_logger(__name__)
config = configparser.ConfigParser()


class MyException(Exception):
    pass


def value_range(min, max):
    return [str(x) for x in [*range(min, max + 1)]]


class MyConfig(ConfigParser):
    def __init__(self, config_file):
        super(MyConfig, self).__init__()

        self.read(config_file)
        self.validate_config()

    def validate_config(self):
        required_values = {
            'DEFAULT': {
                'gift_types': ('All', 'Wishlist', 'Recommended', 'Copies', 'DLC', 'New'),
                'pinned': ('true', 'false'),
                'minimum_points': '%s' % (value_range(0,400)),
                'max_entries': '%s' % (value_range(0,10000)),
                'max_time_left': '%s' % (value_range(0,21600))
            }
        }

        for section, keys in required_values.items():
            if section not in self:
                raise MyException(
                    'Missing section %s in the config file' % section)

            for key, values in keys.items():
                if key not in self[section] or self[section][key] == '':
                    raise MyException((
                                              'Missing value for %s under section %s in ' +
                                              'the config file') % (key, section))

                if values:
                    if self[section][key] not in values:
                        raise MyException((
                                                  'Invalid value for %s under section %s in ' +
                                                  'the config file') % (key, section))


def run():
    from main import SteamGifts as SG

    file_name = '../config/config.ini'
    try:
        with open(file_name) as f:
            config.read_file(f)
            MyConfig(file_name)
    except IOError:
        txt = f"{file_name} doesn't exist. Rename {file_name}.example to {file_name} and fill out."
        logger.warning(txt)
        exit(-1)
    except MyException as e:
        logger.error(e)
        exit(-1)

    config.read(file_name)
    cookie = config['DEFAULT'].get('cookie')
    pinned_games = config['DEFAULT'].getboolean('pinned')
    gift_types = config['DEFAULT'].get('gift_types')
    minimum_points = config['DEFAULT'].getint('minimum_points')
    max_entries = config['DEFAULT'].getint('max_entries')
    max_time_left = config['DEFAULT'].getint('max_time_left')

    s = SG(cookie, gift_types, pinned_games, minimum_points, max_entries, max_time_left)
    s.start()


if __name__ == '__main__':
    run()