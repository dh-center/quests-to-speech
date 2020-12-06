# quests-to-speech

Stack:
* Python 3.8
* `pip install requests pydub`
* `sudo apt install ffmpeg`
------------------------------------------

### API:
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

##### result:
* **OK** (OK 200) - accepted task for processing
* **ALREADY_DONE** (OK 200) - already have done task
* **ALREADY_HAVE_TASK** (CREATED 201) - already have task for processing
* **ERROR** - sth went wrong (with msg)
* **BAD REQUEST** (BAD_REQUEST 400) - not know or malformed request


#### /set_yandex_token (POST) with request body
```json
{
  "token": "<iam_token>"
}
```

##### result:
* **TOKEN_SET** (OK 200) - token set
* **BAD REQUEST** (BAD_REQUEST 400) - not know or malformed request