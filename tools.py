from PIL import Image, ImageOps
import io, requests, random
from bs4 import BeautifulSoup

ASCII_CHARS = '@%#*+=-:. '
COMPLIMENTS = [
    'У вас безупречные манеры.',
    'Мне нравится ваш стиль.',
    'Вы сильный.',
    'Это ваша фотография рядом со словом очаровательный" в словаре?',
    'Ваша доброта - бальзам для всех, кто с ней сталкивается.',
    'Вы смелая.',
    'Вы красивы внутри и снаружи.',
    'Вы смелы в своих убеждениях.',
    'Ты отличный слушатель.',
    'Ты был крут задолго до того, как хипстеры стали крутыми.',
    'То, что тебе не нравится в себе, делает тебя действительно интересным.',
    'Ты вдохновляешь.',
    'Ты такой внимательный.',
    'Когда ты принимаешь решение, ничто не стоит на твоем пути.',
    'Ты, кажется, действительно знаешь, кто ты.',
    'Вы умный человек.',
    'Ваш взгляд освежает.',
    'Ваша способность вспоминать случайные факты в нужный момент впечатляет.',
    'Когда ты говоришь: "Я так и собирался сделать", я полностью тебе верю.',
    'У тебя самые лучшие идеи.',
    'Ты всегда учишься чему-то новому и стараешься стать лучше. Это круто.',
    'Если бы кто-то создал интернет-мем о вас, в нем была бы безупречная грамматика.',
    'Вы можете пережить зомби-апокалипсис.',
    'Когда вы совершаете ошибку, вы ее исправляете.',
    'Вы отлично разбираетесь во всем.',
    'Ваш творческий потенциал кажется безграничным.',
    'У вас светлая голова.',
    'Все иногда падают духом только такие люди, как вы, снова поднимаются и продолжают идти вперед.'
]


def resize_image(image, new_width=100):
    """
    Resizes the image while maintaining its aspect ratio.

    Args:
        image (PIL.Image.Image): The input image to resize.
        new_width (int): The desired width of the resized image.

    Returns:
        PIL.Image.Image: The resized image with the new dimensions.
    """
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))


def grayify(image):
    """
    Converts the image to grayscale.

    Args:
        image (PIL.Image.Image): The input image.

    Returns:
        PIL.Image.Image: The grayscale version of the image.
    """
    return image.convert("L")


def image_to_ascii(image_stream, ascii_set=None, new_width=40):
    """
        Converts an image to ASCII art.

        Args:
            image_stream (io.BytesIO): A byte stream of the input image.
            ascii_set (str, optional): Custom ASCII characters for mapping brightness. Defaults to None.
            new_width (int): The desired width of the ASCII art.

        Returns:
            str: The resulting ASCII art as a string.
        """
    image = Image.open(image_stream).convert('L')

    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(
        aspect_ratio * new_width * 0.55)
    img_resized = image.resize((new_width, new_height))
    img_str = pixels_to_ascii(img_resized, ascii_set)
    img_width = img_resized.width

    max_characters = 4000 - (new_width + 1)
    max_rows = max_characters // (new_width + 1)

    ascii_art = ""
    for i in range(0, min(max_rows * img_width, len(img_str)), img_width):
        ascii_art += img_str[i:i + img_width] + "\n"

    return ascii_art


def pixels_to_ascii(image, ascii_set=None):
    """
    Maps pixel brightness values to ASCII characters.

    Args:
        image (PIL.Image.Image): The grayscale image.
        ascii_set (str, optional): Custom ASCII characters for mapping brightness. Defaults to None.

    Returns:
        str: A string representation of the image using ASCII characters.
    """
    pixels = image.getdata()
    characters = ""
    if ascii_set:
        for pixel in pixels:
            characters += ascii_set[pixel * len(ASCII_CHARS) // 256]
    else:
        for pixel in pixels:
            characters += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
    return characters


def pixelate_image(image, pixel_size):
    """
   Applies a pixelation effect to the image.

   Args:
       image (PIL.Image.Image): The input image.
       pixel_size (int): The size of the pixels for the effect.

   Returns:
       io.BytesIO: A byte stream of the pixelated image in JPEG format.
   """
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    output_stream = io.BytesIO()
    image.save(output_stream, format="JPEG")
    return output_stream


def invert_colors(image):
    """
    Inverts the colors of the image.

    Args:
        image (io.BytesIO): A byte stream of the input image.

    Returns:
        io.BytesIO: A byte stream of the color-inverted image in JPEG format.
    """
    image = Image.open(image)
    image = ImageOps.invert(image)
    output_stream = io.BytesIO()
    image.save(output_stream, format="JPEG")
    return output_stream


def mirror_image(image, reflection):
    """
   Mirrors the image horizontally or vertically.

   Args:
       image (io.BytesIO): A byte stream of the input image.
       reflection (str): Either 'horizontal' or 'vertical', indicating the reflection type.

   Returns:
       io.BytesIO: A byte stream of the mirrored image in JPEG format.
   """
    image = Image.open(image)
    if reflection == 'horizontal':
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif reflection == 'vertical':
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    output_stream = io.BytesIO()
    image.save(output_stream, format="JPEG")
    return output_stream


def convert_to_heatmap(image):
    """
   Converts the grayscale image to a heatmap using a blue-to-red color gradient.

   Args:
       image (io.BytesIO): A byte stream of the grayscale input image.

   Returns:
       io.BytesIO: A byte stream of the heatmap image in JPEG format.
   """
    image = Image.open(image).convert("L")
    image = ImageOps.colorize(image, black='blue', white='red')
    output_stream = io.BytesIO()
    image.save(output_stream, format="JPEG")
    return output_stream


def resize_for_sticker(image):
    """
    Resizes the image to fit within 512x512 pixels for Telegram stickers.

    Args:
        image (io.BytesIO): A byte stream of the input image.

    Returns:
        io.BytesIO: A byte stream of the resized image in PNG format.
    """
    image = Image.open(image)
    image.thumbnail((512, 512))
    output_stream = io.BytesIO()
    image.save(output_stream, format="PNG")
    return output_stream


def get_random_joke():
    """
    Fetches a random joke from a website.

    Returns:
        str: The text of the joke, or an error message if the request fails.
    """
    url = "https://башорг.рф/random"
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        joke = soup.find('div', class_='quote__body')
        if joke:
            return joke.get_text(separator='\n').strip()
    except Exception as e:
        return e


def get_random_compliment():
    """
    Returns a random compliment from a predefined list.

    Returns:
        str: A random compliment.
    """
    return random.choice(COMPLIMENTS)


def coin_toss():
    """
    Simulates a coin toss.

    Returns:
        str: Either 'Орёл' or 'Решка'.
    """
    return random.choice(['Орёл', 'Решка'])
