# - *- coding: utf- 8 - *-
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
