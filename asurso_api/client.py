from dataclasses import dataclass
from datetime import date

from asurso_api.auth import (
    AuthData,
    LoginData,
)
from asurso_api.context import Context
from asurso_api.diary.diary import Diary, get_diary_info
from asurso_api.region import Region
from asurso_api.student import get_student_info, Student
from asurso_api.utils.hash import md5


@dataclass
class ASURSOClient:
    base_url: str
    login_data: LoginData = None
    auth_data: AuthData = None
    student: Student = None
    context: Context = None

    @classmethod
    def from_account_data(cls, login: str, password: str, region: Region = Region.SAM):
        login_data = LoginData.get(region.value)
        hashed_password = md5(login_data.salt + md5(password))
        return cls(
            auth_data=AuthData.auth(region.value, login, hashed_password, len(password), login_data),
            base_url=region.value,
        )

    @classmethod
    def from_auth_data(cls, auth_data: AuthData, login_data: LoginData | None = None, region: Region = Region.SAM):
        return cls(
            auth_data=auth_data,
            login_data=login_data,
            base_url=region.value,
        )

    def init(self):
        self.context = Context.from_auth_data(self.base_url, self.auth_data)
        self.student = get_student_info(self.base_url, self.auth_data)

    def logout(self):
        if self.login_data:
            self.auth_data.logout(self.base_url, self.login_data)

    def get_diary(self, day: date) -> Diary:
        return get_diary_info(self.base_url, self.auth_data, self.student, self.context, day)
