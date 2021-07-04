# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsPrivate, IsAdmin
from keyboards.default import payment_default, get_settings_func, get_functions_func, check_user_out_func, items_default
from loader import dp
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT

# Обработка кнопки "К платёжным системам"
@dp.message_handler(IsPrivate(), IsAdmin(), text="🔑 К платёжным системам ↩", state="*")
async def back_to_payments(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🔑 Настройка платежных системы.", reply_markup=payment_default())
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT

# Обработка кнопки "К настройкам"
@dp.message_handler(IsPrivate(), IsAdmin(), text="⚙ К настройкам ↩", state="*")
async def back_to_settings(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("⚙ Основные настройки бота.", reply_markup=get_settings_func())
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT

# Обработка кнопки "К общим функциям"
@dp.message_handler(IsPrivate(), IsAdmin(), text="🔆 К общим функциям", state="*")
async def back_to_functions(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🔆 Выберите нужную функцию.", reply_markup=get_functions_func(message.from_user.id))

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Обработка кнопки "К управлению товарами"
@dp.message_handler(IsPrivate(), IsAdmin(), text="🎁 К управлению товарами ↩", state="*")
async def back_to_edit_items(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🎁 Редактирование товаров, разделов и категорий 📜",
                         reply_markup=items_default)
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT

# Обработка кнопки "На главную"
@dp.message_handler(text="⬅ На главную", state="*")
async def back_to_main(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🔸 <b>Бот готов к использованию.</b>\n"
                         "🔸 Если не появились вспомогательные кнопки\n"
                         "▶ Введите /start",
                         reply_markup=check_user_out_func(message.from_user.id))
