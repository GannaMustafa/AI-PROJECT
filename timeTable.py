import pandas as pd 
import random


courses = pd.read_csv("data/courses.csv").reset_index(drop = True)
rooms = pd.read_csv("data/rooms.csv").reset_index(drop = True)
sessions = pd.read_csv("data/sessions.csv").reset_index(drop = True)


def make_table () :
    table = []
    for i in range(len(sessions)):
        slot = random.randint(0, 39)
        room = random.randint(0,9)
        table.append([
            slot,
            room
        ])

    return table

def copy_table(table):
    copied = []
    for i in table :
        row = []
        for j in i :
            row.append(j)
        copied.append(row)

    return copied


def check_constraints (table) :
    total = 0
    for i in range(len(table)):
        for j in range(i+1, len(table)) :
            if  table[i][1] == table[j][1] and table[i][0] == table[j][0]:
                total += 1


        teacher_i = sessions.iloc[i]['teacher_id'] 
        for j in range(i + 1, len(table)):
            teacher_j = sessions.iloc[j]['teacher_id']
            
            if teacher_i == teacher_j and table[i][0] == table[j][0]:
                total += 1


        index = table[i][1]
        room_capacity = rooms.iloc[index]['capacity']
        course_id = sessions.iloc[i]['course_id']
        students_num = courses.iloc[course_id - 1]['enrolled']

        if students_num > room_capacity :
            total += 1

    return total


if __name__ == "__main__":
    # اختبار make_table
    t = make_table()
    print(f"طول الجدول: {len(t)}")
    print(f"أول 3 عناصر: {t[:3]}")
    print()
    
    # اختبار check_constraints
    violations = check_constraints(t)
    print(f"عدد التعارضات في جدول عشوائي: {violations}")
    print("(المفروض رقم كبير لأن الجدول عشوائي)")
    print()
    
    # اختبار copy_table
    t2 = copy_table(t)
    t2[0][0] = 999  # نعدل في النسخة
    print(f"الأصل بعد التعديل: {t[0]}")  # المفروض ما يتأثرش
    print(f"النسخة بعد التعديل: {t2[0]}")  # المفروض تتعدل