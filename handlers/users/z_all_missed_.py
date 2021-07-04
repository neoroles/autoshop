# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageCantBeDeleted

from keyboards.default import check_user_out_func
from loader import dp, bot
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT


# Обработка всех колбэков которые потеряли стейты после перезапуска скрипта
@dp.callback_query_handler(text="...", state="*")
async def processing_missed_callback(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT

# Обработка всех колбэков которые потеряли стейты после перезапуска скрипта
@dp.callback_query_handler(state="*")
async def processing_missed_callback(call: CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except MessageCantBeDeleted:
        pass
    await bot.send_message(call.from_user.id, "❌ <b>Данные не были найдены из-за перезапуска скрипта.\n"
                                              "♻ Выполните действие заново.</b>",
                           reply_markup=check_user_out_func(call.from_user.id))
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT


# Обработка всех неизвестных сообщений
@dp.message_handler()
async def processing_missed_messages(message: types.Message):
    await message.answer("♦ <b>Неизвестная команда.</b>\n"
                         "▶ Введите /start")
    # reply_markup=check_user_out_func(message.from_user.id)
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
