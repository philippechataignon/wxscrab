FROM alpine

RUN apk --update add python py-twisted py-pip
RUN adduser -u 50000 -D -H scrabble
COPY gen_part dico-1.02.linux-x86_64.tar.gz ./
RUN tar xf dico-1.02.linux-x86_64.tar.gz
VOLUME /scrabble
#RUN rm -r client/ win/ ; \
#    cd gen ; scons ; \
#    python setup.py install ; \
#    chown -R scrabble: /scrabble
#USER scrabble
EXPOSE 12345
WORKDIR /scrabble/server
CMD ./go_server
