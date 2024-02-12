import asyncio
import logging
import os
from datetime import datetime
from typing import List

from pydantic import ValidationError
from pytz import timezone

from reader_base import DataReader
from reader_file import LocalFileReader
from record import Record
from writer_base import DataWriter
from writer_file import FileWriter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def etl(reader: type[DataReader], input_resource: str,
              writer_inst: type[DataWriter]):
    async for json_obj in reader(input_resource).read_data():
        try:
            record = Record(**json_obj)
        except ValidationError as e:
            logging.error("%s. Content of record: %s", e, json_obj)
        else:
            await writer_inst.write_data(record.model_dump_json())


async def etl_all(sources: List[tuple[type[DataReader], str]],
                  writer: type[DataWriter], output_resource: str):
    pipes = []
    async with writer(output_resource) as writer_inst_:
        for (reader_, resource_) in sources:
            pipes.append(asyncio.create_task(etl(reader_, resource_, writer_inst_)))
        await asyncio.gather(*pipes)


if __name__ == "__main__":
    local_now = datetime.now()
    est_now = local_now.astimezone(timezone("US/Eastern"))
    timestamp = est_now.strftime("%Y_%m_%d_%H_%M_%S")
    # TODO: add input/env var parse to use other readers and writers, i.e. HttpReader and PostgreSQLDatabaseWriter
    r, w = LocalFileReader, FileWriter
    input_dir = os.path.join("data", "input")
    output_dir = os.path.join("data", "output")
    f1, f2 = (os.path.join(input_dir, f) for f in ("original_dataset.json", "modified_dataset.json"))
    output_file_path = os.path.join(output_dir, f"output_{timestamp}.jsonl")

    asyncio.run(etl_all([(r, f1), (r, f2)], w, output_file_path))
