![](https://github.com/UOSHUB/Images/raw/master/slogan.png)

# UOS HUB Website Back-End

This repository contains the server-side code of UOS HUB website. 
We're using a Python Web Framework called Django, which will be connected to an SQLite database that'll store users' data like their preferences and additions.
Our Django project contains two apps, one is the `Website` app which contains all the static files of the client-side to be sent to it when requested.
The other app is the `Requests` app, which contains all the code and logic for data getting and scraping.
We wrote the `get.py` scripts using Requests library to login, get data and post it from and to UOS websites (myUDC, Blackboard, Outlook & UOS homepage).
And we wrote `scrape.py` scripts using lxml library to scrape the retrieved data and extract the required data to be sent to the client-side.
Then the extracted data will be structured and sent to the client-side as JSON objects.

***

### Diagram of our Back-End's scraping flow (the main functionality)

![](https://github.com/UOSHUB/Images/raw/master/scraping-flow.png)

***

### Details of the Back-End

##### What's happening in the diagram above?
It shows the data scraping request flow in our back-end, which starts by logging into one of the UOS Websites,
then navigating to the page which contains the desired data to be scraped and fetching it.
That's done by the Requests library, which then passes the retrieved page to the lxml library to process and extract exactly what we need from it.
The extracted data is then formatted into JSON objects and passed through Django to the client-side.
Before sending the data, Django might store some of it in it's SQLite Database for later use (by the student only).

##### What's inside the folders?
The `Requests` folder contains the Requests app that handles the data scraping and requesting.
> The `Requests/*` folders are packages containing the `get.py` and `scrape.py` modules for UOS Websites.

The `Website` folder contains the Website app that handles the static files of the front-end.
> The `Website/static` folder links to the [FrontEnd](https://github.com/UOSHUB/FrontEnd) repository which contains front-end's static files.

The `UOSHUB` folder is the Django project root which contains the general configurations of the project.  

***

### Things to do in the future

There're a lot of thing we still need to do in the back-end:

- Finish writing the Requests of the different pages we need from UOS Websites.
- Write the scraping logic of the data fetched from  UOS Websites.
- Provide a RESTful API that the front-end can communicate with in a stateless manner.
- Login once to access to all UOS websites without time limit (UDC limits to 15 mins)
- Implement the logic needed to allow easy designing experience of the student schedule
- Filter emails from repeated emails and from spam
- Build the tasks system to allow adding events, quizzes, tasks, etc.
- Integrate Blackboard announcements and due dates on schedule
- View and notify about courses grades as they come out and calculate GPA
- Allow changing password and profile photo without affecting the original ones
- Add the ability to mark all spam emails as read at once

***

### References

- [Django](https://github.com/django/django)
- [Requests](https://github.com/requests/requests)
- [lxml](https://github.com/lxml/lxml)