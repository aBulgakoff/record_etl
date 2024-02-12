import json

import asyncpg

from writer_base import DataWriter


class PostgreSQLDatabaseWriter(DataWriter):
    # TODO: PostgreSQLDatabaseWriter provided to show potential usage outside of initial task. Yet to be tested.
    def __init__(self, db_config: dict, table_name: str):
        self.db_config = db_config
        self.table_name = table_name
        self.connection = None

    async def __aenter__(self):
        self.connection = await asyncpg.connect(**self.db_config)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()

    async def write_data(self, data: str):
        insert_query = (f"INSERT INTO {self.table_name} "
                        f"(id, code, description, status, date_opened, date_closed) "
                        f"VALUES ($1, $2, $3, $4, $5, $6)")

        record = json.loads(data)
        if not record.get('id'):
            raise ValueError(f'No id found in record: "{data}"')
        await self.connection.execute(insert_query,
                                      record.get('id'),
                                      record.get('code'),
                                      record.get('description'),
                                      record.get('status'),
                                      record.get('date_opened'),
                                      record.get('date_closed'))
