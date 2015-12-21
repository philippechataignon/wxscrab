build:
	docker build -t philippechataignon/wxscrab:build .
run:
	docker run --restart=always --name scrab_top    -d -e OPTS='-o -c90 -i10 --mintour 18 --maxtour 20' -p 1991:12345 philippechataignon/wxscrab
	docker run --restart=always --name scrab_normal -d -p 1989:12345 philippechataignon/wxscrab
	docker run --restart=always --name scrab_public -d -p 12345:12345 philippechataignon/wxscrab
log:
	docker logs  scrab_top    
	docker logs  scrab_normal 
	docker logs  scrab_public 
stop:
	docker rm -f  scrab_top    
	docker rm -f  scrab_normal 
	docker rm -f  scrab_public 
