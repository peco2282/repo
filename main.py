import asyncio
import time
from os import getenv

from dotenv import load_dotenv

from folder import Client

load_dotenv()

m = Client()
asyncio.run(m.send(channel="...", text="text"))

m.run(getenv("OAUTH_TOKEN"))

