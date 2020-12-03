import json
from http.server import BaseHTTPRequestHandler

import server.utils.task_executor as executor
from server.controllers.controllers_utils import HTTP_BAD_REQUEST, FIELD_ROUTE_JSON, FIELD_ROUTE_ID, \
    check_json_data, HTTP_OK, HTTP_CREATED
from server.utils.json_merger import merge_json_to_text
from server.utils.mp3_storage import MP3_STORAGE, StorageValue
from server.utils.text_hashing import hash_text


def prepare_api_response(handler: BaseHTTPRequestHandler, status: int, msg: str = None):
    handler.send_response(status)
    handler.send_header('Content-type', 'application/json')
    handler.end_headers()
    if msg:
        handler.wfile.write(json.dumps({"msg": msg}).encode())


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
        text = merge_json_to_text(json)
        text_hash = hash_text(text)

        (is_created, value) = MP3_STORAGE.get_or_create_value(route_id, text_hash)

        # check for repeated requests
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
        return "GetTrackForRoute"
