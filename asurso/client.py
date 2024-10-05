from dataclasses import dataclass
from datetime import date

from asurso.auth import (
    AuthData,
    LoginData,
)
from asurso.diary.diary import Diary, get_diary_info
from asurso.student import get_student_info, Student
from asurso.utils import md5


@dataclass
class ASURSOClient:
    login: str
    hashed_password: str
    password_length: int
    login_data: LoginData = None
    auth_data: AuthData = None
    student: Student = None

    @classmethod
    def create(cls, login: str, password: str):
        login_data = LoginData.get()
        hashed_password = md5(login_data.salt + md5(password))
        return cls(
            login=login,
            hashed_password=hashed_password,
            password_length=len(password),
            login_data=login_data,
        )

    def auth(self):
        self.auth_data = AuthData.auth(self.login, self.hashed_password, self.password_length, self.login_data)
        self.student = get_student_info(self.auth_data)

    def logout(self):
        self.auth_data.logout(self.login_data)

    def get_diary(self, week_start: date) -> Diary:
        return get_diary_info(self.auth_data, self.student, week_start)
