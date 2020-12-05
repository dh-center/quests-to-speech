import json
from http.server import BaseHTTPRequestHandler
from typing import Union, Dict

import server.utils.task_executor as executor
from server.controllers.controllers_utils import HTTP_BAD_REQUEST, FIELD_ROUTE_JSON, FIELD_ROUTE_ID, \
    check_json_data, HTTP_OK, HTTP_CREATED, HTTP_NO_CONTENT, HTTP_NOT_FOUND
from server.utils.json_merger import merge_json_to_text
from server.utils.mp3_storage import MP3_STORAGE
from server.utils.text_hashing import hash_text


def prepare_api_response(handler: BaseHTTPRequestHandler, status: int, msg: Union[str, Dict] = None):
    handler.send_response(status)
    handler.send_header('Content-type', 'application/json')
    handler.end_headers()
    if isinstance(msg, str):
        handler.wfile.write(json.dumps({"msg": msg}).encode())
    elif isinstance(msg, dict):
        handler.wfile.write(json.dumps(msg).encode())


class ApiMethod:

    def __call__(self, handler: BaseHTTPRequestHandler, json_data):
        raise NotImplemented("")


class RouteToAudio(ApiMethod):
    def __call__(self, handler: BaseHTTPRequestHandler, json_data):
        # check request
        error_msg = check_json_data(json_data, [FIELD_ROUTE_ID, FIELD_ROUTE_JSON])
        if error_msg:
            prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

        route_json = json_data[FIELD_ROUTE_JSON]
        if not isinstance(route_json, dict):
            error_msg = "Invalid route_json"
            prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

        route_id = json_data[FIELD_ROUTE_ID]
        text = merge_json_to_text(route_json)
        text_hash = hash_text(text)

        (is_created, value) = MP3_STORAGE.get_or_create_value(route_id, text_hash)

        # check for repeated requests
        if not is_created:
            if value.is_done():
                return prepare_api_response(handler, HTTP_OK, "ALREADY_DONE")
            elif value.is_processed():
                return prepare_api_response(handler, HTTP_CREATED, "ALREADY_HAVE_TASK")

        value.future = executor.submit(
            executor.route_to_audio_task, executor.route_to_audio_callback, value, route_id, text, text_hash
        )

        return prepare_api_response(handler, HTTP_OK, "OK")


class GetTrackForRoute(ApiMethod):

    def __call__(self, handler: BaseHTTPRequestHandler, json_data):
        # check request
        error_msg = check_json_data(json_data, [FIELD_ROUTE_ID])
        if error_msg:
            prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

        route_id = json_data[FIELD_ROUTE_ID]
        storage_value = MP3_STORAGE.get_value(route_id)
        if not storage_value:
            return prepare_api_response(handler, HTTP_NOT_FOUND, "NOT_FOUND")
        if storage_value.is_broken():
            return prepare_api_response(handler, HTTP_NO_CONTENT, "BROKEN")
        if storage_value.is_processed():
            return prepare_api_response(handler, HTTP_OK, "PROCESSING")
        if storage_value.is_done():
            return prepare_api_response(handler, HTTP_OK, {"msg": "OK", "link": f"/{storage_value.file_name}"})
        return "GetTrackForRoute"
