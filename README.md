## Requirements
* Reads the json file in data/input
* Puts the json object into a Pydantic Model representation of the data structure
* Writes the output to a new-line delimited json file

## Basic constrains
* If the object's status is `OPENED`, the `date_opened` field must be populated
* If the object's status is `CLOSED`, the `date_closed` field must be populated
* If the object's status is `BOTH`, both `date_opened` and `date_closed` must be populated
* The `id` field must be unique across the dataset
* String fields should have empty strings converted into a null value
Exception raised if any of the above are violated, it indicating which record caused the issue alongside the content of the record
