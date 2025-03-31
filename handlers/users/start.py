from aiogram import types
from aiogram.dispatcher.dispatcher import Router
from aiogram.filters.command import CommandStart, CommandObject
from loader import user_db, bot
from utils.birthdate import return_birthdate


router = Router()


@router.message(CommandStart())
async def start_answer(message: types.Message, command: CommandObject) -> None:
    type_user = await user_db.return_user(user_id=message.from_user.id)
    user = message.from_user
    result_birthdate = await return_birthdate(user_id=user.id, bot=bot)
    if type_user:
        await message.answer('Hello world!')
    else:
        chat = await bot.get_chat(chat_id=user.id)
        await user_db.add_user(
            user_id=user.id,
            active_username=None if chat.active_usernames is None else f'{chat.active_usernames}',
            first_name=user.first_name,
            last_name=user.last_name,
            status="MEMBER",
            premium=user.is_premium,
            has_private_forwards=chat.has_private_forwards,
            birth_date=result_birthdate[0],
            birth_date_type=result_birthdate[1],
            language_code=user.language_code,
            user_start_date=message.date.date(),
            personal_chat_username=None if chat.personal_chat is None else chat.personal_chat.username,
            referal=command.args
        )
