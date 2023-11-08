import requests
from bs4 import BeautifulSoup
import os
import re
import dotenv

dotenv.load_dotenv()
COOKIE = os.getenv("COOKIE")
regex = r"\d{6}"
url = "https://nhentai.net/g/443615/"
matches = re.findall(regex, url)
gallery_name = matches[0]

# Function to clean up filenames
def clean_filename(filename):
    # Remove invalid characters from the filename
    cleaned_filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    return cleaned_filename


try:
    headers = {
        "Cookie": "COOKIE",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    }

    response = requests.get(url, headers=headers)
    print("response", response)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        img_tags = soup.find_all("img", class_="lazyload", attrs={"data-src": True})
        # print("image-tag", img_tags)
    except Exception as e:
        print(f"img_tag Error: {e}")
    if img_tags:
        # Create a directory to save the images
        if not os.path.exists(gallery_name):
            os.mkdir(gallery_name)

        for img_tag in img_tags:
            src = img_tag["data-src"]

            # Check if a space exists in the src property
            if " " in src:
                url, size = src.split(" ", 1)
            else:
                url = src
                size = ""
            print("url:  ", url)
            # if "thumb" in url or "avatar" in url:
            #     continue
            image_data = requests.get(url).content

            # Clean up the filename
            filename = clean_filename(os.path.basename(url))

            with open(os.path.join(gallery_name, filename), "wb") as f:
                f.write(image_data)
except Exception as e:
    print(f"Error: {e}")
