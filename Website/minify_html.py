import os, re

# Patterns to match useless spaces and comments in HTML
new_lines = re.compile("(.)\n(.)", re.DOTALL)
double_spaces = re.compile(" {2,}")
tags_spaces = re.compile("({{) | (}})")
char_spaces = re.compile(" ?(\?|;|,|=|\*|\+|\||:|==|\|\||&&|!=) ")
attr_spaces = re.compile("\" ([a-z])")
comments = re.compile("<!-- .+? -->")


# Replaces new line characters
def replace_new_lines(match):
    before, after = match.groups()
    # If surrounding characters are letters
    if before.isalnum() and after.isalpha():
        # Place a space between them
        return before + " " + after
    # Otherwise, concatenate them directly
    return (before + after).replace("\n", "")


# Loop through all folders in Website/static/
for path, _, files in os.walk("static"):
    # Loop through all files
    for name in files:
        # Only apply to HTML files
        if name[-5:] == ".html":
            # Store current files full path
            file = os.path.join(path, name)
            # Open HTML file and read it
            html = open(file).read().strip()
            # Apply all above cleaning patterns
            html = double_spaces.sub("", html)
            html = new_lines.sub(replace_new_lines, html)
            html = tags_spaces.sub(r"\1\2", html)
            html = char_spaces.sub(r"\1", html)
            html = attr_spaces.sub(r'"\1', html)
            html = comments.sub("", html)
            # Write the cleaned code in the same file
            open(file, "w").write(html)
