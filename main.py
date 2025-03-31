import asyncio
import logging
import sys
from aiogram import types
from handlers.users import start
from loader import bot, OWNER_ID, dp, user_db
from bot_commands.set_commands import set_commands
from middlewares.throlling import SimpleThrottlingMiddleware


async def start_message():
    await bot.send_message(text="Bot ishga tushdi!", chat_id=OWNER_ID)


async def shutdown_message():
    await bot.send_document(document=types.FSInputFile(path='database/user/user.db'), chat_id=OWNER_ID)
    await bot.send_message(text="Bot to'xtadi!", chat_id=OWNER_ID)


async def main() -> None:
    dp.message.middleware(middleware=SimpleThrottlingMiddleware(rate_limit=0.5))
    await user_db.create_table_user()
    dp.startup.register(start_message)
    dp.shutdown.register(shutdown_message)
    dp.include_routers(start.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot=bot, owner_id=OWNER_ID)
    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())
