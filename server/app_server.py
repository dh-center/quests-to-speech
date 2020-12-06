import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import server.utils.task_executor as executor
from configs.app_config import CONFIG
from server.controllers.handle_api_request import ApiHandler
from server.controllers.handle_file_download import FileDownloadHandler
from server.controllers.handle_not_activated_storage_page import NotActivatedStorageHandler
from server.controllers.handle_welcome_page import WelcomePageHandler
from server.utils.logger import log
from server.utils.mp3_storage import MP3_STORAGE


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        log(f"GET request received {self.path}")
        if not MP3_STORAGE.is_activated:
            return NotActivatedStorageHandler(self).handle()
        if self.path.endswith(".mp3"):
            return FileDownloadHandler(self).handle()
        return WelcomePageHandler(self).handle()

    def do_POST(self):
        log(f"POST request received {self.path}")
        if not MP3_STORAGE.is_activated:
            return NotActivatedStorageHandler(self).handle()
        return ApiHandler(self).handle()


log(f"Config : {CONFIG}\n")
log("Starting app...")
log(f"Absolute root path : {os.path.abspath(os.curdir)}")
server = None
try:
    server = ThreadingHTTPServer(('', int(CONFIG.port_number)), RequestHandler)
    log(f"Started httpserver on port : {CONFIG.port_number}")

    # check data-folder/mp3 exist and create if not
    if os.path.isdir(CONFIG.mp3_location):
        log(f"Data folder : {CONFIG.mp3_location} exist.")
    else:
        os.makedirs(CONFIG.mp3_location)
        log(f"Created data folder : {CONFIG.mp3_location}.")
    log(f"Absolute folder data folder path : {os.path.abspath(CONFIG.mp3_location)}\n")

    # activate file storage
    MP3_STORAGE.activate_storage()

    # Wait forever for incoming http requests
    server.serve_forever()
except Exception as exp:
    log(exp)
    executor.shutdown()
    if server:
        server.socket.close()
        server.server_close()
