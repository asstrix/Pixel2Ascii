from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_options_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Pixelate', callback_data="pixelate")
    builder.button(text='ASCII Art', callback_data="ascii")
    builder.adjust(2)
    return builder.as_markup()


def get_ascii_options():
    builder = InlineKeyboardBuilder()
    builder.button(text='Default', callback_data="default")
    builder.button(text='Custom', callback_data="custom")
    builder.adjust(2)
    return builder.as_markup()