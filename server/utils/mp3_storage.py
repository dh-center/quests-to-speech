from typing import Tuple

from server.utils.RWLock import RWLock
from server.utils.logger import log


class StorageValue:
    # VALUE states
    STATE_PROCESSING = "PROCESSING"
    STATE_BROKEN = "BROKEN"
    STATE_DONE = "DONE"

    def __init__(self, state: str, text_hash: str):
        self.state = state
        self.text_hash = text_hash
        self.future = None

    def cancel_future(self) -> bool:
        if self.future:
            return self.future.cancel()
        return True

    def destroy_value(self):
        # TODO remove file
        pass

    def is_broken(self):
        return self.state == StorageValue.STATE_BROKEN

    def is_done(self):
        return self.state == StorageValue.STATE_DONE

    def is_processed(self):
        return self.state == StorageValue.STATE_PROCESSING


class Mp3Storage:
    def __init__(self):
        self._storage_dict = {}
        self._activated = False
        self._rw_lock = RWLock()

    def activate_storage(self):
        log("Start storage activation...")
        # TODO parse mp3 files from folder
        self._activated = True
        log("Storage activated.")

    def get_or_create_value(self, key: str, text_hash: str) -> Tuple[bool, StorageValue]:
        value = self.get_value(key)
        if value and value.text_hash == text_hash and not value.is_broken():
            return False, value
        try:
            self._rw_lock.writer_acquire()
            value = self.get_value(key)
            if value and value.text_hash == text_hash and not value.is_broken():
                return False, value
            storage_value = StorageValue(StorageValue.STATE_PROCESSING, text_hash)
            self._storage_dict[key] = storage_value
            return True, storage_value
        finally:
            self._rw_lock.writer_release()

    def get_value(self, key: str) -> StorageValue:
        try:
            self._rw_lock.reader_acquire()
            return self._storage_dict[key]
        finally:
            self._rw_lock.reader_release()


MP3_STORAGE = Mp3Storage()
