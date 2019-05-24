TAG ?= dev_chau

# docker

build-image:
ifeq ("$(shell docker images | grep restaurant-web | cut -d ' ' -f 1)","")
	docker build --rm --no-cache -t restaurant-web:$(TAG) -f dockerfile .;
endif

build: build-image

push-image:
	docker push restaurant-web:$(TAG)
