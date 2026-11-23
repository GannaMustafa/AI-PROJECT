import pandas as pd

courses = pd.read_csv("data/courses.csv")
rooms = pd.read_csv("data/rooms.csv")
teachers = pd.read_csv("data/teachers.csv")
time_slots = pd.read_csv("data/time_slots.csv")
sessions = pd.read_csv("data/sessions.csv")

tables = [courses, rooms, teachers, time_slots, sessions]

for table in tables:
    if table["id"].duplicated().any():
        raise ValueError("A table contains duplicate IDs")
    if table.isna().any().any():
        raise ValueError("A table contains empty values")

checks = [
    ("course_id", courses),
    ("teacher_id", teachers),
    ("room_id", rooms),
    ("slot_id", time_slots),
]

for column, table in checks:
    if not sessions[column].isin(table["id"]).all():
        raise ValueError(f"Invalid IDs in sessions.csv: {column}")

courses = courses.set_index("id")
rooms = rooms.set_index("id")
teachers = teachers.set_index("id")
time_slots = time_slots.set_index("id")

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

sessions["department"] = sessions["course_id"].map(courses.set_index("id")["department"])
sessions["start_time"] = sessions["slot_id"].map(time_slots.set_index("id")["starts_at"])
sessions["end_time"] = sessions["slot_id"].map(time_slots.set_index("id")["ends_at"])

print(sessions.head())