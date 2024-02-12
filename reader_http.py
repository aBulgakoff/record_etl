from typing import AsyncGenerator

import aiohttp

from reader_base import DataReader


class HttpReader(DataReader):
    # TODO: HttpReader provided to show potential usage outside of initial task. Yet to be tested.
    def __init__(self, url: str):
        self.url = url

    async def read_data(self) -> AsyncGenerator[dict, None]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status != 200:
                    raise aiohttp.ClientError(f"Received status code {response.status}")
                if response.content_type != "application/json":
                    raise ValueError("Response content type is not JSON.")
                data = await response.json()
                if not isinstance(data, list):
                    raise ValueError("Expected a list of JSON objects.")
                for item in data:
                    yield item
