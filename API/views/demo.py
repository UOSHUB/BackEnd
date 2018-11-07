from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from random import randint as rand
from json import loads as json
from os.path import dirname

day = timedelta(days=1)
hour = timedelta(hours=1)

# Demo request handler
class Demo(APIView):
    """
    This returns a demo of complete student data.
    """
    # Returns demo student data on GET request
    @staticmethod
    def get(request):
        days = datetime.now().replace(hour=11, minute=59)
        date = lambda d: d.isoformat().split('.')[0] + "+0400"
        with open(dirname(__file__) + "/../demo.json", encoding="utf-8") as demo:
            data = json(demo.read())
        for index, course_id in enumerate(data["courses"].keys()):
            days -= day
            i = index + 1
            data["deadlines"].append({
                "title": f"Assignment #{i} Submission",
                "dueDate": date(days + day*3),
                "course": course_id
            })
            for j in range(5):
                data["documents"].append({
                    "course": course_id,
                    "title": f"Document File #{i+j}",
                    "file": f"document file #{i+j}.pdf",
                })
            exam = rand(12, 18)
            data["finals"].append({
                "course": course_id,
                "date": f"{rand(15, 25)}-DEC-2018",
                "start": f"{rand(12, 18)}:00",
                "end": f"{exam + 2}:00",
                "location": f"{['M', 'W'][rand(0, 1)]}{rand(3, 10)}, 10{rand(1, 9)}"
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
                    "time": date(days + hour * (10 - j)),
                    "title": f"Email Title #{i}"
                })
                data["emails"]["body"][f"{course_id}{i}"] = f"Email #{i} Sample Content<br/><br/><br/>This will be filled with email stuff"
        # Return a JSON object of all demo data
        return Response(data)
