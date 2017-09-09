from lxml.html import fromstring as __parse_html


# Scrapes Student Detail Schedule data from response
def schedule(response):
    data = {}
    # Loop through tables with datadisplaytable class
    for table in __parse_html(response).findall(".//table[@class='datadisplaytable']"):
        # If it's the heading table
        if table.find("caption").text != "Scheduled Meeting Times":
            # Split table caption into three parts ["name", "key", "section"]
            name, key, section = table.find("caption").text.split(" - ")
            # Store dictionary key as course number after removing spaces
            key = key.replace(' ', '')
            # Store all table cells into cells array
            cells = table.findall(".//td[@class='dddefault']")
            # Store course info so far
            course = {
                "name": name, "section": section,
                "crn": int(cells[1].text),
                "ch": int(cells[5].text.strip()[0])}
        else:
            rows = table.findall("tr")
            course.update(__extract_data(rows[1].findall("td[@class='dddefault']"), {"doctor": ["To Be Announced"] * 2}))
            if len(rows) > 2:
                course["lab"] = __extract_data(rows[2].findall("td[@class='dddefault']"), {})
            # If course key is new to schedule
            if data.get(key) is None:
                # Store the course with that key
                data[key] = course
            else:  # If the course already exists
                # Store it as a lab of the previous course
                data[key]["lab"] = course
    return data


# Returns extracted data from cells as a dict
def __extract_data(cells, lab=False):
    # Store doctor and location [building, room]
    location = cells[3].text.split()
    doctor = cells[6].find("a")
    # Upper case and split time string e.g. ["8:00 AM", "9:15 AM"]
    time = cells[1].text.upper().split(" - ")
    return dict({  # Return data dictionary
        "start": time[0], "end": time[1],
        # Store class days in chars, e.g. ["M", "W"]
        "days": cells[2].text.replace(" ", ""),
        # Remove extra parts from location details, e.g. ["M10", "TH007"]
        "building": location[0][0] + __get_digits(location[0][1:]),
        "room": __get_digits(location[-1].split("-")[-1])
        # Also add course doctor
    }, **({  # If doctor info is announced store his name and email
        "doctor": doctor.get("target"),
        "email": doctor.get("href")[7:]
    } if doctor is not None else {
        # If doctor info is not announced put TBA as his name and email
        "doctor": "To Be Announced",
        "email": "To Be Announced"
        # Unless it's a lab, in which case keep it empty
    } if not lab else {}))


# Takes a string and returns all digits in it
def __get_digits(string):
    return "".join([char for char in string if char.isdigit()])
