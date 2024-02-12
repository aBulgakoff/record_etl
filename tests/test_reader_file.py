import pytest

from reader_file import LocalFileReader


@pytest.mark.asyncio
async def test_empty_file():
    reader = LocalFileReader('data/empty.json')
    count = 0
    async for _ in reader.read_data():
        count += 1
    assert count == 0


@pytest.mark.asyncio
async def test_ten_items_file():
    reader = LocalFileReader('data/ten_items.json')
    count = 0
    async for _ in reader.read_data():
        count += 1
    assert count == 10
