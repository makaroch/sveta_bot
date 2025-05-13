from aiogram.fsm.state import State, StatesGroup


class UserGetDate(StatesGroup):
    name = State()
    date = State()
