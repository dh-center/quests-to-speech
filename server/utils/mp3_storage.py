import os
import time
from threading import Thread
from typing import Tuple, Dict

from configs.app_config import CONFIG
from server.utils.RWLock import RWLock
from server.utils.logger import log, log_error


class StorageValue:
    # VALUE states
    STATE_PROCESSING = "PROCESSING"
    STATE_BROKEN = "BROKEN"
    STATE_DONE = "DONE"

    def __init__(self, state: str, text_hash: str):
        self.state = state
        self.text_hash = text_hash
        self.file_name = None
        self.future = None
        self.created_time = None

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

    def __str__(self):
        future_info = "None"
        future = self.future
        if future:
            future_info = "done" if future.done() else "not_yet_done"
        return f"{self.state} | {self.file_name} | {future_info}"

    def __repr__(self):
        return str(self)


class Mp3Storage:
    def __init__(self):
        self._storage_dict: Dict[str, StorageValue] = {}
        self._activated: bool = False
        self._rw_lock: RWLock = RWLock()

    def activate_storage(self):
        log("Start storage activation...")
        try:
            self._rw_lock.writer_acquire()
            for file_name in os.listdir(CONFIG.mp3_location):
                if not file_name.endswith('.mp3'):
                    continue
                log(f"Found {file_name}")
                cropped_name = file_name[:-4]  # crop .mp3 part
                route_id, text_hash, created_time = cropped_name.split(CONFIG.file_parts_separator)
                storage_value = StorageValue(StorageValue.STATE_DONE, text_hash)
                storage_value.file_name = file_name
                storage_value.created_time = float(created_time)
                prev_value = self._storage_dict.get(route_id, None)
                if prev_value:
                    if storage_value.created_time > prev_value.created_time:
                        self._storage_dict[route_id] = storage_value
                        log(f"Overwritten {prev_value}")
                    else:
                        log(f"Skipped {storage_value}")
                else:
                    self._storage_dict[route_id] = storage_value
        finally:
            self._rw_lock.writer_release()
        self._activated = True
        log("Storage activated.")

    @property
    def is_activated(self):
        return self._activated

    def get_or_create_value(self, key: str, text_hash: str) -> Tuple[bool, StorageValue]:
        value = self.get_value(key)
        if value and value.text_hash == text_hash and not value.is_broken():
            return False, value
        try:
            self._rw_lock.writer_acquire()
            value = self._storage_dict.get(key, None)
            if value and value.text_hash == text_hash and not value.is_broken():
                return False, value
            if value:
                value.cancel_future()
            storage_value = StorageValue(StorageValue.STATE_PROCESSING, text_hash)
            self._storage_dict[key] = storage_value
            return True, storage_value
        finally:
            self._rw_lock.writer_release()

    def get_value(self, key: str) -> StorageValue:
        try:
            self._rw_lock.reader_acquire()
            return self._storage_dict.get(key, None)
        finally:
            self._rw_lock.reader_release()

    def get_all_keys_in_use(self) -> Tuple[list, float]:
        try:
            self._rw_lock.reader_acquire()
            return list(self._storage_dict.keys()), time.time()
        finally:
            self._rw_lock.reader_release()

    def get_dict_snapshot(self) -> Dict[str, StorageValue]:
        try:
            self._rw_lock.reader_acquire()
            return {k: v for k, v in self._storage_dict.items()}
        finally:
            self._rw_lock.reader_release()

    @staticmethod
    def clear_tmp_files():
        log("Clear tmp files...")
        for file_name in os.listdir(CONFIG.data_folder):
            if file_name.startswith('tmp') and file_name.endswith(".raw"):
                delete_tmp_file(file_name)
                log(f"tmp file removed {file_name}")
        log("Clear tmp files finished")


MP3_STORAGE = Mp3Storage()


def delete_tmp_file(file_path):
    try:
        os.remove(os.path.join(CONFIG.data_folder, file_path))
    except Exception as exp:
        log_error(f"Exception happened during tmp file {file_path} removal : {exp}")


def delete_mp3_file(file_path):
    try:
        os.remove(os.path.join(CONFIG.mp3_location, file_path))
    except Exception as exp:
        log_error(f"Exception happened during file {file_path} removal : {exp}")


def clean_task():
    log("Clean task initialized")
    prev_run = 0
    while True:
        now = time.time()
        already_met = {}
        if not MP3_STORAGE.is_activated or now - prev_run < CONFIG.clean_storage_interval:
            time.sleep(CONFIG.clean_storage_interval)
        try:
            keys, snapshot_time = MP3_STORAGE.get_all_keys_in_use()
            for file_name in os.listdir(CONFIG.mp3_location):
                if not file_name.endswith('.mp3'):
                    continue
                cropped_name = file_name[:-4]  # crop .mp3 part
                route_id, text_hash, created_time = cropped_name.split(CONFIG.file_parts_separator)
                created_time = float(created_time)
                if route_id not in keys:
                    if created_time <= snapshot_time:
                        delete_mp3_file(file_name)
                        log(f"Removed unused file on clean {file_name}")
                    continue
                if route_id in already_met:
                    _, _, prev_created_time, prev_file_name = already_met[route_id]
                    if prev_created_time > created_time:
                        delete_mp3_file(file_name)
                        log(f"Removed stale file on clean {file_name}")
                    else:
                        delete_mp3_file(prev_file_name)
                        log(f"Removed stale file on clean {prev_file_name}")
                        already_met[route_id] = (route_id, text_hash, created_time, file_name)
                else:
                    already_met[route_id] = (route_id, text_hash, created_time, file_name)

            prev_run = now
        except Exception as exp:
            log_error(f"Exception happened during clean : {exp}")


__CLEANER_THREAD = Thread(
    name="StorageCleaner-thread",
    target=clean_task,
    daemon=True
)
__CLEANER_THREAD.start()
