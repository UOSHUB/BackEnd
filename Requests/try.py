import reports

plan = reports.get.study_plan("u14110989", "201410")
#print(plan.decode())
all_courses = (reports.design_schedule_scraping.study_plan_courses(plan))
#print(all_courses)

dept = "COSC"

future_courses = reports.get.offered_201720_courses(dept)
# print(future_courses.decode())
future_courses_details = (reports.design_schedule_scraping.next_semester_courses(future_courses,all_courses))
print(future_courses_details)
