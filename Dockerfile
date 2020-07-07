FROM python:3.7-slim-buster as ge-build

COPY requirements-base.txt requirements-base.txt
RUN pip wheel --wheel-dir=dist -r requirements-base.txt


FROM python:3.7-slim-buster as base

ARG REVISION
ARG CREATED
ARG GE_VER

LABEL org.opencontainers.image.authors="engineering@bera.dev"
LABEL org.opencontainers.image.created=${CREATED}
LABEL org.opencontainers.image.documentation="https://github.com/bera/wemmick"
LABEL org.opencontainers.image.licenses="https://github.com/bera/wemmick/blob/main/LICENSE"
LABEL org.opencontainers.image.revision=${REVISION}
LABEL org.opencontainers.image.source="https://github.com/bera/wemmick"
LABEL org.opencontainers.image.url="https://github.com/bera/wemmick"
LABEL org.opencontainers.image.vendor="BERA"
LABEL org.opencontainers.image.version=${GE_VER}

RUN groupadd -r ge && useradd -r -m -g ge ge

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1


FROM base as ge

LABEL org.opencontainers.image.title="Great Expectations"
LABEL org.opencontainers.image.description="Great Expectations runtime image"

COPY --from=ge-build /dist/*.whl /tmp/dist/
RUN pip install --no-index --find-links=/tmp/dist/ \
      great_expectations \
      && rm -rf /tmp/dist

WORKDIR /home/ge/project
ENTRYPOINT ["great_expectations"]


## piggyback on ge-build's cache
FROM ge-build as wemmick-build
COPY . .
RUN pip wheel --wheel-dir=dist -e .


FROM base as wemmick

LABEL org.opencontainers.image.title="Wemmick"
LABEL org.opencontainers.image.description="BERA's Great Expectations runtime image"

COPY --from=wemmick-build /dist/*.whl /tmp/dist/
RUN pip install --no-index --find-links=/tmp/dist/ wemmick \
      && rm -rf /tmp/dist
COPY requirements-http.txt /tmp/
RUN pip install -r /tmp/requirements-http.txt \
    && rm -rf /tmp/requirements-http.txt
COPY ./src/wemmick/server /app

# Defaults overridden by Google Cloud Run
ENV HOST="0.0.0.0" \
    PORT=8080

WORKDIR /home/ge/project
ENTRYPOINT ["wemmick"]
# Run server: get PORT and HOST via python and run uvicorn programatically
#ENTRYPOINT ["/app/start_server.py"]
