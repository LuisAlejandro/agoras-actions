FROM dockershelf/python:3.12
LABEL maintainer="Luis Alejandro Martínez Faneyth <luis@luisalejandro.org>"

ARG UID=1000
ARG GID=1000

RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo python3-venv git make libyaml-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install "agoras==2.0.4"

COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip3 install -r /tmp/requirements-dev.txt && rm /tmp/requirements-dev.txt

RUN EXISTUSER=$(getent passwd | awk -F':' '$3 == '$UID' {print $1}') && \
    [ -n "${EXISTUSER}" ] && deluser ${EXISTUSER} || true

RUN EXISTGROUP=$(getent group | awk -F':' '$3 == '$GID' {print $1}') && \
    [ -n "${EXISTGROUP}" ] && delgroup ${EXISTGROUP} || true

RUN groupadd -g "${GID}" agoras || true
RUN useradd -u "${UID}" -g "${GID}" -ms /bin/bash agoras
RUN echo "agoras ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/agoras

USER agoras

RUN mkdir -p /home/agoras/app /home/agoras/.cache/pip

WORKDIR /home/agoras/app

CMD ["tail", "-f", "/dev/null"]
