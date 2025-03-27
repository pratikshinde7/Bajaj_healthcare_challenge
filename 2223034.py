
import pandas as pd
import re
from datetime import datetime

data_frame = pd.read_excel('C:\Users\Admin\Downloads\Data Engineering\data - sample.xlsx')

data_frame['attendance_date'] = pd.to_datetime(data_frame['attendance_date'], format='%Y-%m-%d')

attendance_records = data_frame.to_dict(orient='records')

students_attendance = {}
for record in attendance_records:
    student_id = record["student_id"]
    if student_id not in students_attendance:
        students_attendance[student_id] = []
    students_attendance[student_id].append(record)

def find_absence_streaks(attendance):
    streaks = []
    current_streak = []

    for i in range(1, len(attendance)):
        if attendance[i]["status"] == "Absent" and attendance[i - 1]["status"] == "Absent":
            if current_streak:
                current_streak.append(attendance[i])
            else:
                current_streak = [attendance[i - 1], attendance[i]]
        else:
            if len(current_streak) > 3:
                streaks.append(current_streak)
            current_streak = []

    if len(current_streak) > 3:
        streaks.append(current_streak)

    return streaks

absence_streaks_info = []
for student_id, records in students_attendance.items():

    records.sort(key=lambda x: x["attendance_date"])
    streaks = find_absence_streaks(records)

    if streaks:
 
        recent_streak = streaks[-1]
        streak_start = recent_streak[0]["attendance_date"]
        streak_end = recent_streak[-1]["attendance_date"]
        total_absence_days = len(recent_streak)

        absence_streaks_info.append({
            "student_id": student_id,
            "absence_start_date": streak_start.strftime("%Y-%m-%d"),
            "absence_end_date": streak_end.strftime("%Y-%m-%d"),
            "total_absent_days": total_absence_days
        })
for info in absence_streaks_info:
    print(info)

data_frame['attendance_date'] = pd.to_datetime(data_frame['attendance_date'], format='%Y-%m-%d')

students_df = pd.DataFrame(students_data)

merged_df = pd.merge(data_frame, students_df, on='student_id', how='left')


def is_valid_email(email):
    return bool(re.match(r'^[A-Za-z][A-Za-z0-9_]*@[A-Za-z0-9]+\.(com|org|net|edu|gov)$', email))


merged_df['valid_email'] = merged_df['parent_email'].apply(is_valid_email)
merged_df['email'] = merged_df['parent_email'].where(merged_df['valid_email'], None)

def create_message(row):
    if row['valid_email']:
        return f"Dear Parent, your child {row['student_name']} was absent on {row['attendance_date'].strftime('%Y-%m-%d')}."
    return None

final_output = merged_df[['student_id', 'student_name', 'attendance_date', 'status', 'email']]

print(final_output)