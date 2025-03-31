from environs import Env
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from database.user.aiosqilte import DatabaseUser

env = Env()
env.read_env()
BOT_TOKEN = env.str('BOT_TOKEN')
OWNER_ID = env.int('OWNER_ID')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=MemoryStorage())
user_db = DatabaseUser(path_to_db="database/user/user.db")