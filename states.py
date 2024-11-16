from aiogram.fsm.state import State, StatesGroup


class EventState(StatesGroup):
    ascii = State()
    reflect = State()