# - *- coding: utf- 8 - *-
import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=0.5, key_prefix="antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()
#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
    async def message_throttled(self, message: types.Message, throttled: Throttled):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            await message.reply("<b>❗ Пожалуйста, не спамьте.\n Бот слит в @END_SOFT</b>")
        await asyncio.sleep(delta)
        thr = await dispatcher.check_key(key)

#СЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        if key:
            setattr(func, "throttling_key", key)
        return func

    return decorator
