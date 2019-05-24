TAG ?= dev_chau

# docker

mkdir_wheelhouse:
ifeq ("$(shell docker images | grep restaurant-orders | cut -d ' ' -f 1)","")
	mkdir -p wheelhouse ;
endif

run-wheel-builder: mkdir_wheelhouse
ifeq ("$(shell docker images | grep restaurant-orders | cut -d ' ' -f 1)","")
	docker run --rm \
		-v "$$(pwd)":/home/docker/orders \
		-v "$$(pwd)"/wheelhouse:/home/docker/wheelhouse \
		-w /home/docker/orders \
		restaurant-builder;
endif

build-image: run-wheel-builder
ifeq ("$(shell docker images | grep restaurant-orders | cut -d ' ' -f 1)","")
	docker build --rm --no-cache -t restaurant-orders:$(TAG) -f docker.run .;
endif

build: build-image

push-image:
	docker push restaurant-orders:$(TAG)
