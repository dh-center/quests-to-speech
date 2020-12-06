FROM ubuntu:focal-20201106

WORKDIR /usr/src/app

# install libs
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN apt update -y
RUN apt install -y python3.8
RUN apt install -y python3-pip
RUN pip3 install requests pydub

ARG CONTAINER_APP_PORT_VAR=8081
ENV CONTAINER_APP_PORT=$CONTAINER_APP_PORT_VAR
EXPOSE $CONTAINER_APP_PORT_VAR

# add working directory to source roots
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/app"

COPY . .

RUN ["chmod", "+x", "run_in_container.sh"]
ENTRYPOINT ["./run_in_container.sh"]


