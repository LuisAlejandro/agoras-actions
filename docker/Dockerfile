# syntax=docker/dockerfile:1.4
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

ARG AGORAS_INSTALL_SPEC="agoras==2.1.1"

# The base image pins its security source to "stable-security", which now
# resolves to trixie (Debian 13) since bookworm is oldstable. That pulls
# jq/libjq1 from trixie (needs libc6 >= 2.38) while the image is bookworm
# (libc6 2.36), breaking apt. Pin the security source to bookworm-security.
RUN sed -i 's/stable-security/bookworm-security/' /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends jq git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install "${AGORAS_INSTALL_SPEC}" "PyNaCl"

ADD entrypoint.sh /entrypoint.sh
ADD execute.py /execute.py
ADD refresh_credentials.py /refresh_credentials.py
ADD github_secrets.py /github_secrets.py

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["test"]
