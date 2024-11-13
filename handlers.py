import io
from aiogram.filters import Command
from aiogram import Bot, Router, types, F
from aiogram.types import BufferedInputFile
from cfg import API_TOKEN
from keyboards import *
from tools import image_to_ascii, pixelate_image
from PIL import Image


bot = Bot(token=API_TOKEN)
router = Router()
user_states = {}


async def delete_previous_messages(message: types.Message, skip=0,  amount=1):
    try:
        for i in range(message.message_id - skip, message.message_id - amount, -1):
            await bot.delete_message(message.chat.id, i)
    except Exception as e:
        pass


@router.message(Command(commands=["start", 'help']))
async def send_welcome(message: types.Message):
    await delete_previous_messages(message,0, 30)
    await message.answer(f"Hello {message.from_user.first_name}, welcome to Pixel2Ascii Bot!\n"
                         f"Send me an image, and I'll provide options for you!")


@router.message(F.photo)
async def send_welcome(message: types.Message):
    await delete_previous_messages(message, 1, 10)
    keyboard = get_options_keyboard()
    await message.reply("I got your photo! Please choose what you'd like to do with it.",
                        reply_markup=keyboard)
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id}


@router.callback_query(lambda c: c.data == 'pixelate')
async def pixelate_and_send(call: types.CallbackQuery):
    await call.message.answer("Pixelating your image...")
    photo_id = user_states.get(call.message.chat.id, {}).get('photo')
    file_info = await bot.get_file(photo_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    image = Image.open(downloaded_file)
    output_stream = pixelate_image(image, 20)
    output_stream.seek(0)
    photo = BufferedInputFile(output_stream.read(), filename="pixelated_image.png")
    await call.message.answer_photo(photo=photo, caption="Here's your pixelated image!")


@router.callback_query(lambda c: c.data == 'ascii')
async def pixelate_and_send(call: types.CallbackQuery):
    await call.message.answer("Converting your image to ASCII art...")
    photo_id = user_states.get(call.message.chat.id, {}).get('photo')
    file_info = await bot.get_file(photo_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    ascii_art = image_to_ascii(downloaded_file)
    await call.message.answer(f"```\n{ascii_art}\n```", parse_mode="MarkdownV2")