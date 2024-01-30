# Telegram captcha bot
Еhe bot takes away permissions to write messages from new users, rolls a die and offers to choose value. If user chooses the wrong answer, he gets a ban for 30 seconds, if he chooses the right answer, he gets access to write messages in chat.

# Installation

## 1. Install dependencies

```bash
# create virtual environment
python3 -m venv venv

# enable virtual environment
source venv/bin/activate 

# install dependencies
pip3 install -r ./requirements.txt
```

## 2. Create `.env` file

Copy `example.env` to `.env` file and put API_KEY from your bot in https://t.me/BotFather

```bash
# ./.env
API_TOKEN=https://t.me/BotFather
```

## 3. Run bot
```bash
python3 main.py
```
