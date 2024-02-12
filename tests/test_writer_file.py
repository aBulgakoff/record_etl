import json

import pytest

from writer_file import FileWriter


@pytest.fixture
def test_data():
    return [{"id": i, "data": f"record{i}"} for i in range(1, 11)]


@pytest.mark.asyncio
async def test_write_zero_records(tmp_path):
    async with FileWriter(tmp_path / "output_one.json") as file_writer:
        await file_writer.write_data("")

    with open(tmp_path / "output_one.json", "r") as file:
        lines = file.readlines()
    # new line symbol is expected to be written
    assert len(lines) == 1


@pytest.mark.asyncio
async def test_write_ten_records(tmp_path, test_data):
    async with FileWriter(tmp_path / "output_ten.json") as file_writer:
        for record in test_data:
            await file_writer.write_data(record)

    with open(tmp_path / "output_ten.json", "r") as file:
        lines = file.readlines()
    assert len(lines) == 10


@pytest.mark.asyncio
async def test_compare_records(tmp_path, test_data):
    async with FileWriter(tmp_path / "output_compare.json") as file_writer:
        for record in test_data:
            await file_writer.write_data(json.dumps(record))

    with open(tmp_path / "output_compare.json", "r") as file:
        lines = file.readlines()

    written_records = [json.loads(line) for line in lines]
    assert written_records == test_data
