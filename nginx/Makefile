TAG ?= dev_nginx

# docker

build-image:
ifeq ("$(shell docker images | grep restaurant-nginx | cut -d ' ' -f 1)","")
	docker build --rm --no-cache -t restaurant-nginx:$(TAG) -f Dockerfile .;
endif

build: build-image

clean:
	docker rm nginx
	docker rmi -f restaurant-nginx:$(TAG)

push-image:
	docker push restaurant-kafka:$(TAG)
