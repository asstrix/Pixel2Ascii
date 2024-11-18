from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_options_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Pixelate', callback_data='pixelate')
    builder.button(text='ASCII Art', callback_data='ascii')
    builder.button(text='Invert', callback_data='invert')
    builder.button(text='Reflect', callback_data='reflect')
    builder.button(text='Heatmap', callback_data='heatmap')
    builder.adjust(1)
    return builder.as_markup()


def get_ascii_options():
    builder = InlineKeyboardBuilder()
    builder.button(text='Default', callback_data='default')
    builder.button(text='Custom', callback_data='custom')
    builder.adjust(2)
    return builder.as_markup()


def get_reflect_options():
    builder = InlineKeyboardBuilder()
    builder.button(text='Horizontally', callback_data='horizontal')
    builder.button(text='Vertically', callback_data='vertical')
    builder.adjust(2)
    return builder.as_markup()