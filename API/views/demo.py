from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from json import loads as json
from os.path import dirname
from random import randint as rand

day = timedelta(days=1)

# Demo request handler
class Demo(APIView):
    """
    This returns a demo of complete student data.
    """
    # Returns demo student data on GET request
    @staticmethod
    def get(request):
        days = datetime.today() + day + day
        date = lambda d: d.isoformat().split('.')[0] + "+0400"
        with open(dirname(__file__) + "/../demo.json", encoding="utf-8") as demo:
            data = json(demo.read())
        for index, course_id in enumerate(data["courses"].keys()):
            i = index + 1
            days -= day
            data["deadlines"].append({
                "title": f"Assignment #{i} Submission",
                "dueDate": date(days + day),
                "time": date(days),
                "course": course_id
            })
            data["documents"].append({
                "course": course_id,
                "title": f"Document File #{i}",
                "file": f"document file #{i}.pdf",
                "time": date(days)
            })
            exam = rand(12, 18)
            data["finals"].append({
                "course": course_id,
                "date": f"{rand(15, 25)}-DEC-2018",
                "start": f"{rand(12, 18)}:00",
                "end": f"{exam + 2}:00",
                "location": f"M{rand(1, 12)}, 10{rand(1, 9)}"
            })
            data["grades"].append({
                "course": course_id,
                "title": f"Lab #{i}",
                "grade": rand(5, 10),
                "outOf": 10
            })
            data["updates"].append({
                "course": course_id,
                "title": f"Quiz #{i} next class",
                "time": date(days),
                "body": f"We will have quiz #{i} next class",
                "event": "Announcement"
            })
            for j, category in enumerate(["personal", "courses", "events"]*3):
                i += j
                data["emails"][category].append({
                    "event": "New Email",
                    "from": f"sender{i}@sharjah.ac.ae",
                    "id": f"{course_id}{i}",
                    "sender": f"Sender #{i}",
                    "time": date(days),
                    "title": f"Email Title #{i}"
                })
                data["emails"]["body"][f"{course_id}{i}"] = f"Email #{i} Sample Content<br/><br/><br/>This will be filled with email stuff"
        # Return a JSON object of all demo data
        return Response(data)
