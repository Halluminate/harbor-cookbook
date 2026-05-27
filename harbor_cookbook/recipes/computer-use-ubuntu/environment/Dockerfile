FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

ENV HOME=/home/model
ENV USER=model
ENV LOGNAME=model

RUN existing_group="$(getent group 1000 | cut -d: -f1)" \
    && if [ -n "$existing_group" ] && [ "$existing_group" != "model" ]; then groupmod --new-name model "$existing_group"; elif [ -z "$existing_group" ]; then groupadd --gid 1000 model; fi \
    && existing_user="$(getent passwd 1000 | cut -d: -f1)" \
    && if [ -n "$existing_user" ] && [ "$existing_user" != "model" ]; then usermod --login model --home /home/model --shell /bin/bash "$existing_user"; elif [ -z "$existing_user" ]; then useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash model; fi \
    && echo "model:model" | chpasswd \
    && install -d -o model -g model /app /home/model

WORKDIR /app

USER model
