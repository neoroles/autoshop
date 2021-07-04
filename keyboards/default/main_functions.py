# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup


def get_functions_func(user_id):
    functions_default = ReplyKeyboardMarkup(resize_keyboard=True)
    functions_default.row("📱 Поиск профиля 🔍", "📃 Поиск чеков 🔍")
    functions_default.row("📢 Рассылка")
    functions_default.row("⬅ На главную")
    return functions_default

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
functions_back_default = ReplyKeyboardMarkup(resize_keyboard=True)
functions_back_default.row("🔆 К общим функциям")
