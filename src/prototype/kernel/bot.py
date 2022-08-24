from telebot.async_telebot import AsyncTeleBot
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()


class Bot:
    sBot = AsyncTeleBot(os.getenv("TOK"))
    @staticmethod
    def bot_polling(bot):
        asyncio.run(bot.polling(non_stop=True))
