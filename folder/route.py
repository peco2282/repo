from enum import Enum

base = "https://.../.../"


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"


class Route:
    def __init__(
            self,
            method: str,
            path: str,
            **kwargs
    ):
        self.method = method.upper()
        self.path = path

    @property
    def url(self) -> str:
        return base + self.path
