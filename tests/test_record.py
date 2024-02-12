import pytest
from pydantic import ValidationError

from record import Record


def test_unique_id_validation():
    Record(id=0, status="OPEN", date_opened="2021-01-01", date_closed="", code="a1", description="descr")
    with pytest.raises(ValidationError) as excinfo:
        Record(id=0, status="OPEN", date_opened="2021-02-01", date_closed="", code="a2", description="descr")
    assert "The id 0 is not unique" in str(excinfo.value)


@pytest.mark.parametrize("id_, invalid_date", [
    (1, "01-01-2021"), (2, "2021/01/01"), (3, "01/01/2021"), (4, "20213001"), (5, "2021-13-01")])
def test_date_format_validation_invalid(id_, invalid_date):
    with pytest.raises(ValidationError):
        Record(id=id_, status="OPEN", date_opened=invalid_date, date_closed="", code="a1", description="descr")


@pytest.mark.parametrize("id_, valid_date", [(6, "1990-12-31"), (7, "2035-12-31")])
def test_date_format_validation_valid(id_, valid_date):
    assert Record(id=id_, status="OPEN", date_opened=valid_date, date_closed="", code="a1",
                  description="descr").model_dump_json()


@pytest.mark.parametrize("id_, status_, opened, closed, code, description", [
    (8, "OPEN", "", "2023-01-01", "a1", "opened_empty"),
    (9, "CLOSED", "2023-01-01", "", "a2", "closed_empty"),
    (10, "BOTH", "2023-01-01", "", "a3", "closed_empty"),
    (11, "BOTH", "", "2023-01-01", "a4", "opened_empty"),
    (12, "BOTH", "", "", "a5", "both_empty"),
    (13, "OPEN", "2023-01-01", "2023-01-01", "a5", "both_dates"),
    (14, "CLOSED", "2023-01-01", "2023-01-01", "a5", "both_dates"),

])
def test_status_date_nullability(id_, status_, opened, closed, code, description):
    with pytest.raises(ValidationError):
        Record(id=id_, status=status_, date_opened=opened, date_closed=closed, code=code, description=description)


def test_date_closed_after_date_opened():
    with pytest.raises(ValidationError) as excinfo:
        Record(id=15, status="BOTH", date_opened="2022-01-01", date_closed="2021-12-31", code="a1", description="descr")
    assert "can not be after date_closed" in str(excinfo.value)


@pytest.mark.parametrize("id_, status_, opened, closed, code, description", [
    (None, "BOTH", "2023-01-01", "2023-01-01", "a1", "id_missing"),
    (17, "", "2023-01-01", "2023-01-01", "a1", "status_missing"),
    (18, "BOTH", "", "2023-01-01", "a1", "date_opened_missing"),
    (19, "BOTH", "2023-01-01", "", "a1", "date_closed_missing"),
    (20, "BOTH", "2023-01-01", "2023-01-01", "", "code_missing"),
])
def test_status_required_fields_missing(id_, status_, opened, closed, code, description):
    with pytest.raises(ValidationError):
        Record(id=id_, status=status_, date_opened=opened, date_closed=closed, code=code, description=description)


@pytest.mark.parametrize("id_, status_, opened, closed, code, description", [
    (21, "BOTH", "2023-01-01", "2023-01-01", "a1", ""),
    (22, "BOTH", "2023-01-01", "2023-01-01", "a", "code_1_symbol"),
])
def test_status_not_required_fields(id_, status_, opened, closed, code, description):
    assert Record(id=id_, status=status_, date_opened=opened, date_closed=closed, code=code, description=description)
