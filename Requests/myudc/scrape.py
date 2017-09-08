

# Returns extracted data from cells as a dict
def __extract_data(cells, alt):
    doctor = cells[6].find("a")
    return dict(
        # Upper case and split time string e.g. ["8:00 AM", "9:15 AM"]
        time=cells[1].text.upper().split(" - "),
        # Store class days in chars, e.g. ['M', 'W']
        days=list(cells[2].text),
        # Remove extra parts from place details, e.g. ["M10", "TH007"]
        place=__remove_extras(cells[3].text.split()),
        # If doctor info is valid store doctor name and email, e.g. ["Name", "Email"]
        **({"doctor": [doctor.get("target"), doctor.get("href")[7:]]} if doctor is not None else alt))


# Takes place details array e.g. ["M10:", "Engineering", "(Men)", "TH007"] and remove extra details
def __remove_extras(place):
    # From building only get first letter and the digits after it, and from room remove any duplicates
    return [place[0][0] + __get_digits(place[0][1:]), __get_digits(place[-1].split('-')[-1])]


# Takes a string and returns all digits in it
def __get_digits(string):
    return ''.join([char for char in string if char.isdigit()])
