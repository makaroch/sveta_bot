import asyncio
import re
from datetime import date

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter, KICKED
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated

from src.filters.chat_types import ChatTypesFilter
from src.database.dao import ClientDAO, MotivatingPhrasesDAO, PurposeCountdownDAO
from src.states.users import UserGetDate

user_private_router = Router()
user_private_router.message.filter(ChatTypesFilter(["private"]))


@user_private_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.chat.id
    user = await ClientDAO.find_one_or_none(tg_user_id=user_id)
    if not user:
        user_name = str(message.from_user.username) if message.from_user.username else "-1"
        await ClientDAO.create(tg_user_id=user_id, username=user_name)
    all_user_purpose_countdown = await PurposeCountdownDAO.find_all(tg_user_id=user_id)
    if all_user_purpose_countdown:
        targets = [
            purpose_countdown.__str__()
            for purpose_countdown in all_user_purpose_countdown
        ]
        targets = "\n".join(targets)
        await message.answer(f"Привет, {message.from_user.first_name}!\n"
                             f"У вас есть активные цели:\n{targets}\n")
        return
    await message.answer(
        text=f"Привет, {message.from_user.first_name}!\n"
             f"Похоже у вас нет активных целей.\n"
    )


@user_private_router.message(Command("add_target"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Введите название цели или напишите 'Отмена'")
    await state.set_state(UserGetDate.name)


@user_private_router.message(UserGetDate.name, F.text)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if message.text.lower() == "отмена":
        await message.answer("Добавление цели отменено")
        await state.clear()
        return
    await state.update_data(name=message.text)
    await message.answer("Введите дату в формате ДД.ММ.ГГГГ")
    await state.set_state(UserGetDate.date)


@user_private_router.message(UserGetDate.name)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Жду название цели для отмены добавления напиши 'Отмена'")


@user_private_router.message(UserGetDate.date, F.text)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if message.text.lower() == "отмена":
        await message.answer("Добавление цели отменено")
        await state.clear()
        return
    if re.match(r"^\d{2}\.\d{2}\.\d{4}$", message.text) is None:
        await message.answer("Неверный формат даты")
        return
    try:
        day, month, year = message.text.split(".")
        await state.update_data(date=date(int(year), int(month), int(day)))
    except ValueError:
        await message.answer("Неверный формат даты")
        return
    data = await state.get_data()
    data.update(tg_user_id=message.chat.id)
    await PurposeCountdownDAO.create(**data)
    await message.answer("Цель добавлена")
    await state.clear()

@user_private_router.message(UserGetDate.date)
async def command_start_handler(message: Message) -> None:
    await message.answer("Жду дату цели для отмены добавления напиши 'Отмена'")


@user_private_router.message(Command("off_alerts"))
async def echo_handler(message: Message) -> None:
    asyncio.create_task(ClientDAO.update(_id=message.chat.id, is_subscription=False))
    await message.answer(
        text=f"Отключил рассылку",
    )


@user_private_router.message(Command("on_alerts"))
async def echo_handler(message: Message) -> None:
    asyncio.create_task(ClientDAO.update(_id=message.chat.id, is_subscription=True))
    await message.answer(
        text=f"Включил рассылку",
    )

# @user_private_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
# async def user_blocked_bot(event: ChatMemberUpdated):
#     DB.unsubscribe_user(event.chat.id)
#
#
# @user_private_router.message(Command("about"))
# async def echo_handler(message: Message) -> None:
#     await message.answer(TEXT_ABOUT_MESSAGE[0])
#
#
# @user_private_router.message(F.text == "Как купить")
# async def keyboard_reaction(message: Message):
#     await message.answer(
#         """Чтобы осуществить покупку:
#
#         1. Нажмите в каталоге кнопку «Купить».
#         2. Напишите нашему менеджеру в чат, что хотите приобрести.
#         3. Договоритесь о визите в магазин или доставке.
#
#         Доставка по Москве осуществляется БЕСПЛАТНО!
#
#         ✅У нас только оригинальная продукция.
#         ✅Любые проверки перед покупкой.
#         ✅Trade-in ваших старых девайсов.""")
#
#
# @user_private_router.message(F.text == "Связаться с нами")
# async def keyboard_reaction(message: Message):
#     await message.answer(
#         text="Напишите менеджеру",
#         reply_markup=kupit_knopka()
#     )
#
#
# @user_private_router.callback_query(F.data.startswith("main_menu"))
# async def echo_handler(call: CallbackQuery) -> None:
#     await call.message.delete()
#     await call.message.answer(
#         text=f"Выберите категорию: ",
#         reply_markup=create_keyboard_type_product()
#     )
#
#
# @user_private_router.callback_query(F.data.startswith("type_pr"))
# async def echo_handler(call: CallbackQuery) -> None:
#     temp_lst = call.data.split("|")
#     type_id, type_name = temp_lst[1], temp_lst[2]
#     await call.answer()
#     await call.message.delete()
#     await call.message.answer(
#         text=f"Категория <b>{type_name}</b>",
#         reply_markup=create_keyboard_manufacturer(type_id, type_name)
#     )
#
#
# @user_private_router.callback_query(F.data.startswith("manuf"))
# async def echo_handler(call: CallbackQuery) -> None:
#     temp_lst = call.data.split("|")
#     m_id, type_id, type_name = temp_lst[1], temp_lst[2], temp_lst[3]
#     await call.answer()
#     await call.message.delete()
#     await call.message.answer(
#         text=f"Категория <b>{type_name}</b>\n",
#         reply_markup=create_keyboard_subtype(m_id, type_id, type_name)
#     )
#
#
# @user_private_router.callback_query(F.data.startswith("subt"))
# async def echo_handler(call: CallbackQuery) -> None:
#     temp_lst = call.data.split("|")
#     subtypes_id, m_id, type_id, type_name = temp_lst[1], temp_lst[2], temp_lst[3], temp_lst[4]
#     await call.answer()
#     await call.message.delete()
#     await call.message.answer(
#         text=f"Категория <b>{type_name}</b>\n"
#              f"{get_str_all_product_by_subtypes_id(int(subtypes_id))}",
#         reply_markup=final_keyboard(m_id, type_id, type_name)
#     )
#
#
# def get_str_all_product_by_subtypes_id(subtypes_id: int) -> str:
#     products = DB.get_all_product_by_subtypes_id(subtypes_id)
#     result = ""
#     for product in products:
#         result += f"* {product.name} - {product.price}\n\n"
#     return result
