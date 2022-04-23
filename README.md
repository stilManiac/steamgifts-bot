### About
The bot is specially designed for [SteamGifts.com](https://www.steamgifts.com/)

### Features
- Automatically enters giveaways.
- Undetectable.
- Сonfigurable.
- Sleeps to restock the points.
- Can run 24/7.

### Run from sources
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python src/cli.py
```

### Docker

#### Run it
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
