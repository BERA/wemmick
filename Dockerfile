FROM python:3.7-slim-buster as ge-build
RUN apt-get update
# use same version of ge as wemmick
COPY requirements-base.txt requirements-base.txt
RUN pip wheel --wheel-dir=dist `head -n1 requirements-base.txt`


FROM python:3.7-slim-buster as base
# github actions gives several vcs labels https://github.com/docker/build-push-action#add_git_labels
LABEL org.opencontainers.image.authors="engineering@bera.dev"
LABEL org.opencontainers.image.documentation="https://github.com/bera/wemmick"
LABEL org.opencontainers.image.licenses="https://github.com/bera/wemmick/blob/main/LICENSE"
LABEL org.opencontainers.image.url="https://github.com/bera/wemmick"
LABEL org.opencontainers.image.vcs-url="https://github.com/bera/wemmick"
LABEL org.opencontainers.image.vendor="BERA"

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

ENTRYPOINT ["great_expectations"]

## piggyback on ge-build's cache
FROM ge-build as wemmick-build
COPY . .
RUN pip wheel --wheel-dir=dist -e .

FROM base as wemmick
LABEL org.opencontainers.image.title="Wemmick"
LABEL org.opencontainers.image.description="BERA's Great Expectations runtime image"
COPY --from=wemmick-build /dist/*.whl /tmp/dist/

RUN pip install --no-index --find-links=/tmp/dist/ \
      wemmick \
      && rm -rf /tmp/dist

ENTRYPOINT ["wemmick"]