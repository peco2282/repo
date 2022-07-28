import asyncio
import json
import signal
import traceback
from typing import Coroutine, Callable, TypeVar, Any, Dict, List, Tuple

from . import HTTPClient, Route



class Client:
    def __init__(
            self,
            **options
    ):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.http = HTTPClient(loop=self.loop)
        self._handlers: Dict[str, List[Tuple[asyncio.Future, Callable[..., bool]]]] = {}
        self._closed = False

    def run(self, token: str, **kwargs) -> None:
        loop = self.loop

        try:
            loop.add_signal_handler(signal.SIGINT, loop.stop)
            loop.add_signal_handler(signal.SIGTERM, loop.stop)

        except (NotImplementedError, RuntimeError):
            pass

        async def runner():
            try:
                await self.start(token=token)

            finally:
                if not self.is_closed():
                    await self.close()

        def stop_loop_on_completion(f):
            loop.stop()

        future = asyncio.ensure_future(runner(), loop=loop)
        future.add_done_callback(stop_loop_on_completion)

        try:
            loop.run_forever()

        except KeyboardInterrupt:
            pass

        finally:
            future.remove_done_callback(stop_loop_on_completion)

        if not future.cancelled():
            try:
                return future.result()

            except KeyboardInterrupt:
                return None

    async def start(self, token):
        await self.login(token=token)
        print("log")
        await self.connect()

    def is_closed(self) -> bool:
        return self._closed

    async def close(self):
        if self._closed:
            return

        self._closed = True
        await self.http.closed()
        self._ready.clear()

    async def login(self, token: str):
        if not isinstance(token, str):
            raise TypeError("str")
        print("login")

        data = await self.http.static_login(token=token.strip())
        print(data)
        # with open("login.json", mode="w") as f:
        #     json.dump(data, f)

        print("logging")

    async def connect(self):
        while not self.is_closed():
            if self.is_closed():
                return

    async def send(self, channel, text):
        r = Route(path="...", method="POST")
        resp = await self.http.request(route=r, data={"channel": channel, "text": text})
        print(resp)
        return resp
