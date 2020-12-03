# quests-to-speech

Stack:
* Python 3.8

------------------------------------------

### API:
#### /get_track_for_route (POST)
1. route_id : string
2. passage_idx : int

##### result:
* **OK** - link to audio
* **PROCESSING** - come latter
* **NOT FOUND** - please route_to_audio first

#### /route_to_audio (POST)
1. route_id: string
2. passage_idx: idx
3. text : string

##### result:
* **OK**
* **ERROR** - sth went wrong (with msg)