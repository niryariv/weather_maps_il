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

def send_telegram_photo(bot_token, chat_id, photo_data):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {'photo': photo_data}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    response.raise_for_status()

def main():
    image_data = download_image(IMAGE_URL)
    new_checksum = get_checksum(image_data)

    if not os.path.exists(CHECKSUM_FILE) or open(CHECKSUM_FILE).read() != new_checksum:
        send_telegram_photo(TELEGRAM_TOKEN, CHANNEL_ID, image_data)
        with open(CHECKSUM_FILE, 'w') as file:
            file.write(new_checksum)

if __name__ == "__main__":
    main()
