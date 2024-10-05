from dataclasses import dataclass
from datetime import date, datetime

import requests

from asurso.auth import AuthData
from asurso.diary.weekday import Weekday
from asurso.student import Student


@dataclass
class Diary:
    week_start: date
    week_end: date
    weekdays: list[Weekday]
    la_assigns: list  # TODO
    term_name: str
    class_name: str

    @classmethod
    def from_dict(cls, data: dict):
        weekdays = [Weekday.from_dict(day) for day in data["weekDays"]]
        return cls(
            week_start=datetime.fromisoformat(data["weekStart"]).date(),
            week_end=datetime.fromisoformat(data["weekEnd"]).date(),
            weekdays=weekdays,
            la_assigns=None,
            term_name=data["termName"],
            class_name=data["className"],
        )


def get_diary_info(auth_data: AuthData, student: Student, week_start: date) -> Diary:
    URL = "https://asurso.ru/webapi/student/diary"
    params = {
        "studentId": student.student_id,
        "weekEnd": "2024-09-29",
        "weekStart": "2024-09-23",
        "yearId": 222228,
    }
    response = requests.get(URL, params=params, **auth_data.to_requests_auth())
    return Diary.from_dict(response.json())
