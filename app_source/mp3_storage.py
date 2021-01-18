import os
from typing import Dict, Optional

from app_source.app_settings import settings
from app_source.logger import log, log_error


class StorageValue:
    """
        This class represents storage value with file and its content hash function's value.
        Hash function's value will be used for repetitive calls for the same route, as we will be able
        to get that query has changed.
    """

    def __init__(self, text_hash: str, file_name: str):
        self.text_hash: str = text_hash
        self.file_name: str = file_name

    def __str__(self):
        return str((self.text_hash, self.file_name))

    def __repr__(self):
        return str(self)


class Mp3Storage:
    def __init__(self):
        self._storage_dict: Dict[str, StorageValue] = {}
        self._activated: bool = False

    def activate_storage(self):
        """
        Scans through CONFIG.mp3_location and creates dict of files.
        with abstractly route_id -> [text_hash, file_name] mapping
        """
        log("Start storage activation...")
        Mp3Storage.clear_tmp_files()
        if not os.path.isdir(settings.mp3_location):
            os.makedirs(settings.mp3_location)
        for file_name in os.listdir(settings.mp3_location):
            if not file_name.endswith('.mp3'):
                continue
            log(f"Found {file_name}")
            cropped_name = file_name[:-4]  # crop .mp3 part
            route_id, text_hash, created_time = cropped_name.split(settings.file_parts_separator)
            self._storage_dict[route_id] = StorageValue(text_hash, file_name)
        self._activated = True
        log("Storage activated.")

    def get_storage_dict(self) -> Dict[str, StorageValue]:
        return dict(**self._storage_dict)

    def get(self, route_id: str) -> Optional[StorageValue]:
        """
        :param route_id: to get StorageValue by
        :return: StorageValue for this route_id or None if it is absent
        """
        return self._storage_dict.get(route_id, None)

    def put(self, route_id: str, storage_value: StorageValue):
        """
        :param route_id: to put StorageValue by (as key)
        :param storage_value:  to associate with given route_id (as value)
        """
        prev_value = self._storage_dict.get(route_id, None)
        if prev_value:
            delete_mp3_file(prev_value.file_name)
        self._storage_dict[route_id] = storage_value

    @staticmethod
    def clear_tmp_files():
        """
        Removes all temp files used for audio generation.
        """
        log("Clear tmp files...")
        for file_name in os.listdir(settings.data_folder):
            if file_name.startswith('tmp') and file_name.endswith(".raw"):
                delete_tmp_file(file_name)
                log(f"tmp file removed {file_name}")
        log("Clear tmp files finished")


def delete_tmp_file(file_path):
    try:
        os.remove(os.path.join(settings.data_folder, file_path))
    except Exception as exp:
        log_error(f"Exception happened during tmp file {file_path} removal : {exp}")


def delete_mp3_file(file_name):
    try:
        os.remove(os.path.join(settings.mp3_location, file_name))
    except Exception as exp:
        log_error(f"Exception happened during file {file_name} removal : {exp}")


MP3_STORAGE = Mp3Storage()
