FROM python:3.7.7-slim

RUN apt-get update

ADD ./requirements.txt /app/
RUN pip install -r /app/requirements.txt
WORKDIR /app

LABEL maintainer="BERA"

# Run great_expectations by default and allow any command to be run if desired.
CMD ["great_expectations"]
