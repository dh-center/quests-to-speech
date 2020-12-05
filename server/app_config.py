import os
from collections import namedtuple

# to create constant fields

__Config = namedtuple(
    '__Config', [
        # Server
        'port_number',
        # Folders
        'data_folder',
        'mp3_location',
        # Executor
        'concurrency_lvl',
        # Mp3 server
        'socket_write_chunk_size',
        # Storage
        'clean_storage_interval',
        'file_parts_separator',
        # Speech processor
        'speech_processor',
    ]
)
DATA_FOLDER = "data-folder"

CONFIG = __Config(
    # Server
    port_number=8080,
    # Folders
    data_folder=DATA_FOLDER,
    mp3_location=os.path.join(DATA_FOLDER, "mp3"),
    # Executor
    concurrency_lvl=10,
    # Mp3 server
    socket_write_chunk_size=4 * 1024,  # memory page size
    # Storage
    clean_storage_interval=60,
    file_parts_separator="$$",
    # Speech processor
    speech_processor="Dummy"
    # speech_processor="Yandex"
)
