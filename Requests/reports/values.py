campuses = {
    "Maliha Women's Campus": "MLW",
    "Sharjah Women's Camp Community": "SHW",
    "Al-Dhaid Women's Campus": "DHW",
    "Khorfakan Women's Campus": "KOW",
    "Deba Al Hesn Women's Campus": "DNW",
    "Maliha Men's Campus": "MLM",
    "Al-Dhaid Men's Campus": "DHM",
    "Kalba UOS Men's Campus": "KUM",
    "Kalba Men's Camp. Community": "KAM",
    "Medical Men's Campus": "MDM",
    "Kalba Women's Camp. Community": "KAW",
    "Khorfakan Men's Campus": "KOM",
    "FineArts Men's Campus": "FAM",
    "Kalba UOS Women's Campus": "KUW",
    "Sharjah Men's Camp Community": "SHM",
    "UOS Main Campus": "UOS",
    "UOS Men's Campus": "MAM",
    "UOS Women's Campus": "MAW"
}

collages = {
    "Shari'a & Islamic Studies": "01",
    "Arts, Humanities & Social Sci.": "02",
    "Business Administration": "03",
    "Engineering": "04",
    "Health Sciences": "05",
    "Law": "06",
    "Communication": "08",
    "Medicine": "09",
    "Pharmacy": "11",
    "Community": "12",
    "Sciences": "14",
}

departments = {
    "Physiotherapy": "PHTH",
    "Applied Physics": "APHY",
    "Mechanical Engineering": "MECH",
    "Health Services Administration": "HSAD",
    "Education": "EDUC",
    "Information Technology(Commun)": "INFO",
    "Computer Science": "COSC",
    "English Language Center": "IEP",
    "Pharmacy": "PHRM",
    "Health and Medical Sciences": "HMSC",
    "English Language & Literature": "ENGL",
    "Nuclear Engineering": "NUCL",
    "Financial & Administrative Sci": "FIAD",
    "Mass Communication": "MASS",
    "International Relations": "INRE",
    "Sociology": "SOCI",
    "Electrical/Electronic Eng.": "EECE",
    "Foundations of Religion": "FREL",
    "Basic Sciences(Community)": "BSCC",
    "Health Sciences/General": "HSGN",
    "Medicine": "MEDC",
    "Clinical Nutrition": "CLNU",
    "Communication": "COMM",
    "Accounting": "ACCT",
    "Medical Laboratory Technology": "MLT",
    "Mathematics": "MATH",
    "Medical Diagnostic Imaging": "MDI",
    "Nursing": "NURS",
    "Civil & Environ. Eng.": "CIVL",
    "Industrial Engn & Engn Managmt": "IEMG",
    "Public Relation": "PUBL",
    "General Medicine": "GMED",
    "Chemistry": "CHMS",
    "Computer Engineering": "CENG",
    "Master of Business Admin.": "MBA",
    "Environmental Health": "ENVH",
    "Law": "LAW",
    "History & Islamic Civilization": "HISL",
    "Mang. Info. Sys & Operations": "MIS",
    "Architectural Engineering": "ARCH",
    "Finance and Economics": "FNEC",
    "Management": "BUSP",
    "Arabic Language & Literature": "ARAB",
    "Jurisprudence & its Foundation": "JURF",
    "Sustainable/Renewable Enrg Eng": "SREE",
    "Applied Biology": "BIOT",
    "Public Law": "PBLW",
    "Private Law": "PRLW"
}

levels = {
    "Diploma": "DP",
    "Foundation Year": "FY",
    "General Diploma": "GD",
    "Higher Diploma": "HD",
    "Intensive English": "IE",
    "Master": "GR",
    "Medical Phase 2": "MD",
    "Medical Phase 3": "MF",
    "Undeclared": "00",
    "Undergraduate": "UG"
}

seasons_codes = {"fall": "10", "spring": "20", "summer": "30"}


# Returns semester code from string of "Fall 2017-2018" format
def semester_code(semester):
    # Separate season from year and store both
    season, year = semester.split(" ", 1)
    # Return the first year among the two plus season's code
    return year.split("-")[0].strip() + seasons_codes[season.lower()]
