FROM dockershelf/python:3.10-bookworm

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL org.label-schema.build-date=${BUILD_DATE} \
      org.label-schema.name="agoras-actions" \
      org.label-schema.description="An Agoras image to allow for github actions usage" \
      org.label-schema.url="https://github.com/LuisAlejandro/agoras-actions" \
      org.label-schema.vcs-ref=${VCS_REF} \
      org.label-schema.vcs-url="https://github.com/LuisAlejandro/agoras-actions" \
      org.label-schema.vendor="Luis Alejandro Martínez Faneyth" \
      org.label-schema.version=${VERSION} \
      org.label-schema.schema-version="1.0.0-rc.1" \
      org.opencontainers.image.created=${BUILD_DATE} \
      org.opencontainers.image.title="agoras-actions" \
      org.opencontainers.image.description="An Agoras image to allow for github actions usage" \
      org.opencontainers.image.url="https://github.com/LuisAlejandro/agoras-actions" \
      org.opencontainers.image.revision=${VCS_REF} \
      org.opencontainers.image.source="https://github.com/LuisAlejandro/agoras-actions" \
      org.opencontainers.image.vendor="Luis Alejandro Martínez Faneyth" \
      org.opencontainers.image.version=${VERSION} \
      org.opencontainers.image.licenses="GPL-3.0" \
      maintainer="Luis Alejandro Martínez Faneyth <luis@luisalejandro.org>"

RUN apt-get update && apt-get install jq

RUN pip3 install agoras==1.1.1

ADD entrypoint.sh /entrypoint.sh
ADD execute.py /execute.py

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["test"]
