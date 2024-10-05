from dataclasses import dataclass
from typing import Dict

import requests


@dataclass
class LoginData:
    nssession_id: str
    lt: str
    ver: str
    salt: str

    @classmethod
    def from_data(cls, nssessionid: str, session_data: Dict):
        return cls(
            nssession_id=nssessionid,
            lt=session_data["lt"],
            ver=session_data["ver"],
            salt=session_data["salt"],
        )


@dataclass
class AuthData:
    at: str
    esrn: str

    @classmethod
    def from_data(cls, at: str, esrn: str):
        return cls(at=at, esrn=esrn)

    def to_requests_auth(self):
        return {"headers": {"at": self.at}, "cookies": {"ESRNSec": self.esrn}}


def get_login_data_asurco() -> LoginData:
    URL = "https://asurso.ru/webapi/auth/getdata"
    response = requests.post(URL)
    if response.status_code == 200:
        nssessionid = response.cookies.get("NSSESSIONID")
        data = response.json()
        return LoginData.from_data(nssessionid, data)
    return None


def logout_asurco(auth_data: AuthData, login_data: LoginData):
    URL = "https://asurso.ru/webapi/auth/logout"
    params = {"at": auth_data.at, "VER": login_data.ver}
    response = requests.post(URL, params=params)
    return response.status_code


def auth_asurco(
    login: str, hashed_password: str, password_length: int, login_data: LoginData
) -> AuthData | None:
    URL = "https://asurso.ru/webapi/login"

    params = {
        "LoginType": 1,
        "cid": 2,
        "sid": 1,
        "pid": -1,
        "cn": 1,
        "sft": 2,
        "scid": 2436,
        "UN": login,
        "PW": hashed_password[:password_length],
        "lt": login_data.lt,
        "pw2": hashed_password,
        "ver": login_data.ver,
    }
    response = requests.post(
        URL, params=params, cookies={"NSSESSIONID": login_data.nssession_id}
    )
    if response.status_code == 200:
        data = response.json()
        if data.get("at") is None or response.cookies.get("ESRNSec") is None:
            return None
        return AuthData.from_data(data.get("at"), response.cookies.get("ESRNSec"))
    return None
