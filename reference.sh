#!/bin/sh

# Run
#docker run -it --entrypoint bash dh-center/quest_to_speech:1.0
#docker exec -it <container-name-or-id> bash
#docker run -it --name <WHATEVER> -p <LOCAL_PORT>:<CONTAINER_PORT> -v <LOCAL_PATH>:<CONTAINER_PATH> -d <IMAGE>:<TAG>

docker run -it -p 8091:8081 -v /home/kinmanz/PycharmProjects/quests-to-speech/tmp:/usr/src/app/data-folder -d dh-center/quest_to_speech:1.0
# or
docker-compose up