# - *- coding: utf- 8 - *-

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from filters import IsPrivate, IsWork, IsUser
from keyboards.default import check_user_out_func
from loader import dp, bot
from utils.db_api.sqlite import *
from utils.other_func import clear_firstname
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
@dp.message_handler(IsWork())
async def send_work_message(message: types.Message):
    await message.answer("<b>🔴 Бот находится на технических работах.</b>")


@dp.callback_query_handler(IsWork())
async def send_work_message(call: CallbackQuery):
    await call.answer("🔴 Бот находится на технических работах.")
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT

# Обработка кнопки "На главную" и команды "/start"
@dp.message_handler(IsPrivate(), text="⬅ На главную", state="*")
@dp.message_handler(IsPrivate(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    first_name = clear_firstname(message.from_user.first_name)
    get_user_id = get_userx(user_id=message.from_user.id)
    if get_user_id is None:
        if message.from_user.username is not None:
            get_user_login = get_userx(user_login=message.from_user.username)
            if get_user_login is None:
                add_userx(message.from_user.id, message.from_user.username.lower(), first_name,
                          0, 0, datetime.datetime.today().replace(microsecond=0))
            else:
                delete_userx(user_login=message.from_user.username)
                add_userx(message.from_user.id, message.from_user.username.lower(), first_name,
                          0, 0, datetime.datetime.today().replace(microsecond=0))
        else:
            add_userx(message.from_user.id, message.from_user.username, first_name,
                      0, 0, datetime.datetime.today().replace(microsecond=0))
    else:
        if first_name != get_user_id[3]:
            update_userx(get_user_id[1], user_name=first_name)
        if message.from_user.username is not None:
            if message.from_user.username.lower() != get_user_id[2]:
                update_userx(get_user_id[1], user_login=message.from_user.username.lower())

    await message.answer("<b>🔸 Бот готов к использованию.</b>\n"
                         "🔸 Если не появились вспомогательные кнопки\n"
                         "▶ Введите /start",
                         reply_markup=check_user_out_func(message.from_user.id))
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT

@dp.message_handler(IsUser())
@dp.callback_query_handler(IsUser())
async def send_user_message(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "<b>❗ Ваш профиль не был найден.</b>\n"
                           "▶ Введите /start")
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT