import os

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse

from app_source.app_settings import APP_SETTINGS
from app_source.app_utils import APP_MAIN_METHODS
from app_source.logger import LOGGER
from app_source.mp3_storage import MP3_STORAGE, StorageValue
from yandex_speech_kit.token_renewal import token_renew

# initialisation of main components
app = FastAPI()
MP3_STORAGE.activate_storage()
token_renew(forced=True)


# In this file all main controllers are kept

@app.get("/")
async def all_routes():
    """
    :return: all mapped routes
    """
    return MP3_STORAGE.get_storage_dict()


class RouteToSpeechRequestBody(BaseModel):
    """
    Main request entity with id of route and text
    """
    route_id: str
    ssml_text: str


@app.post("/route_to_speech")
async def route_to_speech(request_body: RouteToSpeechRequestBody):
    """
    :param request_body: route_id and text of route
    :return: audio file representation of given route
    """
    if len(request_body.ssml_text) > APP_SETTINGS.TEXT_LENGTH_LIMIT:
        return f"Too long ssml_text passed! (> {APP_SETTINGS.TEXT_LENGTH_LIMIT})"

    LOGGER.log(f"Got query in route to speech route_id: {request_body.route_id},"
               f" ssml_text: {request_body.ssml_text}")
    route_id, ssml_text = request_body.route_id, request_body.ssml_text

    text_hash = APP_MAIN_METHODS.hash_text(ssml_text)
    storage_value = MP3_STORAGE.get(route_id)
    if storage_value is not None and storage_value.text_hash == text_hash:
        file_name = storage_value.file_name
    else:
        file_name = APP_MAIN_METHODS.route_to_audio_file(route_id, ssml_text, text_hash)
        MP3_STORAGE.put(route_id, StorageValue(text_hash, file_name))

    return FileResponse(
        path=os.path.join(os.path.abspath(os.curdir),
                          APP_SETTINGS.MP3_LOCATION, file_name),
        media_type="audio/mpeg3",
        filename=file_name
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
