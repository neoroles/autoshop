# - *- coding: utf- 8 - *-
async def on_startup(dp):
    import asyncio
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
    from utils.other_func import on_startup_notify, update_last_profit, check_update_bot, update_profit
    from utils.set_bot_commands import set_default_commands
    from utils.db_api.sqlite import create_bdx

    await set_default_commands(dp)
    await on_startup_notify(dp)
    create_bdx()
    update_profit()
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
    print("~~~~~ Bot was started ~~~~~")
    asyncio.create_task(update_last_profit())
    asyncio.create_task(check_update_bot())


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
    import filters
    import middlewares
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
    filters.setup(dp)
    middlewares.setup(dp)

    executor.start_polling(dp, on_startup=on_startup)
