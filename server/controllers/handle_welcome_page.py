from http.server import BaseHTTPRequestHandler

from server.controllers.common_utils import HTTP_OK


class WelcomePageHandler:
    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler

    def handle(self):
        self.handler.send_response(HTTP_OK)
        self.handler.send_header('Content-type', 'text/html')
        self.handler.end_headers()

        # TODO show all tracks stored
        self.handler.wfile.write(str.encode("Hello World !"))
