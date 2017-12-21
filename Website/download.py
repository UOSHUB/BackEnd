import os, requests, re


# Store files and folders paths
requirements_file = "static/requirements.txt"
css_folder = "static/min/css/"
css_file = "requirements.css"
js_folder = "static/min/js/"
js_file = "requirements.js"
inner_download_folder = "static/fonts/"
# Regular expression and dictionary to extract and store inner URLs
inner_urls_regex = re.compile("url\(['\"]?((?:\.\./|http)[\w:=./-]+?)(?:[#|?].+?)?['\"]?\)")
inner_urls_folders = {}
# Variables to combine all files
css_files, js_files = "", ""

# Create requirements folders if they're not already
if not os.path.exists(css_folder):
    os.makedirs(css_folder)
if not os.path.exists(js_folder):
    os.makedirs(js_folder)


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
        css_files += inner_urls_regex.sub(get_inner_urls_handler(name[:-4], url), file)
    # If it's a JS file
    if name.endswith(".js"):
        # Just combine it
        js_files += file
# Store CSS & JS files in their folders as one file with "UTF-8" encoding
open(css_folder + css_file, "w", encoding="utf-8").write(css_files)
open(js_folder + js_file, "w", encoding="utf-8").write(js_files)

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
