# - *- coding: utf- 8 - *-
import asyncio
import time

import requests
from aiogram import Dispatcher
from bs4 import BeautifulSoup
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
from data.config import admins, bot_version, bot_description
from loader import bot
from utils.db_api.sqlite import get_settingsx, update_settingsx

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Уведомление и проверка обновления при запуске скрипта
async def on_startup_notify(dp: Dispatcher):
    if len(admins) >= 1:
        update_link = "https://sites.google.com/view/check-update-autoshop/main-page"

        response = requests.get(update_link)
        soup_parse = BeautifulSoup(response.text, "html.parser")
        get_bot_info = soup_parse.select("p[class$='CDt4Ke zfr3Q']")[0].text.split("=")
        if float(get_bot_info[0]) <= float(bot_version):
            await send_all_admin(f"<b>✅ Бот был успешно запущен</b>\n"
                                 f"➖➖➖➖➖➖➖➖➖➖\n"
                                 f"{bot_description}")
        else:
            update_discription = get_bot_info[2].split("**")
            update_discription = "\n".join(update_discription)
            await send_all_admin(f"<b>✅ Бот был успешно запущен</b>\n"
                                 f"#СЛИТ В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT\n"
                                 f"➖➖➖➖➖➖➖➖➖➖\n"
                                 f"{bot_description}\n"
                                 f"➖➖➖➖➖➖➖➖➖➖\n"
                                 f"<b>❇ Вышло обновление ❇</b>\n"
                                 f"▶ <a href='{get_bot_info[1]}'><b>Скачать обновление</b></a>\n"
                                 f"➖➖➖➖➖➖➖➖➖➖\n"
                                 f"{update_discription}")

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Рассылка сообщения всем администраторам
async def send_all_admin(message, markup=None):
    if markup is None:
        for admin in admins:
            try:
                await bot.send_message(admin, message)
            except:
                pass
    else:
        for admin in admins:
            try:
                await bot.send_message(admin, message, reply_markup=markup)
            except:
                pass

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Очистка имени пользователя от тэгов
def clear_firstname(firstname):
    if "<" in firstname: firstname = firstname.replace("<", "*")
    if ">" in firstname: firstname = firstname.replace(">", "*")
    return firstname


# Проверка на обновление счётчика 24-х часов при запуске
def update_profit():
    settings = get_settingsx()
    now_unix = int(time.time())
    if now_unix - int(settings[4]) >= 86400:
        update_settingsx(profit_buy=now_unix)
    if now_unix - int(settings[5]) >= 86400:
        update_settingsx(profit_refill=now_unix)
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT

# Автоматическая ежечасовая проверка на обновление счётчика 24-х часов
async def update_last_profit():
    while True:
        await asyncio.sleep(3600)
        settings = get_settingsx()
        now_unix = int(time.time())
        if now_unix - int(settings[4]) >= 86400:
            update_settingsx(profit_buy=now_unix)
        if now_unix - int(settings[5]) >= 86400:
            update_settingsx(profit_refill=now_unix)

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Автоматическая проверка обновления каждые 24 часа
async def check_update_bot():
    while True:
        await asyncio.sleep(86400)
        update_link = "https://sites.google.com/view/check-update-autoshop/main-page"

        response = requests.get(update_link)
        soup_parse = BeautifulSoup(response.text, "html.parser")
        get_bot_info = soup_parse.select("p[class$='CDt4Ke zfr3Q']")[0].text.split("=")
        if float(get_bot_info[0]) > float(bot_version):
            update_discription = get_bot_info[2].split("**")
            update_discription = "\n".join(update_discription)
            await send_all_admin(f"<b>❇ Вышло обновление ❇</b>\n"
                                 f"▶ <a href='{get_bot_info[1]}'><b>Скачать обновление</b></a>\n"
                                 f"➖➖➖➖➖➖➖➖➖➖\n"
                                 f"{update_discription}")
