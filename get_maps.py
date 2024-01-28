import requests
import os

# Configuration
IMAGES_INFO = [
    {
        "url": "https://ims.gov.il/sites/default/files/ims_data/map_images/c3RainForecast/c3RainForecast.png",
        "header_file": "last_modified_c3.txt"
    },
    {
        "url": "https://ims.gov.il/sites/default/files/ims_data/map_images/ecRainForecast/ecRainForecast.png",
        "header_file": "last_modified_ec.txt"
    }
]
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Get Telegram token from environment variable
CHANNEL_ID = os.getenv('CHANNEL_ID')  # Get Channel ID from environment variable

def check_for_update(url, header_file):
    response = requests.head(url)
    last_modified = response.headers.get('Last-Modified')

    if not last_modified:
        print(f"Last-Modified header not found for {url}.")
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
    for image_info in IMAGES_INFO:
        if check_for_update(image_info['url'], image_info['header_file']):
            print(f"New content detected for {image_info['url']}! Downloading image.")
            image_data = requests.get(image_info['url']).content
            print(f"Sending image to Telegram from {image_info['url']}.")
            send_telegram_photo(TELEGRAM_TOKEN, CHANNEL_ID, image_data)
            print("Image sent successfully.")
        else:
            print(f"No new content found for {image_info['url']}.")

if __name__ == "__main__":
    main()
