import os
import requests
import zipfile

# Create data/raw directory
raw_data_dir = 'data/raw'
os.makedirs(raw_data_dir, exist_ok=True)

# Download the 2023-2024 NYStateData
url = 'https://data.openstates.org/json/latest/NY_2023-2024_json_5ak18hjB9GhV4bBh3GAFmy.zip'
zip_file_path = os.path.join(raw_data_dir, 'NY_2023-2024.zip')

print("Downloading file...")
response = requests.get(url)
with open(zip_file_path, 'wb') as file:
    file.write(response.content)
print("Download completed.")

# Unzip the file
print("Unzipping the file...")
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(raw_data_dir)
print("Unzipping completed.")

