import aiofiles

from writer_base import DataWriter


class FileWriter(DataWriter):
    def __init__(self,
                 filename: str,
                 mode: str = 'w+',
                 encoding: str = 'utf-8'):
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.file = None

    async def __aenter__(self):
        self.file = await aiofiles.open(self.filename, mode=self.mode, encoding=self.encoding)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            await self.file.close()

    async def write_data(self, data: str):
        if self.file is None:
            raise RuntimeError('File is not open. Use "async with FileWriter(...)" to open the file.')
        await self.file.write(f"{data}\n")
