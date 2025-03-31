import time
from aiogram import BaseMiddleware
from aiogram.types import Message

class SimpleThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit=1, block_time=3):
        self.rate_limit = rate_limit  # ❗ Har bir foydalanuvchi uchun vaqt oralig‘i (sekund)
        self.block_time = block_time  # ❗ Juda ko‘p yuborsa, qancha vaqt bloklanadi
        self.users = {}  # ❗ Foydalanuvchilarning so‘nggi xabarlari saqlanadi

    async def __call__(self, handler, event: Message, data):
        if event.chat.type != "private":  # ❗ Faqat shaxsiy chatlar uchun ishlaydi
            return await handler(event, data)

        user_id = event.from_user.id
        now = time.time()

        last_call, blocked_until = self.users.get(user_id, (0, 0))

        if now < blocked_until:
            await event.answer(f"🚫 Too many requests! Try again in {int(blocked_until - now)} sec.")
            return

        if now - last_call < self.rate_limit:
            self.users[user_id] = (last_call, now + self.block_time)  # ⛔ Bloklash
            await event.answer(f"🚫 Slow down! Wait {self.block_time} sec.")
            return

        self.users[user_id] = (now, 0)  # ✅ Xabar yuborishga ruxsat
        return await handler(event, data)


