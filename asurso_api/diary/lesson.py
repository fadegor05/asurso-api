from dataclasses import dataclass
from datetime import time, date, datetime

from asurso_api.diary.assignment import Assignment


@dataclass
class Lesson:
    assignments: list[Assignment]
    is_distance_lesson: bool
    is_ea_lesson: bool
    class_meeting_id: int
    day: date
    number: int
    relay: int
    room: int
    start_time: time
    end_time: time
    subject_name: str

    @classmethod
    def from_dict(cls, data: dict):
        assignments = [
            Assignment.from_dict(assignment) for assignment in data["assignments"]
        ]
        return cls(
            assignments=assignments,
            is_distance_lesson=data["isDistanceLesson"],
            is_ea_lesson=data["isEaLesson"],
            class_meeting_id=data["classmeetingId"],
            day=datetime.fromisoformat(data["day"]).date(),
            number=data["number"],
            relay=data["relay"],
            room=data["room"],
            start_time=datetime.strptime(data["startTime"], "%H:%M").time(),
            end_time=datetime.strptime(data["endTime"], "%H:%M").time(),
            subject_name=data["subjectName"],
        )
