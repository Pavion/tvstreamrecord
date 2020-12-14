FROM alpine

MAINTAINER Pavion <tvstreamrecord@gmail.com>
# Thanks docqube/tvstreamrecord for his contribution

COPY . /tsr

RUN apk update
RUN apk add --upgrade python3 py-pip ca-certificates ffmpeg tzdata
RUN pip install "cherrypy>=3.8.0,<9.0.0"
RUN pip install bottle

ENV TIMEZONE=Europe/Brussels
RUN cp /usr/share/zoneinfo/${TIMEZONE} /etc/localtime && echo ${TIMEZONE} > /etc/timezone && apk del tzdata

EXPOSE 8030/tcp

RUN mkdir -p /volume1/common
VOLUME [/volume1/common]

WORKDIR /tsr
ENTRYPOINT ["/usr/bin/python3" , "tvstreamrecord.py"]
