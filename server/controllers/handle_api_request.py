import json
from http.server import BaseHTTPRequestHandler

from server.controllers.api_methods import RouteToAudio, GetTrackForRoute, prepare_api_response
from server.controllers.controllers_utils import HTTP_BAD_REQUEST
from server.utils.logger import log

ROUTES = {
    "/get_track_for_route": GetTrackForRoute(),
    "/route_to_audio": RouteToAudio(),
}


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

            log(f"For path {self.handler.path} got {json_data}")
            return api_method(self.handler, json_data)
        except Exception as exp:
            error_msg = f"Exception happened : {exp}"
            prepare_api_response(self.handler, HTTP_BAD_REQUEST, error_msg)
            log(error_msg)
