import os

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse

from app_source.app_settings import settings
from app_source.app_utils import hash_text, route_to_audio
from app_source.mp3_storage import MP3_STORAGE, StorageValue
from yandex_speech_kit.token_renewal import renew_token

app = FastAPI()
MP3_STORAGE.activate_storage()
renew_token()


@app.get("/")
async def all_routes():
    return MP3_STORAGE.get_storage_dict()


class RouteToSpeechRequestBody(BaseModel):
    route_id: str
    text: str


@app.post("/route_to_speech")
async def route_to_speech(request_body: RouteToSpeechRequestBody):
    if len(request_body.text) > settings.text_length_limit:
        return f"Too long text passed! (> {settings.text_length_limit})"

    route_id, text = request_body.route_id, request_body.text

    text_hash = hash_text(text)
    storage_value = MP3_STORAGE.get(route_id)
    if storage_value is not None and storage_value.text_hash == text_hash:
        file_name = storage_value.file_name
    else:
        file_name = route_to_audio(route_id, text, text_hash)
        MP3_STORAGE.put(route_id, StorageValue(text_hash, file_name))

    return FileResponse(
        path=os.path.join(os.path.abspath(os.curdir), settings.mp3_location, file_name),
        media_type="audio/mpeg3",
        filename=file_name
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8091, log_level="info")
