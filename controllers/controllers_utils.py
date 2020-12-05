from typing import List

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_SERVICE_UNAVAILABLE = 503

FIELD_ROUTE_JSON = 'route_json'
FIELD_ROUTE_ID = 'route_id'


def check_json_data(json_data, fields: List[str]) -> str:
    # check request
    if not json_data or not isinstance(json_data, dict):
        return "Can not read passed json"
    for field in fields:
        field_value = json_data[field]
        if not field_value:
            return f"{field} is not passed"
