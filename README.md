### About
The bot is specially designed for [SteamGifts.com](https://www.steamgifts.com/)

### Features
- Automatically enters giveaways.
- Undetectable.
- Сonfigurable.
- Sleeps to restock the points.
- Can run 24/7.


## Instructions
 1. Rename `config/config.ini.example` to `config/config.ini`. 
 2. Add your PHPSESSION cookie to it.
 3. Modifying the other settings is optional.

### Run from sources

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
cd src
python run.py
```

### Docker
#### Run it
```bash
# Run the container
docker run --name steamgifts -d -v /path/to/the/config/folder:/config mcinj/docker-steamgifts-bot:v2.0
```

#### Or build it yourself locally
```bash
# Build the image
docker build -t steamgifts:latest .
# Run the container
docker run --name steamgifts -d -v /path/to/the/config/folder:/config steamgifts:latest
```



### Help
Please leave your feedback and bugs in `Issues` page.
