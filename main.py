"""
telegram captcha bot for groups

bot sending dice for new user and ask dice value
"""


import logging
from aiogram import Bot, Dispatcher
import asyncio
import os
from dotenv import load_dotenv
import handlers

load_dotenv()


API_TOKEN = os.getenv("API_TOKEN")
logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    dp.include_routers(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
