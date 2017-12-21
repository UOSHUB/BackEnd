import os, requests, re


# Store requirements paths
requirements_file = "static/requirements.txt"
download_folder = "static/libs/"
inner_download_folder = "static/fonts/"
# Regular expression and dictionary to extract and store inner URLs
inner_urls_regex = re.compile("url\(['\"]?((?:\.\./|http)[\w:=./-]+?)(?:[#|?].+?)?['\"]?\)")
inner_urls_folders = {}

# Create requirements folder if it's not already
if not os.path.exists(download_folder):
    os.makedirs(download_folder)


# Returns a function that handles matched inner URLs
def get_inner_urls_handler(folder_name, root_url):
    # Stores URL and modifies it
    def handler(regex):
        # Initialize a set for folder if it's not already
        if folder_name not in inner_urls_folders:
            inner_urls_folders[folder_name] = set()
        # Store matched inner URL
        match = regex.group(1)
        # Add full inner URL to its folder's set
        inner_urls_folders[folder_name].add(
            # Full URL is root URL plus the matched one
            root_url.rsplit("/", 2)[0] + match[2:]
            # If it starts with "../", otherwise keep it as is
            if match.startswith("../") else match
        )
        # Return CSS url() after modification
        return regex.group().replace(
            # Replace the online URL with the future local path
            match, "/" + inner_download_folder + folder_name + "/" + match.rsplit("/", 1)[-1]
        )
    return handler


# Loop through requirements
for requirement in open(requirements_file).read().splitlines():
    # Extract & store requirement name and URL
    name, url = requirement.split("==", 1)
    # Get requirement file
    file = requests.get(url).text
    # If it's a CSS file
    if name.endswith(".css"):
        # Check, store and replace any inner URL with it's future local path
        file = inner_urls_regex.sub(get_inner_urls_handler(name[:-4], url), file)
    # Store file in download folder with "UTF-8" encoding
    open(os.path.join(download_folder, name), "w", encoding="utf-8").write(file)

# Loop through CSS files with inner URLs
for inner_folder, inner_urls in inner_urls_folders.items():
    # Store file's downloads folder path
    sub_folder = os.path.join(inner_download_folder, inner_folder) + "/"
    # Create folder if it's not already
    if not os.path.exists(sub_folder):
        os.makedirs(sub_folder)
    # Loop through file's inner URLs
    for inner_url in inner_urls:
        # Download file from URL and write it to the folder
        open(sub_folder + inner_url.rsplit("/", 1)[-1], "wb").write(requests.get(inner_url).content)
