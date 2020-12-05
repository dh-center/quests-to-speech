import textwrap
from http.server import BaseHTTPRequestHandler

from server.controllers.controllers_utils import HTTP_OK
from server.utils.mp3_storage import MP3_STORAGE


class WelcomePageHandler:
    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler

    def handle(self):
        self.handler.send_response(HTTP_OK)
        self.handler.send_header('Content-type', 'text/html')
        self.handler.end_headers()

        # TODO show all tracks stored
        list_elements = [
            f'<span style="color : red"><b>Route ID</b></span> : {route_id} --> <b>State</b> : {storage_value.state} ||  <b>Text Hash</b> : {storage_value.text_hash} || ' \
            f'<b>File</b> : <a href="/{storage_value.file_name}">{storage_value.file_name}</a>'
            for route_id, storage_value in MP3_STORAGE.get_dict_snapshot().items()
        ]
        self.html(textwrap.dedent(f"""
        <!DOCTYPE html>
        <html>
        <body>
        
        <h2>Storage snapshot: len {len(list_elements)}</h2>
        {self.ul(list_elements)}
        </body>
        </html>
"""))

    def ul(self, llist: list):
        html_list = "\n".join(f"<li>{el}</li>" for el in llist)
        return f"<ul>{html_list}</ul>"

    def html(self, text: str):
        self.handler.wfile.write(str.encode(text))
