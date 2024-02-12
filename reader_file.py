from typing import AsyncGenerator

import aiofiles
import ijson

from reader_base import DataReader


class LocalFileReader(DataReader):
    def __init__(self, file_name: str):
        self.file_name = file_name

    async def read_data(self) -> AsyncGenerator[dict, None]:
        async with aiofiles.open(self.file_name, 'r') as f:
            content = await f.read()
            for json_obj in ijson.items(content, 'item'):
                yield json_obj
