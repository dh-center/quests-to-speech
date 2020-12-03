import json
from http.server import BaseHTTPRequestHandler

from server.controllers.common_utils import HTTP_BAD, HTTP_OK
from server.utils.logger import log

ROUTES = {
    "get_track_for_route": None,
    "route_to_audio": None,
}


class ApiHandler:
    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler

    def prepare(self, status: int):
        self.handler.send_response(status)
        self.handler.send_header('Content-type', 'application/json')
        self.handler.end_headers()

    def handle(self):
        try:
            content_length = int(self.handler.headers['content-length'])
            json_data = json.loads(self.handler.rfile.read(content_length).decode())
            # TODO submit task
            self.prepare(HTTP_OK)
            log(json_data)
        except Exception as exp:
            self.prepare(HTTP_BAD)
            msg = f"Exception happened : {exp}"
            self.handler.wfile.write(str.encode(msg))
            log(msg)
