FROM beradev/ge:latest

RUN apt-get update
COPY ./dataquality/ /app/dataquality/
WORKDIR /app/dataquality
RUN pip install -r requirements.txt
RUN pip install -e .
WORKDIR /home
LABEL maintainer="BERA"
ENTRYPOINT ["dataquality"]
