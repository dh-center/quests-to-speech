import os
from typing import Dict, Optional

from app_source.app_settings import APP_SETTINGS
from app_source.logger import LOGGER


class StorageValue:
    """
        This class represents storage value with file
        and its content hash function's value.
        Hash function's value will be used for repetitive calls
        for the same route, as we will be able
        to get that the route has changed.
    """

    def __init__(self, text_hash: str, file_name: str):
        self.text_hash: str = text_hash
        self.file_name: str = file_name

    def __str__(self):
        return str((self.text_hash, self.file_name))

    def __repr__(self):
        return str(self)


class Mp3Storage:
    """
    Main class which is responsible for saving and checking
    that content was already processed.
    """

    def __init__(self):
        self._storage_dict: Dict[str, StorageValue] = {}
        self._activated: bool = False

    def activate_storage(self):
        """
        Scans through CONFIG.mp3_location and creates dict of files.
        with abstractly route_id -> [text_hash, file_name] mapping
        """
        LOGGER.log("Start storage activation...")
        Mp3Storage.clear_tmp_files()
        if not os.path.isdir(APP_SETTINGS.MP3_LOCATION):
            os.makedirs(APP_SETTINGS.MP3_LOCATION)
        for file_name in os.listdir(APP_SETTINGS.MP3_LOCATION):
            if not file_name.endswith('.mp3'):
                continue
            LOGGER.log(f"Found {file_name}")
            cropped_name = file_name[:-4]  # crop .mp3 part
            route_id, text_hash, created_time = cropped_name.split(APP_SETTINGS.FILE_PARTS_SEPARATOR)
            self._storage_dict[route_id] = StorageValue(text_hash, file_name)
        self._activated = True
        LOGGER.log("Storage activated.")

    def get_storage_dict(self) -> Dict[str, StorageValue]:
        """
        :return: dict with route_id -> StorageValue mapping
        """
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
            Mp3Storage.__delete_mp3_file(prev_value.file_name)
        self._storage_dict[route_id] = storage_value

    @staticmethod
    def clear_tmp_files():
        """
        Removes all temp files used for audio generation.
        """
        LOGGER.log("Clear tmp files...")
        for file_name in os.listdir(APP_SETTINGS.DATA_FOLDER):
            if file_name.startswith('tmp') and file_name.endswith(".raw"):
                Mp3Storage.__delete_temp_file(file_name)
                LOGGER.log(f"tmp file removed {file_name}")
        LOGGER.log("Clear tmp files finished")

    # private api (utils)

    @staticmethod
    def __delete_temp_file(file_name):
        """
        Convenience method to remove temp files from default storage.
        :param file_name: file to be removed
        """
        try:
            os.remove(os.path.join(APP_SETTINGS.DATA_FOLDER, file_name))
        except Exception as exp:
            LOGGER.log_error(f"Exception happened during tmp file {file_name} removal : {exp}")

    @staticmethod
    def __delete_mp3_file(file_name):
        """
        Convenience method to remove mp3 files.
        :param file_name: file to be removed
        """
        try:
            os.remove(os.path.join(APP_SETTINGS.MP3_LOCATION, file_name))
        except Exception as exp:
            LOGGER.log_error(f"Exception happened during mp3 file {file_name} removal : {exp}")


MP3_STORAGE = Mp3Storage()
