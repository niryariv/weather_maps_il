import requests
import hashlib
import os

# Configuration
IMAGE_URL = "https://ims.gov.il/sites/default/files/ims_data/map_images/c3RainForecast/c3RainForecast.png"
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Get Telegram token from environment variable
CHANNEL_ID = os.getenv('CHANNEL_ID')  # Get Channel ID from environment variable
CHECKSUM_FILE = 'last_checksum.txt'

def download_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def get_checksum(data):
    return hashlib.md5(data).hexdigest()

def send_telegram_message(bot_token, chat_id, message):
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data=payload)
    response.raise_for_status()

def main():
    if not TELEGRAM_TOKEN or not CHANNEL_ID:
        raise ValueError("Telegram token and channel ID must be set as environment variables.")

    image_data = download_image(IMAGE_URL)
    new_checksum = get_checksum(image_data)

    if not os.path.exists(CHECKSUM_FILE) or open(CHECKSUM_FILE).read() != new_checksum:
        send_telegram_message(TELEGRAM_TOKEN, CHANNEL_ID, "New content detected!")
        with open(CHECKSUM_FILE, 'w') as file:
            file.write(new_checksum)

if __name__ == "__main__":
    main()

