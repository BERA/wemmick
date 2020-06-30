FROM <NAME TBD VANILLA GE>

RUN apt-get update && apt-get install -y make && apt-get install -y git

# Add requirements and pip install before app to speed docker builds via caching
# TODO all this is WIP
ADD ./qa/requirements.txt /app/
RUN pip install -r /app/requirements.txt

ADD ./packages/dataquality/ /app/dataquality/
WORKDIR /app/dataquality
RUN make install-for-docker
WORKDIR /app
ADD ./qa/ /app

CMD ["dataquality"]
