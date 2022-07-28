import asyncio
import json
import traceback
from typing import Optional

import aiohttp

from folder import Route


class HTTPClient:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop
        self.__session = aiohttp.ClientSession()
        self.token: Optional[str] = None

    async def closed(self):
        if self.__session:
            await self.__session.close()

    async def static_login(self, token: str):
        self.token = token
        try:
            # TODO path
            data = await self.request(Route("GET", "..."))

        except Exception as exc:
            return traceback.TracebackException.from_exception(exc)

        return data

    async def request(
            self,
            route: Route,
            **kwargs
    ):
        method = route.method
        url = route.url
        data = kwargs.get("data")

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        async with self.__session.request(method="POST", url=url, headers=headers, data=data) as response:
            text = await response.text(encoding="utf8")
            print(text)
            try:
                if response.headers["content-type"] == "application/json":
                    return json.loads(text)
                json_data = await response.json(encoding="utf8")
                return json_data

            except KeyError as k:
                print(k)

            except json.JSONDecodeError as js:
                print(js)

            return text

