FROM dockershelf/python:3.10
LABEL maintainer "Luis Alejandro Martínez Faneyth <luis@collagelabs.org>"

RUN pip3 install https://github.com/LuisAlejandro/agoras/archive/develop.zip

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT "/entrypoint.sh"

CMD "daemon"