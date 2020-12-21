FROM python:3.9-slim-buster
# FROM python:3.9-buster

WORKDIR /usr/src/app

RUN apt -y update
RUN apt -y install ffmpeg

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ARG CONTAINER_APP_PORT_VAR=8081
ENV CONTAINER_APP_PORT=$CONTAINER_APP_PORT_VAR
EXPOSE $CONTAINER_APP_PORT_VAR

# add working directory to source roots
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app"

COPY . .

RUN ["chmod", "+x", "run_in_container.sh"]
ENTRYPOINT ["./run_in_container.sh"]


