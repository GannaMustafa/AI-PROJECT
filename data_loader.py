import pandas as pd

courses = pd.read_csv("data/courses.csv").set_index("id")
rooms = pd.read_csv("data/rooms.csv").set_index("id")
teachers = pd.read_csv("data/teachers.csv").set_index("id")
time_slots = pd.read_csv("data/time_slots.csv").set_index("id")
sessions = pd.read_csv("data/sessions.csv")

sessions["course_code"] = sessions["course_id"].map(courses["course_code"])
sessions["course_title"] = sessions["course_id"].map(courses["course_title"])
sessions["students"] = sessions["course_id"].map(courses["enrolled"])

teacher_names = teachers["first_name"] + " " + teachers["last_name"]
sessions["teacher_name"] = sessions["teacher_id"].map(teacher_names)

sessions["room_code"] = sessions["room_id"].map(rooms["room_code"])
sessions["room_capacity"] = sessions["room_id"].map(rooms["capacity"])
sessions["room_type"] = sessions["room_id"].map(rooms["room_type"])

sessions["day"] = sessions["slot_id"].map(time_slots["weekday"])
sessions["period"] = sessions["slot_id"].map(time_slots["period_no"])

import pandas as pd

courses = pd.read_csv("data/courses.csv").set_index("id")
rooms = pd.read_csv("data/rooms.csv").set_index("id")
teachers = pd.read_csv("data/teachers.csv").set_index("id")
time_slots = pd.read_csv("data/time_slots.csv").set_index("id")
sessions = pd.read_csv("data/sessions.csv")

sessions["course_code"] = sessions["course_id"].map(courses["course_code"])
sessions["course_title"] = sessions["course_id"].map(courses["course_title"])
sessions["students"] = sessions["course_id"].map(courses["enrolled"])

teacher_names = teachers["first_name"] + " " + teachers["last_name"]
sessions["teacher_name"] = sessions["teacher_id"].map(teacher_names)

sessions["room_code"] = sessions["room_id"].map(rooms["room_code"])
sessions["room_capacity"] = sessions["room_id"].map(rooms["capacity"])
sessions["room_type"] = sessions["room_id"].map(rooms["room_type"])

sessions["day"] = sessions["slot_id"].map(time_slots["weekday"])
sessions["period"] = sessions["slot_id"].map(time_slots["period_no"])

print(sessions.head())