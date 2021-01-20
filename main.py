import os
from typing import Dict, Union, List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse

from app_source.app_settings import app_settings
from app_source.app_utils import app_main_methods
from app_source.json_paragraphs_merger import json_merger
from app_source.logger import main_logger
from app_source.mp3_storage import mp3_storage, StorageValue
from yandex_speech_kit.token_renewal import token_renew

# initialisation of main components
app = FastAPI()
mp3_storage.activate_storage()
token_renew(forced=True)


# In this file all main controllers are kept

@app.get("/")
async def all_routes():
    """
    :return: all mapped routes
    """
    return mp3_storage.get_storage_dict()


class RouteToSpeechRequestBody(BaseModel):
    """
       Main request entity with id of route and text
    """
    route_id: str
    ssml_text: Union[str, List, Dict]


@app.post("/route_to_speech")
async def route_to_speech(request_body: RouteToSpeechRequestBody):
    """
    :param request_body: route_id and text of route | or dict
    :return: audio file representation of given route
    """

    ssml_text = ""
    if isinstance(request_body.ssml_text, str):
        if len(request_body.ssml_text) > app_settings.TEXT_LENGTH_LIMIT:
            return f"Too long ssml_text passed! (> {app_settings.TEXT_LENGTH_LIMIT})"
        ssml_text = request_body.ssml_text
    else:
        ssml_text = json_merger.merge_json_to_text_for_yandex(request_body.ssml_text)

    main_logger.log(f"Got query in route to speech route_id: {request_body.route_id},"
                    f" ssml_text: {ssml_text}")
    route_id = request_body.route_id

    text_hash = app_main_methods.hash_text(ssml_text)
    storage_value = mp3_storage.get(route_id)
    if storage_value is not None and storage_value.text_hash == text_hash:
        file_name = storage_value.file_name
    else:
        file_name = app_main_methods.route_to_audio_file(route_id, ssml_text, text_hash)
        mp3_storage.put(route_id, StorageValue(text_hash, file_name))

    return FileResponse(
        path=os.path.join(os.path.abspath(os.curdir),
                          app_settings.MP3_LOCATION, file_name),
        media_type="audio/mpeg3",
        filename=file_name
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
