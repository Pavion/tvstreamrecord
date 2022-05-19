FROM alpine

MAINTAINER Pavion <tvstreamrecord@gmail.com>
# Thanks docqube/tvstreamrecord for his contribution

COPY . /tsr
RUN echo "/volume1/common/tvstreamrecord.db" > /tsr/db.ini

RUN apk update
RUN apk add --upgrade python3 py-pip ca-certificates ffmpeg tzdata
RUN pip install "cherrypy>=3.8.0,<9.0.0"
RUN pip install bottle

ENV TZ=Europe/Brussels

EXPOSE 8030/tcp

RUN mkdir -p /volume1/common
VOLUME ["/volume1/common"]

WORKDIR /tsr
ENTRYPOINT ["/usr/bin/python3" , "tvstreamrecord.py"]
