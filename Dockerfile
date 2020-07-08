# 322 mb
FROM python:3.7-slim-buster as ge-build

# use same version of ge as wemmick, not neccesarily the latest version
# unlike `head -n1 requirements-base.txt` this grep does not require
# first line placement and will fail if great_expectations is ommitted.
COPY requirements-base.txt requirements-base.txt
RUN GE_VER=$(grep "^great_expectations" requirements-base.txt | cut -d'=' -f3-) \
    && pip wheel --wheel-dir=dist "great_expectations==${GE_VER}"

# 156 mb
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
WORKDIR /ge

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 539 mb
FROM base as ge

LABEL org.opencontainers.image.title="Great Expectations"
LABEL org.opencontainers.image.description="Great Expectations runtime image"

COPY --from=ge-build /dist/*.whl /tmp/dist/
RUN pip install --no-index --find-links=/tmp/dist/ \
      great_expectations

ENTRYPOINT ["great_expectations"]


# 461 vs the wheel method of 539 mb
FROM base as ge2

LABEL org.opencontainers.image.title="Great Expectations"
LABEL org.opencontainers.image.description="Great Expectations runtime image"

COPY requirements-base.txt requirements-base.txt
RUN GE_VER=$(grep "^great_expectations" requirements-base.txt | cut -d'=' -f3-) \
    && pip install "great_expectations==${GE_VER}"

ENTRYPOINT ["great_expectations"]


# piggyback on ge-build's cache
# 363 mb
FROM ge-build as wemmick-build
COPY . .
RUN pip wheel --wheel-dir=dist -e .


# 637 mb
FROM base as wemmick

LABEL org.opencontainers.image.title="Wemmick"
LABEL org.opencontainers.image.description="BERA's Great Expectations runtime image"

COPY --from=wemmick-build /dist/*.whl /tmp/dist/
RUN pip install --no-index --find-links=/tmp/dist/ wemmick \
      && rm -rf /tmp/dist

# Defaults overridden by Google Cloud Run
ENV HOST="0.0.0.0" \
    PORT=8080

WORKDIR /home/ge/project
ENTRYPOINT ["wemmick"]
# Run server: get PORT and HOST via python and run uvicorn programatically
#ENTRYPOINT ["/app/start_server.py"]


# 540 mb vs 637 mb  when packaged as a wheel and copied over
FROM base as wemmick2

LABEL org.opencontainers.image.title="Wemmick"
LABEL org.opencontainers.image.description="BERA's Great Expectations runtime image"
COPY . .

RUN pip install -e .


# Defaults overridden by Google Cloud Run
ENV HOST="0.0.0.0" \
    PORT=8080

WORKDIR /home/ge/project
ENTRYPOINT ["wemmick"]
# Run server: get PORT and HOST via python and run uvicorn programatically
#ENTRYPOINT ["/app/start_server.py"]



