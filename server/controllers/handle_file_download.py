import os
from http.server import BaseHTTPRequestHandler

from configs.app_config import CONFIG
from server.controllers.controllers_utils import HTTP_OK, HTTP_NOT_FOUND
from server.utils.logger import log, log_error


class FileDownloadHandler:
    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler

    def prepare(self, status: int):
        self.handler.send_response(status)
        self.handler.send_header('Content-type', 'application/json')
        self.handler.end_headers()

    def handle(self):
        mp3_file_name = self.handler.path.split("/")[-1]
        file_path = os.path.join(os.path.abspath(os.curdir), CONFIG.mp3_location, mp3_file_name)
        log(f"Serve file {file_path}")
        return self.mp3_serve(file_path, mp3_file_name)

    def mp3_serve(self, file_path, served_file_name):
        try:
            with open(file_path, 'rb') as file:
                size = os.path.getsize(file_path)
                self.handler.send_response(HTTP_OK)
                self.handler.send_header("Content-type", "audio/mpeg3")
                self.handler.send_header("Content-length", str(size))
                self.handler.send_header("Content-Disposition", f'filename="{served_file_name}"')
                self.handler.end_headers()
                while True:
                    block = file.read(CONFIG.socket_write_chunk_size)
                    if not block:
                        break
                    self.handler.wfile.write(block)
        except Exception as exp:
            self.handler.send_response(HTTP_NOT_FOUND)
            self.handler.end_headers()
            log_error(f"Exception happened on mp3 file serve {file_path} {exp}")
