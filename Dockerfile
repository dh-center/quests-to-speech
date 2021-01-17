FROM python:3.9-slim-buster
# FROM python:3.9-buster

WORKDIR /usr/src/app

RUN apt -y update
RUN apt -y install build-essential
RUN apt -y install ffmpeg

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8091

# add working directory to source roots
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app"

COPY . .

RUN ["chmod", "+x", "run_in_container.sh"]
ENTRYPOINT ["./run_in_container.sh"]


