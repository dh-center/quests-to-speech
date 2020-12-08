import json
from http.server import BaseHTTPRequestHandler
from typing import Union, Dict

import server.utils.task_executor as executor
from configs.app_config import CONFIG
from configs.yandex_speech_kit_config import YandexConfig
from server.controllers.controllers_utils import HTTP_BAD_REQUEST, FIELD_ROUTE_JSON, FIELD_ROUTE_ID, \
    check_json_data, HTTP_OK, HTTP_CREATED, HTTP_NOT_FOUND, FIELD_YANDEX_PASSPORT_TOKEN, \
    FIELD_YANDEX_FOLDER_ID
from server.utils.logger import log, log_error
from server.utils.mp3_storage import MP3_STORAGE
from server.utils.speech_processor import CURRENT_PROCESSOR
from server.utils.text_hashing import hash_text
from server.utils.token_renewal import renew_token


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
            return prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

        route_json = json_data[FIELD_ROUTE_JSON]
        if not isinstance(route_json, dict):
            error_msg = "Invalid route_json"
            return prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

        text = CURRENT_PROCESSOR.get_json_merger()(route_json)

        route_id = json_data[FIELD_ROUTE_ID]
        log(f"For Route ID : {route_id} got {route_json} and merged it to :\n {text}")

        if not text:
            error_msg = f"No text provided"
            return prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

        if len(text) > CONFIG.text_length_limit:
            error_msg = f"Too large text (> {CONFIG.text_length_limit} characters)"
            return prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

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
            return prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

        route_id = json_data[FIELD_ROUTE_ID]
        storage_value = MP3_STORAGE.get_value(route_id)
        if not storage_value:
            return prepare_api_response(handler, HTTP_NOT_FOUND, "NOT_FOUND")
        if storage_value.is_broken():
            return prepare_api_response(handler, HTTP_OK, "BROKEN")
        if storage_value.is_processed():
            return prepare_api_response(handler, HTTP_OK, "PROCESSING")
        if storage_value.is_done():
            return prepare_api_response(handler, HTTP_OK, {"msg": "OK", "link": f"/{storage_value.file_name}"})

        log(f"Sth went wrong {route_id}")
        return prepare_api_response(handler, HTTP_BAD_REQUEST, "Sth went wrong")


class SetYandexToken(ApiMethod):

    def __call__(self, handler: BaseHTTPRequestHandler, json_data):
        # check request
        error_msg = check_json_data(json_data, [FIELD_YANDEX_PASSPORT_TOKEN, FIELD_YANDEX_FOLDER_ID])
        if error_msg:
            return prepare_api_response(handler, HTTP_BAD_REQUEST, error_msg)

        passport_token = json_data[FIELD_YANDEX_PASSPORT_TOKEN]
        folder_id = json_data[FIELD_YANDEX_FOLDER_ID]
        YandexConfig.set_passport_token(passport_token)
        YandexConfig.set_folder_id(folder_id)
        log(f"Yandex passport token : {passport_token} and folder id reset {folder_id}")
        try:
            renew_token()
        except Exception as exp:
            log_error(f"Can not authenticated in Yandex {exp}")
            return prepare_api_response(handler, HTTP_OK, "NOT AUTHENTICATED")
        return prepare_api_response(handler, HTTP_OK, "AUTHENTICATED")
