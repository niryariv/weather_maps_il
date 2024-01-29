import requests
import os

# Configuration
IMAGES_INFO = [
    {
        "url": "https://ims.gov.il/sites/default/files/ims_data/map_images/c3RainForecast/c3RainForecast.png",
        "header_file": "data/last_modified_c3.txt"
    },
    {
        "url": "https://ims.gov.il/sites/default/files/ims_data/map_images/ecRainForecast/ecRainForecast.png",
        "header_file": "data/last_modified_ec.txt"
    }
]
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

def check_for_update(image_info):
    response = requests.head(image_info['url'])
    last_modified = response.headers.get('Last-Modified')

    if not last_modified:
        print(f"Last-Modified header not found for {image_info['url']}.")
        return True

    previous_last_modified = None
    if os.path.exists(image_info['header_file']):
        with open(image_info['header_file'], 'r') as file:
            previous_last_modified = file.read().strip()
        print(f'Previous Last-Modified for {image_info['url']}: {previous_last_modified}')

    if last_modified != previous_last_modified:
        print(f'Current Last-Modified for {image_info['url']}: {last_modified}')
        print('Writing last-modified to', image_info['header_file'])
        with open(image_info['header_file'], 'w') as file:
            file.write(last_modified)
        return True

    return False

def main():
    print("Script started. Checking for new content.")
    for image_info in IMAGES_INFO:
        if check_for_update(image_info):
            print(f"New content detected for {image_info['url']}! Downloading image.")
            image_data = download_image(image_info['url'])
            print(f"Sending image to Telegram from {image_info['url']}.")
            send_telegram_photo(TELEGRAM_TOKEN, CHANNEL_ID, image_data)
            print("Image sent successfully.")
        else:
            print(f"No new content found for {image_info['url']}.")

if __name__ == "__main__":
    main()
