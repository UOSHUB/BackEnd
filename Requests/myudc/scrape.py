from lxml.html import fromstring as __parse

seasons_codes = {"Fall": "10", "Spring": "20", "Summer": "30"}


# Returns term code from string of "TERM YYYY-YYYY" format
def __get_term_code(term_name):
    # Separate season from year and store both
    season, year = term_name.split(" ", 1)
    # Return the first year among the two plus season's code
    return year.split("-")[0] + seasons_codes[season]


# Scrapes all terms that student was registered in
def registered_terms(page):
    return {
        # Return a dictionary that contains {term code: term name} pairs
        __get_term_code(term_name.text): term_name.text
        # Loop through tags which contain term name
        for term_name in __parse(page).findall(".//span[@class='fieldOrangetextbold']")
    }


# Scrapes a single course's data
def course(page):
    # Store main table's caption and body
    caption, body = __parse(page).find(".//table[@class='datadisplaytable']").findall("tr")
    # Split caption to get course's title, crn, key and section
    title, crn, key, section = caption.text_content().strip().split(" - ")
    # Return course data dictionary
    return {  # In {course key: course data} format
        key.replace(" ", ""): dict({
            "title": title,
            "section": section,
            "crn": int(crn),
            # Credits hours value isn't structured, so search among the strings to find it
            "ch": int(body.xpath("td/text()[contains(., 'Credits')]")[0].strip()[0])
            # Get & add lecture/lab details
        }, **__get_data(body.findall(".//tr"), title))
    }


# Scrapes "Student Detail Schedule" data
def term(page):
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
        # Combine all course data
        course_data = dict({
            "title": title,
            "section": section,
            "crn": int(cells[1].text),
            "ch": int(cells[5].text.strip()[0])
            # Get & add lecture/lab details
        }, **__get_data(rows, title))
        # If course key is new to term
        if data.get(key) is None:
            # Store the course with that key
            data[key] = course_data
        # If the course already exists
        else:  # Store it as a lab of the previous course
            data[key]["lab"] = course_data
    return data


# Returns course's lecture (and lab if available) details
def __get_data(rows, title):
    data = {}
    # If course is not the Junior/Senior Project
    if not ("Junior" in title or "Senior" in title):  # TODO: also if time is TBA
        # Extract and add lecture details
        data = __extract_data(rows[1].findall("td"))
        # If there's a lab (second row)
        if len(rows) > 2:
            # Extract and add lab details
            data["lab"] = __extract_data(rows[2].findall("td"), True)
    return data


# Returns extracted data from lecture/lab cells as a dict
def __extract_data(cells, lab=False):
    # A function that takes a string and returns all digits in it
    clean = lambda string: "".join([c for c in string if c.isdigit()])  # TODO: this vs re (speed test)
    # Upper case and split time string e.g. ["8:00 AM", "9:15 AM"]
    time = cells[1].text.upper().split(" - ")
    # Store location and doctor
    location = cells[3].text.split()
    doctor = cells[6].find("a")
    return dict({  # Return data dictionary
        "start": time[0], "end": time[1],
        # Store class days in chars, e.g. ["M", "W"]
        "days": cells[2].text.replace(" ", ""),
        # Remove extra parts from location details to get e.g. "M10, 007"
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


# Scrapes student's holds
def holds(page):
    data = []
    # Loop through holds table's rows which contain data
    for hold in __parse(page).findall(".//table[@class='datadisplaytable']/tr")[1:]:
        # Store hold's row cells
        cells = hold.findall("td")
        # Add holds type, reason, start & end dates
        data.append({
            "type": cells[0].text,
            "start": cells[1].text,
            "end": cells[2].text,
            "reason": cells[4].text
        })
    return data
