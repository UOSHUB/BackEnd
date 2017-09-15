from lxml.html import fromstring as __parse

seasons_codes = {"Fall": "10", "Spring": "20", "Summer": "30"}


# Returns term code from string of "TERM YYYY-YYYY" format
def __get_term_code(term):
    # Separate season from year and store both
    season, year = term.split(" ", 1)
    # Return the first year among the two plus season's code
    return year.split("-")[0] + seasons_codes[season]


# Scrapes all terms that student was registered in
def registered_terms(page):
    return {
        # Return a dictionary that contains {term code: term name} pairs
        __get_term_code(term.text): term.text
        # Loop through tags which contain term name
        for term in __parse(page).findall(".//span[@class='fieldOrangetextbold']")
    }


# Scrapes "Student Detail Schedule" data from page
def schedule(page):
    data = {}
    # Store all tables with "datadisplaytable" class
    tables = iter(__parse(page).findall(".//table[@class='datadisplaytable']"))
    # Loop through every two tables as one (head and body)
    for head, body in zip(tables, tables):
        # Split table caption into three parts ["title", "key", "section"]
        title, key, section = head.find("caption").text.split(" - ")
        # Remove spaces from course key
        key = key.replace(" ", "")
        # Store all table head cells and body rows into arrays
        cells, rows = head.findall(".//td"), body.findall("tr")
        # Store course info so far
        course = {
            "title": title,
            "section": section,
            "crn": cells[1].text,
            "ch": cells[5].text.strip()[0]
        }
        # Add extra details to course if it's not the Junior/Senior Project
        if not ("Junior" in title or "Senior" in title):
            # Extract more course data and add them
            course.update(dict(__extract_data(rows[1].findall("td")), **({
                # Add course lab if it has one attached
                "lab": __extract_data(rows[2].findall("td"), True)
            } if len(rows) > 2 else {})))
        # If course key is new to schedule
        if data.get(key) is None:
            # Store the course with that key
            data[key] = course
        # If the course already exists
        else:  # Store it as a lab of the previous course
            data[key]["lab"] = course
    return data


# Returns extracted data from cells as a dict
def __extract_data(cells, lab=False):
    # A function that takes a string and returns all digits in it
    clean = lambda string: "".join([c for c in string if c.isdigit()])
    # Upper case and split time string e.g. ["8:00 AM", "9:15 AM"]
    time = cells[1].text.upper().split(" - ")
    # Store location and doctor
    location = cells[3].text.split()
    doctor = cells[6].find("a")
    return dict({  # Return data dictionary
        "start": time[0], "end": time[1],
        # Store class days in chars, e.g. ["M", "W"]
        "days": cells[2].text.replace(" ", ""),
        # Remove extra parts from location details to gat e.g. "M10, 007"
        "location": location[0][0] + clean(location[0][1:]) + ", " + clean(location[-1].split("-")[-1])
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
