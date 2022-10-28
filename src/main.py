import sys
import configparser
import requests
import json
import threading

from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from time import sleep
from random import randint
from requests import RequestException
from bs4 import BeautifulSoup

from cli import log

class SteamGifts:
    def __init__(self, cookie, gifts_type, pinned, entered_giveaways, min_points):
        self.cookie = {
            'PHPSESSID': cookie
        }
        self.gifts_type = gifts_type
        self.pinned = pinned
        self.entered_giveaways = entered_giveaways
        self.min_points = int(min_points)

        self.base = "https://www.steamgifts.com"
        self.session = requests.Session()
        self.past_games = None 

        self.filter_url = {
            'All': "search?page=%d",
            'Wishlist': "search?page=%d&type=wishlist",
            'Recommended': "search?page=%d&type=recommended",
            'Copies': "search?page=%d&copy_min=2",
            'DLC': "search?page=%d&dlc=true",
            'New': "search?page=%d&type=new"
        }

    def requests_retry_session(
        self,
        retries=5,
        backoff_factor=0.3
    ):
        session = self.session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=(500, 502, 504),
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def get_soup_from_page(self, url):
        r = self.requests_retry_session().get(url)
        r = requests.get(url, cookies=self.cookie)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def update_info(self):
        soup = self.get_soup_from_page(self.base)

        try:
            self.xsrf_token = soup.find('input', {'name': 'xsrf_token'})['value']
            self.points = int(soup.find('span', {'class': 'nav__points'}).text)  # storage points
        except TypeError:
            log("⛔  Cookie is not valid.", "red")
            sleep(10)
            exit()
    
    def get_entered_giveaways(self, page=1, last_page=20):
        n = page
        game_names = []
        paginated_url = f"{self.base}/giveaways/entered/search?page={n}"
        soup = self.get_soup_from_page(paginated_url)
        last_div = str(soup.find_all('div', {'class': 'pagination'})[0].find_all('a')[-1])

        if not last_page:
            last_page = int(last_div.split('=')[1].split('"')[1])

        if self.entered_giveaways:
           while n <= last_page:

              txt = "⚙️  Retrieving past giveaways from page %d." % n
              log(txt, 'magenta')
              paginated_url = f"{self.base}/giveaways/entered/search?page={n}"
              soup = self.get_soup_from_page(paginated_url)
              game_list = soup.find_all('div', {'class': 'table__row-inner-wrap'})

              if not len(game_list):
                  log("⛔  Page is empty. Please, select another type.", "red")
                  sleep(10)
                  exit()

              for item in game_list:
                  game_name = item.find_all('a',{'class':'table__column__heading'})[0]['href'].split('/')[-1]
                  game_names.append(game_name) 
                  continue
              n+=1
              
        self.past_games = set(game_names) 

        return self.past_games

    def get_game_content(self, game_names, page=1):
        n = page
        game_str = ' '.join(game_names)

        while n <= 3:

            txt = "⚙️  Retrieving games from %d page." % n
            log(txt, "magenta")
            filtered_url = self.filter_url[self.gifts_type] % n
            paginated_url = f"{self.base}/giveaways/{filtered_url}"

            soup = self.get_soup_from_page(paginated_url)
            game_list = soup.find_all('div', {'class': 'giveaway__row-inner-wrap'})

            if not len(game_list):
                log("⛔  Page is empty. Please, select another type.", "red")
                sleep(10)
                exit()

            for item in game_list:
                if len(item.get('class', [])) == 2 and not self.pinned:
                    continue

                if self.points == 0 or self.points < self.min_points:
                    txt = f"🛋️  Sleeping to get 6 points. We have {self.points} points, but we need {self.min_points} to start."
                    log(txt, "yellow")
                    sleep(900)
                    self.start()
                    break

                game_cost = item.find_all('span', {'class': 'giveaway__heading__thin'})[-1]

                if game_cost:
                    game_cost = game_cost.getText().replace('(', '').replace(')', '').replace('P', '')
                else:
                    continue
                
                game_name = item.find('a')['href'].split('/')[-1]
                if game_name not in game_names:
                    continue

                if self.points - int(game_cost) < 0:
                    txt = f"⛔ Not enough points to enter: {game_name}"
                    log(txt, "red")
                    continue

                elif self.points - int(game_cost) >= 0:
                    game_id = item.find('a', {'class': 'giveaway__heading__name'})['href'].split('/')[2]
                    res = self.entry_gift(game_id)
                    if res:
                        self.points -= int(game_cost)
                        txt = f"🎉 One more game! Has just entered {game_name}"
                        log(txt, "green")
                        sleep(randint(3, 7))

            n+=1

        t_secs = 3600
        log(f"🛋️  List of games is ended. Waiting {t_secs/60}  mins to update...", "yellow")
        sleep(t_secs)
        self.start()

    def entry_gift(self, game_id):
        payload = {'xsrf_token': self.xsrf_token, 'do': 'entry_insert', 'code': game_id}
        entry = requests.post('https://www.steamgifts.com/ajax.php', data=payload, cookies=self.cookie)
        json_data = json.loads(entry.text)

        if json_data['type'] == 'success':
            return True

    def start(self):
        self.update_info()

        if self.points > 0:
            txt = "🤖 Hoho! I am back! You have %d points. Lets hack." % self.points
            log(txt, "blue")

        if self.past_games is None:
            self.get_entered_giveaways()

        self.get_game_content(self.past_games)
