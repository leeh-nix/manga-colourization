import requests
from bs4 import BeautifulSoup
import os
import dotenv
import json
import re

dotenv.load_dotenv()
COOKIE = os.getenv("COOKIE")
# print(COOKIE)

codes = [
    # Your codes
]
# f
result = []
# Function to clean up filenames
# def clean_filename(filename):
#     cleaned_filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
#     return cleaned_filename


headers = {
    "Cookie": f"{COOKIE}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
}
for code in codes:
    try:
        url = f"https://example.com/g/{code}/"
        print(url)
        response = requests.get(url, headers=headers)
        print("response", response)
        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img", class_="lazyload", attrs={"data-src": True})
        image_urls = []

        for img_tag in img_tags:
            src = img_tag["data-src"]

            # Check if a space exists in the src property
            if " " in src:
                url, size = src.split(" ", 1)
            else:
                url = src
                if "cover" in url or "thumb" in url:
                    continue
                regex = ":\\//t"
                substr = "://i"
                url = re.sub(regex, substr, url, 0, re.MULTILINE)
                regex = r"(t.jpg)"
                substr = ".jpg"
                url = re.sub(regex, substr, url, 0, re.MULTILINE)
            image_urls.append(url)

        code_data = {"code": code, "urls": image_urls}
        result.append(code_data)

    except Exception as e:
        print(f"img_tag Error: {e}")

print("result: ", result)
# Loading existing data
try:
    with open("image_data.json", "r") as json_file:
        existing_data = json.load(json_file)
except json.decoder.JSONDecodeError:
    existing_data = []

combined_data = existing_data + result

# Saving data
with open("image_data.json", "w") as json_file:
    json.dump(combined_data, json_file, indent=4)

print("JSON file saved with image data.")
