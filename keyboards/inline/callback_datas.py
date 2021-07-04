# - *- coding: utf- 8 - *-
from aiogram.utils.callback_data import CallbackData

user_purchases_cd=CallbackData("show_purchases", "user_id")

user_add_balance_cd=CallbackData("add_balance", "user_id")

user_set_balance_cd=CallbackData("set_balance", "user_id")

user_send_message_cd=CallbackData("send_message", "user_id")
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT