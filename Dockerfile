FROM alpine

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.3/main" > /etc/apk/repositories
RUN apk --update add musl-dev gcc python python-dev py-twisted scons
RUN adduser -u 50000 -D -H scrabble
COPY . /scrabble
RUN rm -r /scrabble/client /scrabble/win
WORKDIR /scrabble
RUN ./install
RUN chown -R scrabble: /scrabble
USER scrabble
EXPOSE 12345

ENTRYPOINT /scrabble/go_server
