from aiogram import types

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота 🔥")
    ])
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT