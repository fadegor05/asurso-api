from dataclasses import dataclass
from datetime import datetime

from asurso.diary.type import Type


@dataclass
class Assignment:
    assignment_id: int
    assignment_type: Type
    assignment_name: str
    weight: int
    due_date: datetime
    class_assignment: bool
    class_meeting_id: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            assignment_id=data["id"],
            assignment_type=data["typeId"],
            assignment_name=data["assignmentName"],
            weight=data["weight"],
            due_date=datetime.fromisoformat(data["dueDate"]),
            class_assignment=data["classAssignment"],
            class_meeting_id=data["classMeetingId"],
        )
