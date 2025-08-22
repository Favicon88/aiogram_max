import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict

from aiogram_max import Bot, Dispatcher, F, Router, html
from aiogram_max.client.default import DefaultBotProperties
from aiogram_max.enums import ParseMode
from aiogram_max.filters import Command, CommandStart
from aiogram_max.fsm.context import FSMContext
from aiogram_max.fsm.state import State, StatesGroup
from aiogram_max.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

TOKEN = getenv("BOT_TOKEN")

form_router = Router()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Hi there! What's your name?",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Yes", callback_data="start"),
                ]
            ],
        ),
    )


@form_router.callback_query(F.data == "start")
# @form_router.callback_query()
async def demo_callback(callback_query: CallbackQuery):
    await callback_query.answer("123", cache_time=0)


async def main():
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(
        token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    dp.include_router(form_router)

    # Start event dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
