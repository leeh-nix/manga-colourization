# Batch download using threading

import os
import json
import threading
import requests
import dotenv

dotenv.load_dotenv()
COOKIE = os.getenv("COOKIE")

def download_urls(code, urls):
    # Create a folder for the code if it doesn't exist
    code_folder = os.path.join("downloads", str(code))
    if not os.path.exists(code_folder):
        os.makedirs(code_folder)

    # Download and save the content for each URL
    for url in urls:
        # Generate a filename based on the URL
        filename = os.path.basename(url)

        # Determine the full path for saving the file
        filepath = os.path.join(code_folder, filename)

        try:
            headers = {
                "Cookie": f"{COOKIE}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                # print(f"Downloaded: {filename}")
            else:
                print(
                    f"Failed to download: {filename} (Status code: {response.status_code})"
                )
        except Exception as e:
            print(f"Failed to download: {filename} ({str(e)})")


def parallel_download(data):
    threads = []

    # Loop through each entry in the data
    for entry in data:
        code = entry["code"]
        urls = entry["urls"]

        # Create a thread for each entry
        thread = threading.Thread(target=download_urls, args=(code, urls))
        threads.append(thread)

    # Start all the threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("Download process completed.")


if __name__ == "__main__":
    # Load the JSON data
    with open("image_data.json", "r") as json_file:
        data = json.load(json_file)

    # Ensure the download directory exists
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # Start parallel download
    parallel_download(data)
