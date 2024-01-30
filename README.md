# Telegram captcha bot
telegram bot for group chats/ showing captcha to new users

At startup, the bot takes away the rights to write messages from new users, rolls a die and offers to choose how many answers it has rolled. If the user chooses the wrong answer, he gets a ban for 30 seconds, if he chooses the right answer, he gets the right to write messages in the chat.

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