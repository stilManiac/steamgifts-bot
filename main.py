import sys
import requests
from bs4 import BeautifulSoup
import json
import time
import threading
from requests import RequestException

try:
    file = open('cookie.txt', 'r')
    cook = file.readline()
    if len(cook) == 0:
        print('There is no cookie in cookie.txt file')
        time.sleep(30)
        sys.exit(0)
except FileNotFoundError:
    print('Cant find cookie.txt file')
    time.sleep(30)
    sys.exit(0)

timeout = 900
pages = 1


def get_soup_from_page(url):
    global cookies 

    cookies = {'PHPSESSID': cook}
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
        time.sleep(120)
        get_page()
    except TypeError:
        print('Cant recognize your cookie value.')
        time.sleep(30)
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
                    time.sleep(timeout)
                    get_games()
                    break

                game_cost = item.find_all('span', {'class': 'giveaway__heading__thin'})

                last_div = None
                for last_div in game_cost:
                    pass
                if last_div:
                    game_cost = last_div.getText().replace('(', '').replace(')', '').replace('P', '')

                game_name = item.find('a', {'class': 'giveaway__heading__name'}).text

                if int(points) - int(game_cost) < 0:
                    print('Not enough points to enter: ' + game_name)
                    continue
                elif int(points) - int(game_cost) > 0:
                    entry_gift(item.find('a', {'class': 'giveaway__heading__name'})['href'].split('/')[2])
                
            n = n+1
        except AttributeError as e:
            break

    print('List of games is ended. Waiting 2 min to update...')
    time.sleep(120)
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
        print('> Bot has entered giveaway: ' + game_name)
        time.sleep(5)


def inputs_data():
    global timeout
    global pages

    while 1:
        cmd = input().split()
        if cmd == '!help':
            print(' [ HELP BOX ]')
            print('!sleep [arg]\t- change a sleeping interval in sec (default is 900 sec)')
            print('!page [arg]\t- set a final page')
        if len(cmd) == 1:
            print('!help to see available commands')
        if cmd[0] == '!sleep':
            try:
                timeout = int(cmd[1])
                print('Successfuly set interval to ' + (timeout))
            except ValueError:
                print('Expect a digit!')

        elif cmd[0] == '!page':
            try:
                pages = int(cmd[1])
                print('Successfuly set final page to ' + str(pages))
            except ValueError:
                print('Expect a digit!')


if __name__ == '__main__':
    thread = threading.Thread(target=inputs_data)
    thread.start()
    get_page()
    get_games()
