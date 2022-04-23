import json
import re
from random import randint
from time import sleep

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

import log

logger = log.get_logger(__name__)

class SteamGifts:
    def __init__(self, cookie, gifts_type, pinned, min_points, max_entries, max_time_left):
        self.cookie = {
            'PHPSESSID': cookie
        }
        self.gifts_type = gifts_type
        self.pinned = pinned
        self.min_points = int(min_points)
        self.max_entries = int(max_entries)
        self.max_time_left = int(max_time_left)

        self.base = "https://www.steamgifts.com"
        self.session = requests.Session()

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
            logger.error("⛔  Cookie is not valid.")
            sleep(10)
            exit()

    def determine_time_in_minutes(self, string_time):
        if not string_time:
            logger.error(f"Could not determine time from string {string_time}")
            return None
        match = re.search('(?P<number>[0-9]+) (?P<time_unit>(hour|day|minute|second))', string_time)
        if match:
            number = int(match.group('number'))
            time_unit = match.group('time_unit')
            if time_unit == 'hour':
                return number * 60
            elif time_unit == 'day':
                return number * 24 * 60
            elif time_unit == 'minute':
                return number
            elif time_unit == 'second':
                return 1
            else:
                return None
        else:
            return None

    def get_game_content(self, page=1):
        n = page
        while True:
            txt = "⚙️  Retrieving games from %d page." % n
            logger.info(txt)

            filtered_url = self.filter_url[self.gifts_type] % n
            paginated_url = f"{self.base}/giveaways/{filtered_url}"

            soup = self.get_soup_from_page(paginated_url)

            game_list = soup.find_all('div', {'class': 'giveaway__row-inner-wrap'})

            if not len(game_list):
                random_seconds = randint(900, 1400)
                txt = f"We have run out of gifts to consider. Trying again in {random_seconds} seconds."
                logger.info(txt)
                sleep(random_seconds)
                self.start()
                continue

            for item in game_list:
                if len(item.get('lass', [])) == 2 and not self.pinned:
                    continue

                if self.points == 0 or self.points < self.min_points:
                    random_seconds = randint(900, 1400)
                    txt = f"🛋️  Sleeping {random_seconds} seconds to get more points. We have {self.points} points, but we need {self.min_points} to start."
                    logger.info(txt)
                    sleep(random_seconds)
                    self.start()
                    break

                game_name = item.find('a', {'class': 'giveaway__heading__name'}).text
                game_id = item.find('a', {'class': 'giveaway__heading__name'})['href'].split('/')[2]
                game_cost = item.find_all('span', {'class': 'giveaway__heading__thin'})[-1]
                if game_cost:
                    game_cost = game_cost.getText().replace('(', '').replace(')', '').replace('P', '')
                else:
                    continue
                times = item.select('div span[data-timestamp]')
                game_remaining = times[0].text
                game_remaining_in_minutes = self.determine_time_in_minutes(game_remaining)
                game_created = times[1].text
                game_created_in_minutes = self.determine_time_in_minutes(game_created)
                game_entries = int(item.select('div.giveaway__links span')[0].text.split(' ')[0].replace(',' ,''))

                txt = f"{game_name} {game_cost} - {game_entries} - Created {game_created} ago with {game_remaining} remaining."
                logger.debug(txt)

                if self.points - int(game_cost) < 0:
                    txt = f"⛔ Not enough points to enter: {game_name}"
                    logger.info(txt)
                    continue
                if self.max_time_left > game_remaining_in_minutes:
                    txt = f"Game {game_name} has {game_remaining_in_minutes} left and is above your cutoff of {self.max_time_left} minutes."
                    logger.info(txt)
                    continue
                if self.max_entries > game_entries:
                    txt = f"Game {game_name} has {game_entries} entries is above your cutoff of {self.max_entries} entries."
                    logger.info(txt)
                    continue
                # defensive move
                if self.points - int(game_cost) >= 0:
                    res = self.entry_gift(game_id)
                    if res:
                        self.points -= int(game_cost)
                        txt = f"🎉 One more game! Has just entered {game_name}"
                        logger.info(txt)
                        sleep(randint(3, 7))

            n = n+1

        logger.info("🛋️  List of games is ended. Waiting 2 mins to update...")
        sleep(120)
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
            logger.info(txt)

        self.get_game_content()
