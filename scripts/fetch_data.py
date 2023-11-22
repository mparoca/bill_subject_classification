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

# Unzipping the file and flattening the directory structure
zip_file_path = os.path.join(raw_data_dir, 'NY_2023-2024.zip')
print("Unzipping the file...")

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Iterate over each file in the ZIP
    for file_info in zip_ref.infolist():
        # Extract only the name of the file (discard the folder structure)
        filename = os.path.basename(file_info.filename)
        # Check if it's not a directory
        if filename:
            # Extract the file to the desired directory
            source = zip_ref.open(file_info.filename)
            target = open(os.path.join(raw_data_dir, filename), "wb")
            with source, target:
                target.write(source.read())

print("Unzipping completed.")

