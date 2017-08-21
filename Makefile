build:
	docker build -t philippechataignon/wxscrab:build .
tag:
	docker tag -f philippechataignon/wxscrab:build philippechataignon/wxscrab
run:
	docker run --restart=always --name scrab_top    -d -e OPTS='-o -c90 -i10 --mintour 18 --maxtour 20' -p 1991:12345 philippechataignon/wxscrab
	docker run --restart=always --name scrab_normal -d -p 1989:12345 philippechataignon/wxscrab
	docker run --restart=always --name scrab_public -d -p 12345:12345 philippechataignon/wxscrab
log:
	echo Top
	docker logs  scrab_top    
	echo Normal
	docker logs  scrab_normal 
	echo Public
	docker logs  scrab_public 
stop:
	docker rm -f  scrab_top    
	docker rm -f  scrab_normal 
	docker rm -f  scrab_public 
