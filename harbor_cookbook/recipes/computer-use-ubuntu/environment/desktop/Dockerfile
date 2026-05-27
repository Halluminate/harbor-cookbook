FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99
ENV HOME=/home/model
ENV USER=model
ENV LOGNAME=model
ENV XDG_RUNTIME_DIR=/tmp/runtime-model
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gnupg \
    software-properties-common \
    && install -d -m 0755 /etc/apt/keyrings \
    && curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-linux.gpg \
    && chmod 0644 /etc/apt/keyrings/google-linux.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-linux.gpg] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && add-apt-repository -y ppa:mozillateam/ppa \
    && printf "Package: thunderbird*\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001\n" > /etc/apt/preferences.d/mozillateam-thunderbird \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    dbus-x11 \
    evince \
    file-roller \
    git \
    gnome-calculator \
    google-chrome-stable \
    libreoffice-calc \
    libreoffice-impress \
    libreoffice-writer \
    mousepad \
    nano \
    novnc \
    python3 \
    python3-pip \
    python3-tk \
    python3-venv \
    ristretto \
    scrot \
    sudo \
    thunderbird \
    vim-tiny \
    websockify \
    wget \
    xfce4 \
    xfce4-terminal \
    xterm \
    xvfb \
    x11vnc \
    xdotool \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv "${VIRTUAL_ENV}" \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir fastmcp

RUN printf '%s\n' \
        '#!/bin/sh' \
        'exec /usr/bin/google-chrome-stable --no-sandbox --disable-dev-shm-usage "$@"' \
        > /usr/local/bin/google-chrome \
    && chmod +x /usr/local/bin/google-chrome \
    && ln -sf /usr/local/bin/google-chrome /usr/local/bin/google-chrome-stable \
    && ln -sf /usr/local/bin/google-chrome /usr/local/bin/chrome \
    && sed -i 's|Exec=/usr/bin/google-chrome-stable|Exec=/usr/bin/google-chrome-stable --no-sandbox --disable-dev-shm-usage|g' /usr/share/applications/google-chrome.desktop

RUN existing_group="$(getent group 1000 | cut -d: -f1)" \
    && if [ -n "$existing_group" ] && [ "$existing_group" != "model" ]; then groupmod --new-name model "$existing_group"; elif [ -z "$existing_group" ]; then groupadd --gid 1000 model; fi \
    && existing_user="$(getent passwd 1000 | cut -d: -f1)" \
    && if [ -n "$existing_user" ] && [ "$existing_user" != "model" ]; then usermod --login model --home /home/model --shell /bin/bash "$existing_user"; elif [ -z "$existing_user" ]; then useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash model; fi \
    && echo "model:model" | chpasswd \
    && install -d -o model -g model /home/model/Desktop /home/model/Downloads "${XDG_RUNTIME_DIR}" \
    && chmod 700 "${XDG_RUNTIME_DIR}" \
    && mkdir -p /tmp/.X11-unix \
    && chmod 1777 /tmp /tmp/.X11-unix

WORKDIR /app

COPY server.py .
COPY challenge.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh \
    && chown -R model:model /app /home/model "${XDG_RUNTIME_DIR}"

EXPOSE 8000 6080

USER model

CMD ["./entrypoint.sh"]
