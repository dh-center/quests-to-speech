from server.utils.logger import log


class Mp3Storage:
    def __init__(self):
        self._activated = False

    def activate_storage(self):
        log("\nStart storage activation...")
        # TODO parse mp3 files
        self._activated = True
        log("Storage activated.")


MP3_STORAGE = Mp3Storage()
