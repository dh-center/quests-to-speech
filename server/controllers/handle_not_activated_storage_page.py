from http.server import BaseHTTPRequestHandler

from server.controllers.common_utils import HTTP_SERVICE_UNAVAILABLE


class NotActivatedStorageHandler:
    UNAVAILABILITY_MSG = "Storage is not initialized yet!"

    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler

    def handle(self):
        self.handler.send_response(HTTP_SERVICE_UNAVAILABLE)
        self.handler.send_header('Content-type', 'text/html')
        self.handler.end_headers()
        self.handler.wfile.write(str.encode(NotActivatedStorageHandler.UNAVAILABILITY_MSG))
