# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Кнопки при поиске профиля через админ-меню
open_profile_inl = InlineKeyboardMarkup()
input_kb = InlineKeyboardButton(text="💵 Пополнить", callback_data="user_input")
mybuy_kb = InlineKeyboardButton(text="🛒 Мои покупки", callback_data="my_buy")
open_profile_inl.add(input_kb, mybuy_kb)
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Кнопка с возвратом к профилю
to_profile_inl = InlineKeyboardMarkup()
to_profile_inl.add(InlineKeyboardButton(text="📱 Профиль", callback_data="user_profile"))
