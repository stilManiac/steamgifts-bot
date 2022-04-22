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

### Docker

#### Run it using a hub.docker.com image
```bash
# Run the container
docker run --name steamgifts -d -it mcinj/docker-steamgifts-bot:latest
# Attach to it to fill in the questions
docker attach steamgifts # to detach, you must use ctrl+p then ctrl+q. 
                         # ctrl+c will kill the container
```

#### Or build it yourself locally
```bash
# Build the image
docker build -t steamgifts:latest .
# Run the container
docker run --name steamgifts -d -it steamgifts:latest
# Attach to it to fill in the questions
docker attach steamgifts # to detach, you must use ctrl+p then ctrl+q. 
                         # ctrl+c will kill the container
```



### Help
Please leave your feedback and bugs in `Issues` page.
