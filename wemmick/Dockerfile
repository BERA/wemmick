FROM vanilla-ge:latest

RUN apt-get update && apt-get install -y make
ADD ./dataquality/ /app/dataquality/
WORKDIR /app/dataquality
RUN make install-for-docker
WORKDIR /app
LABEL maintainer="BERA"
ENTRYPOINT ["dataquality"]
