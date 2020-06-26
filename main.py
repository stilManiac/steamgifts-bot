import sys
import configparser
import requests
import json
import threading

from time import sleep
from random import randint
from requests import RequestException
from bs4 import BeautifulSoup

CONFIG_DEFAULT = {
    'cookie': 'Paste you cookie here',
    'sleeptime': 900
}

def exitMessage(msg):
    print(msg)
    input()
    sys.exit()

def readConfig():
    config = configparser.ConfigParser()

    def initConfig():
        config['STEAMGIFTS'] = CONFIG_DEFAULT
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    if not len(config.read('config.ini')):
        initConfig()
        exitMessage('Init file was created. Please, look into it and set up your cookie.')
    elif list(CONFIG_DEFAULT.keys()) != list(config['STEAMGIFTS'].keys()):
        initConfig()
        exitMessage('Init file was reinitialised due to incorrect format. Please, look into it and set up your cookie.')

    global timeout, cookies
    timeout = config['STEAMGIFTS']['sleeptime']
    cookies = {'PHPSESSID': config['STEAMGIFTS']['cookie']}


pages = 1

def get_soup_from_page(url):
    r = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_page():
    global xsrf_token, points

    try:
        soup = get_soup_from_page('https://www.steamgifts.com')

        xsrf_token = soup.find('input', {'name': 'xsrf_token'})['value']
        points = soup.find('span', {'class': 'nav__points'}).text  # storage points
    except RequestException:
        print('Cant connect to the site')
        print('Waiting 2 minutes and reconnect...')
        sleep(120)
        get_page()
    except TypeError:
        print('Cant recognize your cookie value.')
        sleep(30)
        sys.exit(0)


# get codes of the games
def get_games():
    global game_name
    global pages

    n = 1
    while n <= pages:
        print('Proccessing games from %d page.' % n)

        soup = get_soup_from_page('https://www.steamgifts.com/giveaways/search?page=' + str(n))

        try:
            gifts_list = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['giveaway__row-inner-wrap'])

            for item in gifts_list:
                if int(points) == 0:
                    print('> Sleeping to get 6 points')
                    sleep(timeout)
                    get_games()
                    break

                game_cost = item.find_all('span', {'class': 'giveaway__heading__thin'})

                last_div = None
                for last_div in game_cost:
                    pass
                if last_div:
                    game_cost = last_div.getText().replace('(', '').replace(')', '').replace('P', '')

                game_name = item.find('a', {'class': 'giveaway__heading__name'}).text.encode('utf-8')

                if int(points) - int(game_cost) < 0:
                    print('Not enough points to enter: ' + game_name)
                    continue
                elif int(points) - int(game_cost) > 0:
                    entry_gift(item.find('a', {'class': 'giveaway__heading__name'})['href'].split('/')[2])

            n = n+1
        except AttributeError:
            break

    print('List of games is ended. Waiting 2 min to update...')
    sleep(120)
    get_page()
    get_games()


def entry_gift(code):
    payload = {'xsrf_token': xsrf_token, 'do': 'entry_insert', 'code': code}
    entry = requests.post('https://www.steamgifts.com/ajax.php', data=payload, cookies=cookies)
    json_data = json.loads(entry.text)

    get_page()
    # print(json_data)

    # updating points after entered a giveaway
    if json_data['type'] == 'success':
        print('> Bot has entered giveaway: ' + game_name.decode("utf-8"))
        sleep(randint(10, 30))

if __name__ == '__main__':
    readConfig()

    get_page()
    get_games()
