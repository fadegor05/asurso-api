from dataclasses import dataclass
from datetime import date, datetime

import requests
from asurso_api.utils.date import get_week_interval_by_date

from asurso_api.auth import AuthData
from asurso_api.context import Context
from asurso_api.diary.weekday import Weekday
from asurso_api.student import Student


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


def get_diary_info(auth_data: AuthData, student: Student, context: Context,
                   day: date = datetime.now().date()) -> Diary:
    start_datetime, end_datetime = get_week_interval_by_date(day)
    URL = "https://asurso.ru/webapi/student/diary"
    params = {
        "studentId": student.student_id,
        "weekStart": start_datetime.strftime("%Y-%m-%d"),
        "weekEnd": end_datetime.strftime("%Y-%m-%d"),
        "yearId": context.school_year_id,
    }
    response = requests.get(URL, params=params, **auth_data.to_requests_auth())
    return Diary.from_dict(response.json())
