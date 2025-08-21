import asyncio
import logging
import sys
from os import getenv

from aiogram_max import Bot, Dispatcher, html
from aiogram_max.client.default import DefaultBotProperties
from aiogram_max.enums import ParseMode
from aiogram_max.filters import CommandStart, Command
from aiogram_max.types import Message, BotCommand

# Bot token can be obtained via https://max.ru/MasterBot
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("age"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/age` command
    """
    await message.answer(f"age!")


@dp.message(Command("help"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    await message.answer(f"help!")


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="age", description="Ваш возраст"),
            BotCommand(command="help", description="Помощь"),
        ]
    )


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(
        token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await set_default_commands(bot)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
