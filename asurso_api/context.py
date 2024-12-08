from dataclasses import dataclass

import requests

from asurso_api.auth import AuthData


@dataclass
class Context:
    global_year_id: int
    school_year_id: int
    school_id: int
    school_name: str
    user_id: int
    user_name: str

    @classmethod
    def from_auth_data(cls, base_url: str, auth_data: AuthData):
        context = cls.request_context(base_url, auth_data)
        return cls(global_year_id=context["globalYearId"],
                   school_year_id=context["schoolYearId"],
                   school_id=context["schoolId"],
                   school_name=context["organization"]["name"],
                   user_id=context["userId"],
                   user_name=context["user"]["name"])

    @classmethod
    def request_context(cls, base_url: str, auth_data: AuthData):
        URL = f"{base_url}/webapi/context"
        response = requests.get(URL, **auth_data.to_requests_auth())
        return response.json()
