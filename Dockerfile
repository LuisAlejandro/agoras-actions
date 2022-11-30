FROM dockershelf/python:3.10
LABEL maintainer "Luis Alejandro Martínez Faneyth <luis@luisalejandro.org>"

RUN apt-get update && \
    apt-get install sudo python3.10-venv git make libyaml-dev

RUN ln -s /usr/bin/python3.10 /usr/bin/python

ADD requirements.txt requirements-dev.txt /root/
RUN pip3 install -r /root/requirements.txt -r /root/requirements-dev.txt
RUN rm -rf /root/requirements.txt /root/requirements-dev.txt

RUN echo "agoras-actions ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/agoras-actions
RUN useradd -ms /bin/bash agoras-actions

USER agoras-actions

RUN mkdir -p /home/agoras-actions/app

WORKDIR /home/agoras-actions/app

CMD tail -f /dev/null