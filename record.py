import logging
from collections import deque
from datetime import date
from enum import Enum
from typing import ClassVar

from pydantic import (BaseModel,
                      ValidationInfo,
                      constr,
                      field_validator,
                      model_validator)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class RecordStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    BOTH = "BOTH"


class RecordError(ValueError):
    pass


"""TODO: add async SharedLock i.e. using external cache since in Pydantic 
class fields a.k.a 'ModelPrivateAttr' objects do not support the asynchronous context manager protocol.
tried: Record._lock = asyncio.Lock()

"""


class Record(BaseModel):
    id: int
    code: constr(min_length=1)
    status: RecordStatus
    description: str | None
    date_opened: date | None
    date_closed: date | None
    _ids: ClassVar[set[int]] = set()

    @field_validator("id", mode="before")
    def validate_id(cls, v: int) -> int:
        if v in cls._ids:
            raise RecordError(f"The id {v} is not unique.")
        cls._ids.add(v)
        return v

    # TODO: confirm assumption that forced upper case is a good option for status field
    @field_validator("status", mode="before")
    def validate_status(cls, v: str) -> str:
        try:
            RecordStatus(v := v.upper())
        except ValueError as e:
            raise RecordError("Invalid status value") from e
        return v

    @field_validator("date_opened", "date_closed", mode="before")
    def validate_dates(cls, v: str | None, info: ValidationInfo) -> date | None:
        # TODO: confirm if the only expected date format is 'YYYY-MM-DD'
        if not v:
            return None
        try:
            record_date = date.fromisoformat(v)
        except ValueError as e:
            # TODO: try another format if confirmed
            raise RecordError(
                f'Invalid date format in "{info.field_name}" field. '
                f'Expected format is YYYY-MM-DD'
            ) from e
        return record_date

    @model_validator(mode="after")
    def validate_status_dates_non_empty(self) -> 'Record':
        err_message = deque()
        if self.status in ("OPEN", "BOTH") and not self.date_opened:
            err_message.append('"date_opened"')
        if self.status in ("CLOSED", "BOTH") and not self.date_closed:
            err_message.append('"date_closed"')
        if err_message:
            raise RecordError(
                f'{" and ".join(err_message)} required '
                f'for record with status "{self.status.value}"')
        return self

    @model_validator(mode="after")
    def validate_status_dates_empty(self) -> 'Record':
        # TODO: confirm assumption for opposite case of status/date
        #  status == open -> date_closed = null
        #  status == closed -> date_open = null
        err_message = deque()
        if self.status == RecordStatus.OPEN and self.date_closed:
            err_message.append('"date_closed"')
        if self.status == RecordStatus.CLOSED and self.date_opened:
            err_message.append('"date_opened"')
        if err_message:
            raise RecordError(
                f'{" and ".join(err_message)} should be empty'
                f' for record with status "{self.status.value}"')
        return self

    @model_validator(mode="after")
    def validate_status_both_chronological(self) -> 'Record':
        # TODO: confirm assumption for status BOTH
        #  date_opened <= date_closed
        if (self.status == RecordStatus.BOTH
                and self.date_opened
                and self.date_closed
                and self.date_opened > self.date_closed):
            raise RecordError(
                f'date_opened="{self.date_opened}" '
                f'can not be after date_closed="{self.date_closed}"')
        return self
