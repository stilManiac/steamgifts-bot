import requests
from bs4 import BeautifulSoup

url = 'https://www.steamgifts.com'
cookies = {'PHPSESSID': '7dmn87d0a539pridhlqmm317fs2vbqom6irggn1i84pffud5u0dethqndbcpbvtqsofd4kav483rqac89ma3g2qtbnbmgkas3f0jnf3'}
r = requests.get(url, cookies=cookies)

soup = BeautifulSoup(r.text, 'html.parser')
point = soup.find('span', {'class': 'nav__points'}).text
gifts_list = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['giveaway__row-inner-wrap'])

for test in gifts_list:
    item = test.find('a', {'class': 'giveaway__heading__name'})
    # get code of each gift and add it to a list
    print(item)


def entry_gift():
    payload = {'xsrf_token': '4feb9badc54974acef041a7ebdd6b2e6', 'do': 'entry_insert', 'code': 'AaPCO'}
    entry = requests.post('https://www.steamgifts.com/ajax.php', data=payload, cookies=cookies)
    print(entry.text)


