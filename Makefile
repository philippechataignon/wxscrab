build:
	docker build -t philippechataignon/wxscrab_gen:build .
tag:
	docker tag -f philippechataignon/wxscrab_gen:build philippechataignon/wxscrab_gen
