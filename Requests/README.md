![](https://github.com/requests/requests/raw/749edb35541d7bc008f5db860c798f800881cd2e/docs/_static/requests-sidebar.png)
# Requests App

In this Django app, all the web scraping happens.
Both getting and posting data from and to UOS websites using Python3-Requests,
and extracting the required information from the pulled data.

For further details and a holistic overview of the project, checkout [the main readme file](../README.md)

### Glossary of frequently used terms
- Student id: UOS student's unique identification number, which is the letter 'u' followed by 8 digits
- Student password: UOS student's login password which is usually a 6 digits number unless it's changed
- Student email: UOS student's email address, which is of the format `<Student id>@sharjah.ac.ae`
- Term code: Id of the queried term / semester, which is 6 digits number of the format `<Full Year> + <Season Number>`
    - Full Year is the year in 4 digits
    - Season Number is one of these values {10: Fall, 20: Spring, 30: Summer}
    - For example, Fall 2017 term's code is `201710`
> Reports specific values are listed in `./reports/values.py`

