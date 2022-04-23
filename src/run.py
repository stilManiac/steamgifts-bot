import configparser

config = configparser.ConfigParser()


def run():
    from main import SteamGifts as SG

    config.read('config.ini')
    cookie = config['DEFAULT'].get('cookie')

    pinned_games = config['DEFAULT'].getboolean('pinned')

    gift_types = config['DEFAULT'].get('gift_types')

    min_points = config['DEFAULT'].getint('minimum_points')

    s = SG(cookie, gift_types, pinned_games, min_points)
    s.start()


if __name__ == '__main__':
    run()