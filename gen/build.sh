#!/bin/sh
docker build -t philippechataignon/wxscrab_gen:build .
docker create --name wxscrab_gen philippechataignon/wxscrab_gen:build
docker cp wxscrab_gen:gen/gen_part .
docker cp wxscrab_gen:gen/dist .
