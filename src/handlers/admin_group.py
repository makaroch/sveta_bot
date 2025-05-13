from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from src.filters.chat_types import ChatTypesFilter

admin_group_router = Router()
admin_group_router.message.filter(ChatTypesFilter(["group", "supergroup"]))


@admin_group_router.message(Command('admin'))
async def command_start_handler(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    admin_lst = await bot.get_chat_administrators(chat_id)
    admin_lst = [
        item.user.id
        for item in admin_lst
        if item.status == "creator" or item.status == "administrator"
    ]
    bot.my_admins_lst = admin_lst
    if message.from_user.id in admin_lst:
        await message.delete()
