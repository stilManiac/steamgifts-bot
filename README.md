![](https://i.imgur.com/oCob3wQ.gif)

### About
The bot is specially designed for [SteamGifts.com](https://www.steamgifts.com/)

### Features
- Automatically enters giveaways.
- Undetectable.
- Сonvenient user interface.
- Сonfigurable.
- Sleeps to restock the points.
- Can run 24/7.

_Additions to the original bot_
* If one has manually entered only selected giveaways, with this addition, the bot is able to enter only those giveaways by taking into account past giveaways from the "Entered" page.

On startup it asks the user if they want to use past giveaways as a reference of what giveaways to enter (hardcoded to page 20 of a user's entered giveaway page).
If selected, this option is better combined with the 'All' option to give a higher chances of finding a giveaway that matches the past entered giveaways.


### How to run
1. Download the latest version: https://github.com/stilManiac/steamgifts-bot/releases
2. Sign in on [SteamGifts.com](https://www.steamgifts.com/) by Steam.
3. Find `PHPSESSID` cookie in your browser.
4. Start the bot and follow instructions.

### Run from sources
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python src/cli.py
```

### Help
Please leave your feedback and bugs in `Issues` page.
