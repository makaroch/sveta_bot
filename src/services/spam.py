from aiogram import Bot

from src.database.base_dao import DB


async def spamming_user(message_text: str, bot: Bot):
    users = DB.get_all_signed_users()
    for user in users:
        await bot.send_message(
            chat_id=user.tg_user_id,
            text=message_text
        )
