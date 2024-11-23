Pixel2Ascii Bot is a Telegram bot that provides several functionalities on an image, including converting images to:<br>
ASCII art<br>
heatmaps<br>
color inversion<br>
reflection<br>
pixelation<br>
Additionally, the bot can deliver random jokes, compliments, and simulate a coin toss.<br>

**Features**<br>
**Primary Commands**<br>
/start: Welcomes the user and provides a brief description of the bot's capabilities.<br>
/help: Repeats the description of the bot's capabilities.<br>
Image Processing<br>
Pixelate Image (Pixelate)<br>
Reduces the resolution of an image for a pixelated effect.<br>
Convert to ASCII (ASCII Art)<br>
Converts the uploaded image into ASCII art using a specified set of characters.<br>
Invert Colors (Invert)<br>
Inverts the colors of the image.<br>
Reflect Image (Reflect)<br>
Reflects the image horizontally or vertically.<br>
Generate Heatmap (Heatmap)<br>
Converts the image into a heatmap with a blue-to-red gradient.<br>
Create Sticker (Sticker)<br>
Resizes the image for creating Telegram stickers (512x512 resolution).<br>

**Additional Features**<br>
Random Joke (Random Joke)<br>
Fetches a random joke from bash.org.<br>
Random Compliment (Random Compliment)<br>
Generates a random compliment from a predefined list.<br>
Coin Toss (Toss a Coin)<br>
Simulates a coin toss, returning either "Heads" or "Tails".<br>

**Technologies Used**<br>
Python 3.10+<br>
Aiogram 3.x: Asynchronous library for Telegram Bot API.<br>
Pillow (PIL): Library for image processing.<br>
Requests: For web requests (e.g., fetching jokes).<br>
BeautifulSoup: For HTML parsing.<br>
FSM (Finite State Machine): For managing user states.<br>
Installation and Usage<br>
1. Install Dependencies<br>
Make sure you have Python 3.10+ installed.<br>
pip install -r requirements.txt<br>
2. Configure Environment<br>
Create a cfg.py file and add your bot token:<br>
API_TOKEN = "your-telegram-bot-token"<br>
3. Run the Bot<br>
Start the bot using the following command:<br>
python main.py<br><br>
