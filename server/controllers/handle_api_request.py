import functools
import json
from http.server import BaseHTTPRequestHandler

from server.controllers.api_methods import RouteToAudio, GetTrackForRoute, prepare_api_response, SetYandexToken, \
    ApiMethod
from server.controllers.controllers_utils import HTTP_BAD_REQUEST
from server.utils.logger import log, log_error

# Mapping to another handler of endpoint query
ROUTES = {
    "/get_track_for_route": GetTrackForRoute(),
    "/route_to_audio": RouteToAudio(),
    "/set_yandex_token": SetYandexToken(),
}


def request_mapping(request_url: str = ""):
    if request_url == "":
        raise ValueError("Provide request url!")
    if request_url in ROUTES:
        raise ValueError("Request url is already taken!")

    def dec(func):
        if func is None:
            raise ValueError("callback is None!")
        method = functools.wraps(func)(ApiMethod())
        method._to_replace = func
        ROUTES[request_url] = method

    return dec


@request_mapping("/heart_beat")
def heart_beat(handler: BaseHTTPRequestHandler, json_data):
    return prepare_api_response(handler, 200, "heart_beat")


class ApiHandler:
    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler

    def handle(self):
        try:
            api_method = ROUTES[self.handler.path]
            if not api_method:
                return prepare_api_response(self.handler, HTTP_BAD_REQUEST)
            content_length = int(self.handler.headers['content-length'])
            json_data = json.loads(self.handler.rfile.read(content_length).decode())

            log(f"For path {self.handler.path} chose {api_method} got {json_data}")
            return api_method(self.handler, json_data)
        except Exception as exp:
            error_msg = f"Exception happened : {exp}"
            log_error(error_msg)
            return prepare_api_response(self.handler, HTTP_BAD_REQUEST, error_msg)
