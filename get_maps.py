import requests
import os
import json

# Configuration
IMAGE_URLS = [
    "https://ims.gov.il/sites/default/files/ims_data/map_images/c3RainForecast/c3RainForecast.png",
    "https://ims.gov.il/sites/default/files/ims_data/map_images/ecRainForecast/ecRainForecast.png"
]
LAST_MODIFIED_FILE = "last_modified_data.json"
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

def download_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def send_telegram_photo(bot_token, chat_id, photo_data):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {'photo': ('image.png', photo_data)}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    response.raise_for_status()

def load_last_modified_data():
    if os.path.exists(LAST_MODIFIED_FILE):
        with open(LAST_MODIFIED_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_last_modified_data(data):
    with open(LAST_MODIFIED_FILE, 'w') as file:
        json.dump(data, file)

def main():
    print("Script started. Checking for new content.")
    last_modified_data = load_last_modified_data()

    for url in IMAGE_URLS:
        response = requests.head(url)
        last_modified = response.headers.get('Last-Modified')
        previous_last_modified = last_modified_data.get(url)

        if not last_modified or last_modified != previous_last_modified:
            print(f"New content detected for {url}! Downloading image.")
            image_data = download_image(url)
            send_telegram_photo(TELEGRAM_TOKEN, CHANNEL_ID, image_data)
            print("Image sent successfully.")
            last_modified_data[url] = last_modified

    save_last_modified_data(last_modified_data)

if __name__ == "__main__":
    main()
