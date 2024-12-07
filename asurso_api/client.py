from dataclasses import dataclass
from datetime import date

from asurso_api.auth import (
    AuthData,
    LoginData,
)
from asurso_api.context import Context
from asurso_api.diary.diary import Diary, get_diary_info
from asurso_api.student import get_student_info, Student
from asurso_api.utils.hash import md5


@dataclass
class ASURSOClient:
    login_data: LoginData = None
    auth_data: AuthData = None
    student: Student = None
    context: Context = None

    @classmethod
    def from_account_data(cls, login: str, password: str):
        login_data = LoginData.get()
        hashed_password = md5(login_data.salt + md5(password))
        return cls(
            auth_data=AuthData.auth(login, hashed_password, len(password), login_data)
        )

    @classmethod
    def from_auth_data(cls, auth_data: AuthData, login_data: LoginData | None = None):
        return cls(
            auth_data=auth_data,
            login_data=login_data,
        )

    def init(self):
        self.context = Context.from_auth_data(self.auth_data)
        self.student = get_student_info(self.auth_data)

    def logout(self):
        if self.login_data:
            self.auth_data.logout(self.login_data)

    def get_diary(self, day: date) -> Diary:
        return get_diary_info(self.auth_data, self.student, self.context, day)
