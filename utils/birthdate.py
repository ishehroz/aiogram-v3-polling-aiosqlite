from aiogram import Bot


async def return_birthdate(user_id: int, bot: Bot) -> list:
    user = await bot.get_chat(chat_id=user_id)
    day, month, year = user.birthdate.day, user.birthdate.month, user.birthdate.year
    if all(i is None for i in (day, month, year)):
        return [None, None]
    elif all(i is not None for i in (day, month, year)):
        return [f"{year}-{month:02d}-{day:02d}", "full_date"]
    else:
        return [f"{month:02d}-{day:02d}", "month_day"]