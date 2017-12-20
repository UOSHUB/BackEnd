import os, requests


# Store requirements paths
requirements_file = "static/requirements.txt"
download_folder = "static/requirements/"


# Create requirements folder if not already
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Loop through requirements
for requirement in open(requirements_file).read().splitlines():
    # Extract & store requirement name and URL
    name, url = requirement.split("==", 1)
    # Get requirement file
    file = requests.get(url).text
    # Store file in download folder with "UTF-8" encoding
    open(os.path.join(download_folder, name), "w", encoding="utf-8").write(file)
