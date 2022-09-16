import asyncio
import logging

from aiogram import Bot, Dispatcher
# from aiogram.types import BotCommand
# from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
from app.buttons.commands import set_commands
from app.handlers.starting import register_handlers_starting
from app.handlers.ticket_buying import register_ticket_buying_handler

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error('Starting bot')

    config = load_config("config/bot.ini")
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_starting(dp)
    register_ticket_buying_handler(dp)

    await set_commands(bot)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
