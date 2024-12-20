from dataclasses import dataclass

import requests


@dataclass
class AuthPlaceData:
    region_id: int
    region_area_id: int
    city_id: int
    school_type_id: int
    school_id: int
    country_id: int = 2


@dataclass
class PreAuthData:
    nssession_id: str
    lt: str
    ver: str
    salt: str

    @classmethod
    def get(cls, base_url: str):
        nssession_id, session_data = cls.request_pre_auth(base_url)
        if nssession_id or len(session_data) > 0:
            return cls(
                nssession_id=nssession_id,
                lt=session_data["lt"],
                ver=session_data["ver"],
                salt=session_data["salt"]
            )

    @classmethod
    def request_pre_auth(cls, base_url: str) -> (str, str):
        URL = f"{base_url}/webapi/auth/getdata"
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

    @classmethod
    def auth(cls, base_url: str, login: str, hashed_password: str, password_length: int, pre_auth_data: PreAuthData,
             auth_place_data: AuthPlaceData):
        at, esrn = cls.request_auth(base_url, login, hashed_password, password_length, pre_auth_data, auth_place_data)
        if at and esrn:
            return cls(at=at, esrn=esrn)

    @classmethod
    def request_auth(cls, base_url: str, login: str, hashed_password: str, password_length: int,
                     pre_auth_data: PreAuthData, auth_place_data: AuthPlaceData) -> (str, str):
        URL = f"{base_url}/webapi/login"

        params = {
            "LoginType": 1,
            "cid": auth_place_data.country_id,
            "sid": auth_place_data.region_id,
            "pid": auth_place_data.region_area_id,
            "cn": auth_place_data.city_id,
            "sft": auth_place_data.school_type_id,
            "scid": auth_place_data.school_id,
            "UN": login,
            "PW": hashed_password[:password_length],
            "lt": pre_auth_data.lt,
            "pw2": hashed_password,
            "ver": pre_auth_data.ver,
        }
        response = requests.post(
            URL, params=params, cookies={"NSSESSIONID": pre_auth_data.nssession_id}
        )
        if response.status_code == 200:
            data = response.json()
            at = data.get("at")
            esrn = response.cookies.get("ESRNSec")
            if at is None or esrn is None:
                raise ValueError("Invalid credentials")
            return at, esrn
        raise ValueError("Invalid credentials")

    def to_requests_auth(self):
        return {"headers": {"at": self.at}, "cookies": {"ESRNSec": self.esrn}}

    def logout(self, base_url: str, pre_auth_data: PreAuthData):
        URL = f"{base_url}/webapi/auth/logout"
        params = {"at": self.at, "VER": pre_auth_data.ver}
        response = requests.post(URL, params=params)
        return response.status_code
