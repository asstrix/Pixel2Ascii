from PIL import Image
from aiogram.filters import Command
from aiogram import Bot, Router, types, F
from aiogram.types import BufferedInputFile
from cfg import API_TOKEN
from keyboards import *
# from tools import image_to_ascii, pixelate_image, invert_colors, mirror_image, convert_to_heatmap, resize_for_sticker, get_random_joke, get_random_compliment, coin_toss
from tools import *
from states import EventState
from aiogram.fsm.context import FSMContext


bot = Bot(token=API_TOKEN)
router = Router()
user_states = {}


async def delete_previous_messages(message: types.Message, skip=0,  amount=1):
    """
    Deletes a specified range of previous messages in the chat.

    Args:
        message (types.Message): The current message object.
        skip (int): The number of messages to skip.
        amount (int): Total number of messages to delete (including skipped ones).
    """
    try:
        for i in range(message.message_id - skip, message.message_id - amount, -1):
            await bot.delete_message(message.chat.id, i)
    except Exception as e:
        pass


async def send_ascii(message: types.Message, ascii_set, state: FSMContext):
    """
    Converts the user's uploaded image to ASCII art using a specified set of ASCII symbols.

    Args:
        message (types.Message): The current message object.
        ascii_set (str): A string of ASCII characters to use for the conversion.
        state (FSMContext): Finite State Machine context to retrieve photo data.
    """
    await delete_previous_messages(message, 0, 2)
    data = await state.get_data()
    photo_id = data.get('photo_id')
    file_info = await bot.get_file(photo_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    ascii_art = image_to_ascii(downloaded_file, ascii_set)
    caption = "Here's your ascii image\!"
    await message.answer(f"```\n{ascii_art}\n```\n{caption}", parse_mode="MarkdownV2")


async def send_reflected(message: types.Message, reflection, state: FSMContext):
    """
    Reflects the user's uploaded image either horizontally or vertically.

    Args:
        message (types.Message): The current message object.
        reflection (str): Either 'horizontal' or 'vertical', indicating the reflection type.
        state (FSMContext): Finite State Machine context to retrieve photo data.
    """
    await delete_previous_messages(message, 0, 2)
    data = await state.get_data()
    photo_id = data.get('photo_id')
    file_info = await bot.get_file(photo_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    output_stream = mirror_image(downloaded_file, reflection)
    output_stream.seek(0)
    photo = BufferedInputFile(output_stream.read(), filename=f"{reflection}ly_reflected_image.png")
    await message.answer_photo(photo=photo, caption=f"Here's your {reflection}ly reflected image!")


@router.message(Command(commands=["start", 'help']))
async def send_welcome(message: types.Message):
    """
   Handles /start and /help commands to welcome the user.

   Args:
       message (types.Message): The current message object.
   """
    await delete_previous_messages(message, 0, 30)
    await message.answer(f"Hello {message.from_user.first_name}, welcome to Pixel2Ascii Bot!\n"
                         f"Send me an image, and I'll provide options for you!")


@router.message(F.text == 'Random Joke')
async def joke(message: types.Message):
    await delete_previous_messages(message, 0, 30)
    await message.answer(get_random_joke())


@router.message(F.text == 'Random Compliment')
async def joke(message: types.Message):
    await delete_previous_messages(message, 0, 30)
    await message.answer(get_random_compliment())


@router.message(F.text == 'Toss a coin')
async def toss_a_coin(message: types.Message):
    await delete_previous_messages(message, 0, 30)
    await message.answer(f'{coin_toss()}')


@router.message(F.photo)
async def send_welcome(message: types.Message, state: FSMContext):
    await delete_previous_messages(message, 1, 10)
    keyboard = get_options_keyboard()
    await message.reply("I got your photo! Please choose what you'd like to do with it.",
                        reply_markup=keyboard)
    await state.update_data(photo_id=message.photo[-1].file_id)


@router.callback_query(lambda c: c.data == 'pixelate')
async def pixelate_and_send(call: types.CallbackQuery, state: FSMContext):
    """
    Applies pixelation to the user's uploaded image and sends it back.

    Args:
        call (types.CallbackQuery): The callback query triggered by the user's button press.
        state (FSMContext): Finite State Machine context to retrieve photo data.
    """
    await delete_previous_messages(call.message, 0, 2)
    data = await state.get_data()
    photo_id = data.get('photo_id')
    file_info = await bot.get_file(photo_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    image = Image.open(downloaded_file)
    output_stream = pixelate_image(image, 20)
    output_stream.seek(0)
    photo = BufferedInputFile(output_stream.read(), filename="pixelated_image.png")
    await call.message.answer_photo(photo=photo, caption="Here's your pixelated image!")


@router.callback_query(lambda c: c.data == 'ascii')
async def pixelate_and_send(call: types.CallbackQuery):
    await delete_previous_messages(call.message, 0, 2)
    keyboard = get_ascii_options()
    await call.message.answer("What ascci symbols do you want to use?", reply_markup=keyboard)


@router.callback_query(lambda c: c.data == 'invert')
async def invert_image(call: types.CallbackQuery, state: FSMContext):
    """
    Inverts the colors of the user's uploaded image and sends it back.

    Args:
        call (types.CallbackQuery): The callback query triggered by the user's button press.
        state (FSMContext): Finite State Machine context to retrieve photo data.
    """
    await delete_previous_messages(call.message, 0, 2)
    data = await state.get_data()
    photo_id = data.get('photo_id')
    file_info = await bot.get_file(photo_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    output_stream = invert_colors(downloaded_file)
    output_stream.seek(0)
    photo = BufferedInputFile(output_stream.read(), filename="inverted_image.png")
    await call.message.answer_photo(photo=photo, caption="Here's your inverted image!")


@router.callback_query(lambda c: c.data == 'reflect')
async def reflect_image(call: types.CallbackQuery):
    """
    Prompts the user to select the type of reflection (horizontal or vertical).

    Args:
        call (types.CallbackQuery): The callback query triggered by the user's button press.
    """
    await delete_previous_messages(call.message, 0, 2)
    keyboard = get_reflect_options()
    await call.message.answer("How do you want to reflect the image?", reply_markup=keyboard)


@router.callback_query(lambda c: c.data == 'heatmap')
async def reflect_image(call: types.CallbackQuery, state: FSMContext):
    """
    Converts the user's uploaded image into a heatmap and sends it back.

    Args:
        call (types.CallbackQuery): The callback query triggered by the user's button press.
        state (FSMContext): Finite State Machine context to retrieve photo data.

    Workflow:
        1. Retrieves the user's uploaded image ID from the state.
        2. Downloads the image from Telegram servers.
        3. Applies a heatmap transformation to the image.
        4. Sends the transformed image back to the user.
    """
    await delete_previous_messages(call.message, 0, 2)
    data = await state.get_data()
    photo_id = data.get('photo_id')
    file_info = await bot.get_file(photo_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    output_stream = convert_to_heatmap(downloaded_file)
    output_stream.seek(0)
    photo = BufferedInputFile(output_stream.read(), filename="heatmap_image.png")
    await call.message.answer_photo(photo=photo, caption="Here's your heatmap image!")


@router.callback_query(lambda c: c.data == 'sticker')
async def reflect_image(call: types.CallbackQuery, state: FSMContext):
    await delete_previous_messages(call.message, 0, 2)
    data = await state.get_data()
    photo_id = data.get('photo_id')
    file_info = await bot.get_file(photo_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    output_stream = resize_for_sticker(downloaded_file)
    output_stream.seek(0)
    photo = BufferedInputFile(output_stream.read(), filename="sticker_image.png")
    await call.message.answer_photo(photo=photo, caption="Here's your sticker!")


@router.callback_query(lambda call: True)
async def callback_query(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'default':
        await send_ascii(call.message, None, state)
    elif call.data == 'custom':
        await delete_previous_messages(call.message, 0, 2)
        await call.message.answer(f"Please enter >= 10 ascii symbols:")
        await state.set_state(EventState.ascii)
    elif call.data == 'horizontal':
        await send_reflected(call.message, 'horizontal', state)
    elif call.data == 'vertical':
        await send_reflected(call.message, 'vertical', state)


@router.message(EventState.ascii)
async def custom(message: types.Message, state: FSMContext):
    await delete_previous_messages(message, 0, 2)
    symbols = message.text
    if all(ord(char) < 128 for char in symbols):
        await send_ascii(message, symbols, state)