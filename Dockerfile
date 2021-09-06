FROM python:3.9.7-slim-buster as ge

ARG REVISION
ARG CREATED
ARG GE_VER

LABEL org.opencontainers.image.authors="engineering@bera.dev"
LABEL org.opencontainers.image.created=${CREATED}
LABEL org.opencontainers.image.description="Great Expectations runtime image"
LABEL org.opencontainers.image.documentation="https://github.com/bera/wemmick"
LABEL org.opencontainers.image.licenses="https://github.com/bera/wemmick/blob/main/LICENSE"
LABEL org.opencontainers.image.revision=${REVISION}
LABEL org.opencontainers.image.source="https://github.com/bera/wemmick"
LABEL org.opencontainers.image.title="Great Expectations"
LABEL org.opencontainers.image.url="https://github.com/bera/wemmick"
LABEL org.opencontainers.image.vendor="BERA"
LABEL org.opencontainers.image.version=${GE_VER}

RUN groupadd -r ge && useradd -r -m -g ge ge

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY requirements-base.txt requirements-base.txt
# use same version of ge as wemmick, not neccesarily the latest version
# unlike `head -n1 requirements-base.txt` this grep does not require
# first line placement and will fail if great_expectations is ommitted.
RUN GE_VER=$(grep "^great_expectations" requirements-base.txt | cut -d'=' -f3-) \
    && pip install "great_expectations==${GE_VER}"

# short path for vol mounts
WORKDIR /ge
ENTRYPOINT ["great_expectations"]
CMD ["--help"]


FROM ge as wemmick

ARG HOST
ARG PORT
ENV HOST ${HOST:-"0.0.0.0"}
ENV PORT ${PORT:-"8080"}

LABEL org.opencontainers.image.title="Wemmick"

# It's critical to have wemmick installed somewhere outside the great_expectations mount
WORKDIR /app
COPY requirements-http.txt requirements-http.txt
RUN pip install -r requirements-http.txt
COPY requirements-base.txt requirements-base.txt
RUN pip install -r requirements-base.txt
COPY . .
RUN pip install -e .

# Keep the ge mount as the workdir so the cli functions
WORKDIR /ge
ENTRYPOINT ["wemmick"]

# server mode
# docker run -p 8080:8080 -v "$(pwd):/ge" --entrypoint /app/src/wemmick/start_server.py beradev/wemmick:latest