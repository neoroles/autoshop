# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import admins
from filters import IsPrivate
from keyboards.default import check_user_out_func, all_back_to_main_default
from keyboards.inline import *
from keyboards.inline.inline_page import *
from loader import dp, bot
from states.state_users import *
from utils.other_func import clear_firstname

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Разбив сообщения на несколько, чтобы не прилетало ограничение от ТГ
def split_messages(get_list, count):
    return [get_list[i:i + count] for i in range(0, len(get_list), count)]

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Обработка кнопки "Купить"
@dp.message_handler(IsPrivate(), text="🎁 Купить", state="*")
async def show_search(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    if get_settings[3] == "True" or str(message.from_user.id) in admins:
        get_categories = get_all_categoriesx()
        if len(get_categories) >= 1:
            get_kb = buy_item_open_category_ap(0)
            await message.answer("<b>🎁 Выберите нужный вам товар:</b>", reply_markup=get_kb)
        else:
            await message.answer("<b>🎁 Товары в данное время отсутствуют.</b>")
    else:
        await message.answer("<b>🔴 Покупки в боте временно отключены.</b>")

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Обработка кнопки "Профиль"
@dp.message_handler(IsPrivate(), text="📱 Профиль", state="*")
async def show_profile(message: types.Message, state: FSMContext):
    await state.finish()
    get_status_user = get_user_profile(message.from_user.id)
    await message.answer(get_status_user, reply_markup=open_profile_inl)

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Обработка кнопки "FAQ"
@dp.message_handler(IsPrivate(), text="ℹ FAQ", state="*")
async def show_my_deals(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    send_msg = get_settings[1]
    if "{username}" in send_msg:
        send_msg = send_msg.replace("{username}", f"<b>{message.from_user.username}</b>")
    if "{user_id}" in send_msg:
        send_msg = send_msg.replace("{user_id}", f"<b>{message.from_user.id}</b>")
    if "{firstname}" in send_msg:
        send_msg = send_msg.replace("{firstname}", f"<b>{clear_firstname(message.from_user.first_name)}</b>")
    await message.answer(send_msg, disable_web_page_preview=True)


# Обработка кнопки "Поддержка"
@dp.message_handler(IsPrivate(), text="📕 Поддержка", state="*")
async def show_contact(message: types.Message, state: FSMContext):
    await state.finish()
    get_settings = get_settingsx()
    await message.answer(get_settings[0], disable_web_page_preview=True)


# Обработка колбэка "Мои покупки"
@dp.callback_query_handler(text="my_buy")
async def show_referral(call: CallbackQuery):
    last_purchases = last_purchasesx(call.from_user.id)
    if len(last_purchases) >= 1:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        count_split = 0
        save_purchases = []
        for purchases in last_purchases:
            save_purchases.append(f"<b>📃 Чек:</b> <code>#{purchases[4]}</code>\n"
                                  f"▶ {purchases[9]} | {purchases[5]}шт | {purchases[6]}руб\n"
                                  f"🕜 {purchases[13]}\n"
                                  f"<code>{purchases[10]}</code>")
        await bot.send_message(call.from_user.id,
                               "<b>🛒 Последние 10 покупок</b>\n"
                               "➖➖➖➖➖➖➖➖➖➖➖➖➖")
        save_purchases.reverse()
        len_purchases = len(save_purchases)
        if len_purchases > 4:
            count_split = round(len_purchases / 4)
            count_split = len_purchases // count_split
        if count_split > 1:
            get_message = split_messages(save_purchases, count_split)
            for msg in get_message:
                send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(msg)
                await bot.send_message(call.from_user.id, send_message)
        else:
            send_message = "\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n".join(save_purchases)
            await bot.send_message(call.from_user.id, send_message)

        get_status_user = get_user_profile(call.from_user.id)
        await bot.send_message(call.from_user.id,
                               get_status_user,
                               reply_markup=open_profile_inl)
    else:
        await bot.answer_callback_query(call.id, "❗ У вас отсутствуют покупки")


################################################################################################
######################################### ПОКУПКА ТОВАРА #######################################
# Открытие категории для покупки#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
@dp.callback_query_handler(text_startswith="buy_open_category", state="*")
async def open_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    get_settings = get_settingsx()
    if get_settings[3] == "True" or str(call.from_user.id) in admins:
        category_id = int(call.data.split(":")[1])
        get_category = get_categoryx("*", category_id=category_id)
        get_positions = get_positionsx("*", category_id=category_id)

        get_kb = buy_item_item_position_ap(0, category_id)
        if len(get_positions) >= 1:
            await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                        call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=get_kb)
        else:
            await bot.answer_callback_query(call.id, f"❕ Товары в категории {get_category[2]} отсутствуют.")
    else:
        await bot.answer_callback_query(call.id, "🔴 Покупки в боте временно отключены.", True)


# Вернутсья к предыдущей категории при покупке
@dp.callback_query_handler(text_startswith="back_buy_item_to_category", state="*")
async def back_category_for_buy_item(call: CallbackQuery, state: FSMContext):
    get_kb = buy_item_open_category_ap(0)

    await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=get_kb)


# Следующая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_nextp", state="*")
async def buy_item_next_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    get_kb = buy_item_next_page_category_ap(remover)
    await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=get_kb)


# Предыдущая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_category_prevp", state="*")
async def buy_item_prev_page_category(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])

    get_kb = buy_item_previous_page_category_ap(remover)
    await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=get_kb)


# Следующая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_nextp", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    get_kb = item_buy_next_page_position_ap(remover, category_id)
    await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=get_kb)


# Предыдущая страница позиций при покупке
@dp.callback_query_handler(text_startswith="buy_position_prevp", state="*")
async def buy_item_prev_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    get_kb = item_buy_previous_page_position_ap(remover, category_id)
    await bot.edit_message_text("<b>🎁 Выберите нужный вам товар:</b>",
                                call.message.chat.id,
                                call.message.message_id,
                                reply_markup=get_kb)


# Возвращение к страницам позиций при покупке товара
@dp.callback_query_handler(text_startswith="back_buy_item_position", state="*")
async def buy_item_next_page_position(call: CallbackQuery, state: FSMContext):
    remover = int(call.data.split(":")[1])
    category_id = int(call.data.split(":")[2])

    get_kb = buy_item_item_position_ap(remover, category_id)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id,
                           "<b>🎁 Выберите нужный вам товар:</b>",
                           reply_markup=get_kb)


# Открытие позиции для покупки
@dp.callback_query_handler(text_startswith="buy_open_position", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    get_settings = get_settingsx()
    if get_settings[3] == "True" or str(call.from_user.id) in admins:
        position_id = int(call.data.split(":")[1])
        remover = int(call.data.split(":")[2])
        category_id = int(call.data.split(":")[3])

        get_position = get_positionx("*", position_id=position_id)
        get_category = get_categoryx("*", category_id=category_id)
        get_items = get_itemsx("*", position_id=position_id)

        send_msg = f"<b>🎁 Покупка товара:</b>\n" \
                   f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                   f"<b>📜 Категория:</b> <code>{get_category[2]}</code>\n" \
                   f"<b>🏷 Название:</b> <code>{get_position[2]}</code>\n" \
                   f"<b>💵 Стоимость:</b> <code>{get_position[3]}руб</code>\n" \
                   f"<b>📦 Количество:</b> <code>{len(get_items)}шт</code>\n" \
                   f"<b>📜 Описание:</b>\n" \
                   f"{get_position[4]}\n"
        if len(get_position[5]) >= 5:
            await bot.delete_message(call.from_user.id, call.message.message_id)
            await bot.send_photo(call.from_user.id,
                                 get_position[5],
                                 send_msg,
                                 reply_markup=open_item_func(position_id, remover, category_id))
        else:
            await bot.edit_message_text(send_msg,
                                        call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=open_item_func(position_id, remover, category_id))
    else:
        await bot.answer_callback_query(call.id, "🔴 Покупки в боте временно отключены.", True)


# Выбор кол-ва товаров для покупки
@dp.callback_query_handler(text_startswith="buy_this_item", state="*")
async def open_category_for_create_position(call: CallbackQuery, state: FSMContext):
    get_settings = get_settingsx()
    if get_settings[3] == "True" or str(call.from_user.id) in admins:
        position_id = int(call.data.split(":")[1])

        get_items = get_itemsx("*", position_id=position_id)
        get_position = get_positionx("*", position_id=position_id)
        get_user = get_userx(user_id=call.from_user.id)
        if len(get_items) >= 1:
            if int(get_user[4]) >= int(get_position[3]):
                async with state.proxy() as data:
                    data["here_cache_position_id"] = position_id
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                await StorageUsers.here_input_count_buy_item.set()
                await bot.send_message(call.from_user.id,
                                       f"📦 <b>Введите количество товаров для покупки</b>\n"
                                       f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                                       f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                       f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                       f"💵 Стоимость товара: <code>{get_position[3]}руб</code>\n"
                                       f"💳 Ваш баланс: <code>{get_user[4]}руб</code>\n",
                                       reply_markup=all_back_to_main_default)
            else:
                await bot.answer_callback_query(call.id, "❗ У вас недостаточно средств. Пополните баланс")
        else:
            await bot.answer_callback_query(call.id, "🎁 Товаров нет в наличии.")
    else:
        await bot.answer_callback_query(call.id, "🔴 Покупки в боте временно отключены.", True)

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
# Принятие кол-ва товаров для покупки
@dp.message_handler(IsPrivate(), state=StorageUsers.here_input_count_buy_item)
async def input_buy_count_item(message: types.Message, state: FSMContext):
    get_settings = get_settingsx()
    if get_settings[3] == "True" or str(message.from_user.id) in admins:
        async with state.proxy() as data:
            position_id = data["here_cache_position_id"]
        get_items = get_itemsx("*", position_id=position_id)
        get_position = get_positionx("*", position_id=position_id)
        get_user = get_userx(user_id=message.from_user.id)

        if message.text.isdigit():
            get_count = int(message.text)
            amount_pay = int(get_position[3]) * get_count
            if len(get_items) >= 1:
                if 1 <= get_count <= len(get_items):
                    if int(get_user[4]) >= amount_pay:
                        await state.finish()
                        delete_msg = await message.answer("<b>🎁 Товары подготовлены.</b>",
                                                          reply_markup=check_user_out_func(message.from_user.id))

                        await message.answer(f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
                                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                             f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                             f"💵 Стоимость товара: <code>{get_position[3]}руб</code>\n"
                                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                             f"▶ Количество товаров: <code>{get_count}шт</code>\n"
                                             f"💰 Сумма к покупке: <code>{amount_pay}руб</code>",
                                             reply_markup=confirm_buy_items(position_id, get_count,
                                                                            delete_msg.message_id))
                    else:
                        await message.answer(f"<b>❌ Недостаточно средств на счете.</b>\n"
                                             f"<b>📦 Введите количество товаров для покупки</b>\n"
                                             f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                             f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                                             f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                             f"💵 Стоимость товара: <code>{get_position[3]}руб</code>\n",
                                             reply_markup=all_back_to_main_default)
                else:
                    await message.answer(f"<b>❌ Неверное количество товаров.</b>\n"
                                         f"<b>📦 Введите количество товаров для покупки</b>\n"
                                         f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                         f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                                         f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                         f"💵 Стоимость товара: <code>{get_position[3]}руб</code>\n",
                                         reply_markup=all_back_to_main_default)
            else:
                await state.finish()
                await message.answer("<b>🎁 Товар который вы хотели купить, закончился</b>",
                                     reply_markup=check_user_out_func(message.from_user.id))
        else:
            await message.answer(f"<b>❌ Данные были введены неверно.</b>\n"
                                 f"<b>📦 Введите количество товаров для покупки</b>\n"
                                 f"▶ От <code>1</code> до <code>{len(get_items)}</code>\n"
                                 f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                 f"💳 Ваш баланс: <code>{get_user[4]}</code>\n"
                                 f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                 f"💵 Стоимость товара: <code>{get_position[3]}руб</code>\n",
                                 reply_markup=all_back_to_main_default)
    else:
        await message.answer("<b>🔴 Покупки в боте временно отключены.</b>")


# Отмена покупки товара
@dp.callback_query_handler(text_startswith="not_buy_items", state="*")
async def not_buy_this_item(call: CallbackQuery, state: FSMContext):
    message_id = call.data.split(":")[1]
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.delete_message(call.message.chat.id, message_id)
    await bot.send_message(call.from_user.id,
                           "<b>☑ Вы отменили покупку товаров.</b>",
                           reply_markup=check_user_out_func(call.from_user.id))


# Согласие на покупку товара
@dp.callback_query_handler(text_startswith="xbuy_item:", state="*")
async def yes_buy_this_item(call: CallbackQuery, state: FSMContext):
    get_settings = get_settingsx()
    if get_settings[3] == "True" or str(call.from_user.id) in admins:
        delete_msg = await bot.send_message(call.from_user.id,
                                            "<b>🔄 Ждите, товары подготавливаются</b>")
        position_id = int(call.data.split(":")[1])
        get_count = int(call.data.split(":")[2])
        message_id = int(call.data.split(":")[3])

        await bot.delete_message(call.message.chat.id, message_id)
        await bot.delete_message(call.message.chat.id, call.message.message_id)

        get_items = get_itemsx("*", position_id=position_id)
        get_position = get_positionx("*", position_id=position_id)
        get_user = get_userx(user_id=call.from_user.id)
        amount_pay = int(get_position[3]) * get_count

        if 1 <= int(get_count) <= len(get_items):
            if int(get_user[4]) >= amount_pay:

                save_items, send_count, split_len = buy_itemx(get_items, get_count)

                if split_len <= 50:
                    split_len = 70
                elif split_len <= 100:
                    split_len = 50
                elif split_len <= 150:
                    split_len = 30
                elif split_len <= 200:
                    split_len = 10
                else:
                    split_len = 3

                if get_count != send_count:
                    amount_pay = int(get_position[3]) * send_count
                    get_count = send_count

                random_number = [random.randint(100000000, 999999999)]
                passwd = list("ABCDEFGHIGKLMNOPQRSTUVYXWZ")
                random.shuffle(passwd)
                random_char = "".join([random.choice(passwd) for x in range(1)])
                receipt = random_char + str(random_number[0])
                buy_time = datetime.datetime.today().replace(microsecond=0)

                await bot.delete_message(call.from_user.id, delete_msg.message_id)
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT

                if len(save_items) <= split_len:
                    send_message = "\n".join(save_items)
                    await bot.send_message(call.from_user.id,
                                           f"<b>🎁 Ваши товары:</b>\n"
                                           f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                           f"{send_message}")
                else:
                    await bot.send_message(call.from_user.id,
                                           f"<b>🎁 Ваши товары:</b>\n"
                                           f"➖➖➖➖➖➖➖➖➖➖➖➖➖")

                    save_split_items = split_messages(save_items, split_len)
                    for item in save_split_items:
                        send_message = "\n".join(item)
                        await bot.send_message(call.from_user.id,
                                               send_message)
                save_items = "\n".join(save_items)

                add_purchasex(call.from_user.id, call.from_user.username, call.from_user.first_name,
                              receipt, get_count, amount_pay, get_position[3], get_position[1], get_position[2],
                              save_items, get_user[4], int(get_user[4]) - amount_pay, buy_time, int(time.time()))
                update_userx(call.from_user.id, balance=get_user[4] - amount_pay)
                await bot.send_message(call.from_user.id,
                                       f"<b>🎁 Вы успешно купили товар(ы) ✅</b>\n"
                                       f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                       f"📃 Чек: <code>#{receipt}</code>\n"
                                       f"🏷 Название товара: <code>{get_position[2]}</code>\n"
                                       f"📦 Куплено товаров: <code>{get_count}</code>\n"
                                       f"💵 Сумма покупки: <code>{amount_pay}руб</code>\n"
                                       f"👤 Покупатель: <a href='tg://user?id={get_user[1]}'>{get_user[3]}</a> <code>({get_user[1]})</code>\n"
                                       f"🕜 Дата покупки: <code>{buy_time}</code>",
                                       reply_markup=check_user_out_func(call.from_user.id))
            else:
                await bot.send_message(call.from_user.id, "<b>❗ На вашем счёте недостаточно средств</b>")
        else:
            await state.finish()
            await bot.send_message(call.from_user.id,
                                   "<b>🎁 Товар который вы хотели купить закончился или изменился.</b>",
                                   check_user_out_func(call.from_user.id))
    else:
        await bot.answer_callback_query(call.id, "🔴 Покупки в боте временно отключены.", True)
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT