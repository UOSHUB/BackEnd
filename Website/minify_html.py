import os, re

# Patterns to match useless spaces and comments in HTML
double_spaces = re.compile(" {2,}")
tags_spaces = re.compile("({{) | (}})")
char_spaces = re.compile(" ?(\?|;|,|=|\*|\+|\||:|==|\|\||&&|!=) ")
attr_spaces = re.compile("\" ([a-z])")
comments = re.compile("<!-- .+? -->")

# Loop through all folders in Website/static/
for path, _, files in os.walk("static"):
    # Loop through all files
    for name in files:
        # Only apply to HTML files
        if name[-5:] == ".html":
            # Store current files full path
            file = os.path.join(path, name)
            # Open HTML file and remove all new lines
            html = open(file).read().replace("\n", "")
            # Apply all above cleaning patterns
            html = double_spaces.sub("", html)
            html = tags_spaces.sub(r"\1\2", html)
            html = char_spaces.sub(r"\1", html)
            html = attr_spaces.sub(r'"\1', html)
            html = comments.sub("", html)
            # Write the cleaned code in the same file
            open(file, "w").write(html)
