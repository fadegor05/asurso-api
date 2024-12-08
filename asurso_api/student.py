from dataclasses import dataclass

import requests

from asurso_api.auth import AuthData


@dataclass
class Student:
    student_id: int
    nickname: str
    class_name: str
    class_id: int
    iup_grade: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            student_id=data.get("studentId"),
            nickname=data.get("nickName"),
            class_name=data.get("className"),
            class_id=data.get("classId"),
            iup_grade=data.get("iupGrade"),
        )


def get_student_info(base_url: str, auth_data: AuthData) -> Student:
    URL = f"{base_url}/webapi/student/diary/init"
    response = requests.get(URL, **auth_data.to_requests_auth())

    if response.status_code == 200:
        student_data = response.json().get("students")[0]
        return Student.from_dict(student_data)
    else:
        raise Exception("Failed to fetch student information")
