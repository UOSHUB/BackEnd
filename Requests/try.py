import reports

plan = reports.get.study_plan("u14110989", "201410")
print(plan.decode())
all_courses = (reports.design_schedule_scraping.study_plan_courses(plan))
print (all_courses)

print(reports.design_schedule_scraping.get_future_courses(all_courses))