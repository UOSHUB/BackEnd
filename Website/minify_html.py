from os.path import join
from os import walk
import re

# String formatter for cards and static html files
def cards(*array):
    return list(map(lambda s: f"cards/{s}", array))

def static(*array):
    return list(map(lambda s: f"/static/{s}.html", array))


# ng-template script tag wrapper
template = '\n<script type="text/ng-template" id="{}">{}</script>'
# Pages which need html appended to it
appends = {
    "welcome.html": static("login"),
    "dashboard.html": static("account", *cards("deadlines", "emails", "finals", "holds", "updates")),
    "courses.html": static(*cards("documents", "info", "mailto"))
}

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
for path, _, files in walk("static"):
    # Loop through all files
    for name in files:
        # Only apply to HTML files
        if name.endswith(".html"):
            # Store current files full path
            file = join(path, name)
            # Open HTML file and read it
            html = open(file).read()
            # If page needs other html files appended
            if any(join(path[7:], name).startswith(append) for append in appends.keys()):
                # Loop through needed files
                for to_append in appends[name]:
                    # Append needed file to html code
                    html += template.format(to_append, open("." + to_append).read())
            # Apply all above cleaning patterns
            html = double_spaces.sub("", html.strip())
            html = new_lines.sub(replace_new_lines, html)
            html = tags_spaces.sub(r"\1\2", html)
            html = char_spaces.sub(r"\1", html)
            html = attr_spaces.sub(r'"\1', html)
            html = comments.sub("", html)
            # Write the cleaned code in the same file
            open(file, "w").write(html)
