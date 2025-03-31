from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats


async def set_commands(bot: Bot, owner_id: int) -> None:
    private_chat_commands = [
        BotCommand(command="/start", description="Boshlash!"),
        BotCommand(command='/help', description="Yordam")
    ]
    private_chat_commands_scope = private_chat_commands + [
        BotCommand(command='/admin', description='Admin panel')

    ]
    await bot.set_my_commands(commands=private_chat_commands, scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private_chat_commands_scope, scope=BotCommandScopeChat(chat_id=owner_id))
