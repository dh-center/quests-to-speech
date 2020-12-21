# quests-to-speech

Stack:
* Python 3.8
* `pip install requests pydub`
* `sudo apt install ffmpeg` or `brew install ffmpeg` for mac
------------------------------------------

### API: 
(Check `quest-to-speech-examples.postman_collection.json` at postman)
#### /get_track_for_route (POST) with request body
```json
{
    "route_id": "<string>"
}
```

##### response body:
* **OK** (OK 200) - link to audio
* **PROCESSING** (OK 200) - come latter
* **BROKEN** (OK 200) - had the task but sth went wrong
* **NOT FOUND** (NOT_FOUND 404) - please `/route_to_audio` first
* **BAD REQUEST** (BAD_REQUEST 400) - not know or malformed request

#### /route_to_audio (POST) with request body
```json
{
    "route_id": "<string>",
    "route_json": {...}
}
```
или
```json
{
    "route_id": "<string>",
    "route_text": "ssml text goes here"
}
```
##### result:
* **OK** (OK 200) - accepted task for processing
* **ALREADY_DONE** (OK 200) - already have done task
* **ALREADY_HAVE_TASK** (CREATED 201) - already have task for processing
* **ERROR** - sth went wrong (with msg)
* **BAD REQUEST** (BAD_REQUEST 400) - not know or malformed request


#### /set_yandex_token (POST) with request body
```json
{
  "passport_token": "<passport_token>",
  "folder_id": "<folder_id>"
}
```

##### result:
* **AUTHENTICATED** (OK 200)
* **NOT AUTHENTICATED** (OK 200)
* **BAD REQUEST** (BAD_REQUEST 400) - not know or malformed request