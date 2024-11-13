from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext


def get_options_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Pixelate', callback_data="pixelate")
    builder.button(text='ASCII Art', callback_data="ascii")
    builder.adjust(2)
    return builder.as_markup()