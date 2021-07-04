import logging
from aiogram.types import Update
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError, UserDeactivated,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter, CantParseEntities, MessageCantBeDeleted,
                                      TerminatedByOtherGetUpdates, BotBlocked)

from loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):
    if isinstance(exception, CantDemoteChatCreator):
        logging.exception(f"CantDemoteChatCreator: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, MessageNotModified):
        logging.exception(f"MessageNotModified: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, MessageCantBeDeleted):
        logging.exception(f"MessageCantBeDeleted: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.exception(f"MessageToDeleteNotFound: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.exception(f"MessageTextIsEmpty: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, UserDeactivated):
        logging.exception(f"UserDeactivated: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, Unauthorized):
        logging.exception(f"RetryAfter: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f"RetryAfter: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, RetryAfter):
        logging.exception(f"RetryAfter: {exception} \nUpdate: {update}")
        return True

    # Пользователь заблокировал бота
    if isinstance(exception, BotBlocked):
        # logging.exception(f"BotBlocked: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, TerminatedByOtherGetUpdates):
        logging.exception(f"TerminatedByOtherGetUpdates: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, CantParseEntities):
        logging.exception(f"CantParseEntities: {exception} \nUpdate: {update}")
        await Update.get_current().message.answer(f"❗ Ошибка HTML разметки\n"
                                                  f"▶ `{exception.args}`\n"
                                                  f"❕ Выполните заново действие с правильной разметкой тэгов.",
                                                  parse_mode="Markdown")
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f"TelegramAPIError: {exception} \nUpdate: {update}")
        return True

    logging.exception(f"Update: {update} \n{exception}")
