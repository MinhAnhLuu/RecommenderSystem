TAG ?= dev_chau

# docker

mkdir_wheelhouse:
ifeq ("$(shell docker images | grep restaurant-recommender | cut -d ' ' -f 1)","")
	mkdir -p wheelhouse ;
endif

run-wheel-builder: mkdir_wheelhouse
ifeq ("$(shell docker images | grep restaurant-recommender | cut -d ' ' -f 1)","")
	docker run --rm \
		-v "$$(pwd)":/home/docker/recommender \
		-v "$$(pwd)"/wheelhouse:/home/docker/wheelhouse \
		-w /home/docker/recommender \
		restaurant-builder;
endif

build-image: run-wheel-builder
ifeq ("$(shell docker images | grep restaurant-recommender | cut -d ' ' -f 1)","")
	docker build --rm --no-cache -t restaurant-recommender:$(TAG) -f docker.run .;
endif

build: build-image

push-image:
	docker push restaurant-recommender:$(TAG)
