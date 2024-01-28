import requests
import os

# Configuration
IMAGE_URL = "https://ims.gov.il/sites/default/files/ims_data/map_images/c3RainForecast/c3RainForecast.png"
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Get Telegram token from environment variable
CHANNEL_ID = os.getenv('CHANNEL_ID')  # Get Channel ID from environment variable
HEADER_FILE = 'last_modified.txt'

def check_for_update(url, header_file):
    response = requests.head(url)
    last_modified = response.headers.get('Last-Modified')

    if not last_modified:
        print("Last-Modified header not found.")
        return True

    if not os.path.exists(header_file) or open(header_file).read().strip() != last_modified:
        with open(header_file, 'w') as file:
            file.write(last_modified)
        return True

    return False

def send_telegram_photo(bot_token, chat_id, photo_data):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {'photo': ('image.png', photo_data)}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    response.raise_for_status()

def main():
    print("Script started. Checking for new content.")
    if check_for_update(IMAGE_URL, HEADER_FILE):
        print("New content detected! Downloading image.")
        image_data = requests.get(IMAGE_URL).content
        print("Sending image to Telegram.")
        send_telegram_photo(TELEGRAM_TOKEN, CHANNEL_ID, image_data)
        print("Image sent successfully.")
    else:
        print("No new content found.")

if __name__ == "__main__":
    main()
