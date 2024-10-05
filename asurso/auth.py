from dataclasses import dataclass

import requests


@dataclass
class LoginData:
    nssession_id: str
    lt: str
    ver: str
    salt: str

    @classmethod
    def get(cls):
        nssession_id, session_data = cls.request()
        if nssession_id or len(session_data) > 0:
            return cls(
                nssession_id=nssession_id,
                lt=session_data["lt"],
                ver=session_data["ver"],
                salt=session_data["salt"]
            )

    @classmethod
    def request(cls) -> (str, str):
        URL = "https://asurso.ru/webapi/auth/getdata"
        response = requests.post(URL)
        if response.status_code == 200:
            nssession_id = response.cookies.get("NSSESSIONID")
            data = response.json()
            return nssession_id, data
        return None


@dataclass
class AuthData:
    at: str
    esrn: str

    @classmethod
    def from_data(cls, at: str, esrn: str):
        return cls(at=at, esrn=esrn)

    def to_requests_auth(self):
        return {"headers": {"at": self.at}, "cookies": {"ESRNSec": self.esrn}}


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
