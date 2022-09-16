from aiogram.types import BotCommand

async def set_commands(bot):
    commands = [
        BotCommand(command="/info", description="Посмотреть актуальную информацию."),
        BotCommand(command="/ticket", description="Купить билет!"),
        BotCommand(command="/merch", description="Купить мерч!")
    ]
    await bot.set_my_commands(commands)