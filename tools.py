from PIL import Image, ImageOps
import io, requests
from bs4 import BeautifulSoup

ASCII_CHARS = '@%#*+=-:. '


def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))


def grayify(image):
    return image.convert("L")


def image_to_ascii(image_stream, ascii_set=None, new_width=40):
    # Переводим в оттенки серого
    image = Image.open(image_stream).convert('L')

    # меняем размер сохраняя отношение сторон
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(
        aspect_ratio * new_width * 0.55)  # 0,55 так как буквы выше чем шире
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
    pixels = image.getdata()
    characters = ""
    if ascii_set:
        for pixel in pixels:
            characters += ascii_set[pixel * len(ASCII_CHARS) // 256]
    else:
        for pixel in pixels:
            characters += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
    return characters


# Огрубляем изображение
def pixelate_image(image, pixel_size):
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
    image = Image.open(image)
    image = ImageOps.invert(image)
    output_stream = io.BytesIO()
    image.save(output_stream, format="JPEG")
    return output_stream


def mirror_image(image, reflection):
    image = Image.open(image)
    if reflection == 'horizontal':
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif reflection == 'vertical':
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    output_stream = io.BytesIO()
    image.save(output_stream, format="JPEG")
    return output_stream


def convert_to_heatmap(image):
    image = Image.open(image).convert("L")
    image = ImageOps.colorize(image, black='blue', white='red')
    output_stream = io.BytesIO()
    image.save(output_stream, format="JPEG")
    return output_stream


def resize_for_sticker(image):
    image = Image.open(image)
    image.thumbnail((512, 512))
    output_stream = io.BytesIO()
    image.save(output_stream, format="PNG")
    return output_stream


def get_random_joke():
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