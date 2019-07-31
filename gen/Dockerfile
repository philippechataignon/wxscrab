FROM alpine

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.3/main" > /etc/apk/repositories
RUN apk --update add musl-dev gcc python python-dev py-twisted scons
COPY gen /gen
RUN cd gen ; scons ; \
    python setup.py bdist ;
ENTRYPOINT /bin/sh
