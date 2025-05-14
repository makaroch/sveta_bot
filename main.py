import asyncio
import logging
import datetime as dt
from random import randint

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from scheduler.asyncio import Scheduler
import pytz

from src.settings import Settings
from src.handlers.routers import handlers_router
from src.database.dao import *

dp = Dispatcher()
bot = Bot(token=Settings.TG_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def spam_to_user():
    moscow_time_now = dt.datetime.now(pytz.timezone('Europe/Moscow'))
    start_spam_time = dt.datetime(
        year=dt.date.today().year, month=dt.date.today().month, day=dt.date.today().day, hour=8, minute=0
    )
    start_spam_time = pytz.timezone("Europe/Moscow").localize(start_spam_time)
    end_spam_time = dt.datetime(
        year=dt.date.today().year, month=dt.date.today().month, day=dt.date.today().day, hour=21, minute=30
    )
    end_spam_time = pytz.timezone("Europe/Moscow").localize(end_spam_time)

    if not start_spam_time <= moscow_time_now <= end_spam_time:
        return

    all_motivating_phrases: list[MotivatingPhrases] = await MotivatingPhrasesDAO.find_all()
    clients_targets: list[ClientsPurposeCountdown] = await ClientDAO.get_user_targets()

    for client_target in clients_targets:
        motivating_phrases = all_motivating_phrases[randint(0, len(all_motivating_phrases) - 1)]
        diff = str(client_target.date - dt.date.today()).split(" ")[0]
        text = (f"Цель: <b>{client_target.name}</b>\n"
                f"Осталось дней: <b>{diff}</b>\n"
                f"{motivating_phrases.phrase}")
        await bot.send_message(
            chat_id=client_target.tg_user_id,
            text=text
        )


async def main():
    loop = asyncio.get_running_loop()
    schedule = Scheduler(loop=loop)

    # schedule.daily(dt.time(hour=9, minute=30), spam_to_user)
    schedule.cyclic(dt.timedelta(hours=1), spam_to_user)

    dp.include_router(handlers_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

# start - старт
# add_target - добавить цель
# off_alerts - отключить рассылку
# on_alerts - включить рассылку
