import os
import requests
import json

with open("image_data.json", "r") as json_file:
    data = json.load(json_file)

# Directory where you want to store the downloaded content
download_dir = "downloads"

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

for entry in data:
    code = entry["code"]
    urls = entry["urls"]

    # Create a folder for the code if it doesn't exist
    code_folder = os.path.join(download_dir, str(code))
    if not os.path.exists(code_folder):
        os.makedirs(code_folder)

    # Download and save the content for each URL
    for url in urls:
        filename = os.path.basename(url)

        filepath = os.path.join(code_folder, filename)

        try:
            response = requests.get(url)

            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")
            else:
                print(
                    f"Failed to download: {filename} (Status code: {response.status_code})"
                )
        except Exception as e:
            print(f"Failed to download: {filename} ({str(e)})")

print("Download process completed.")
