from dataclasses import dataclass
from datetime import datetime, date

from asurso_api.diary.lesson import Lesson


@dataclass
class Weekday:
    date: date
    lessons: list[Lesson]

    @classmethod
    def from_dict(cls, data: dict):
        lessons = [Lesson.from_dict(lesson) for lesson in data["lessons"]]
        lessons.sort(key=lambda lesson: lesson.number)
        return cls(date=datetime.fromisoformat(data["date"]).date(), lessons=lessons)
