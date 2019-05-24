HTMLCOV_DIR ?= htmlcov
SHELL := /bin/bash -e

CUSTOMIZED_IMAGES := gateway recommender orders products nginx web
CUSTOMIZED_CONTAINER := gateway recommender orders products nginx web
ORIGINAL_IMAGES := rabbitmq:3.6-alpine postgres:10.5-alpine redis:4.0.11-alpine solr:7.4.0
ORIGINAL_CONTAINER := restaurant-rabbitmq restaurant-postgres restaurant-redis
CACHE_VOLUME := images-cache

# test

coverage-html:
	coverage html -d $(HTMLCOV_DIR) --fail-under 100

coverage-report:
	coverage report -m

test:
	flake8 --ignore E501,E126 orders products gateway authentication
	coverage run -m pytest gateway/test $(ARGS)
	coverage run --append -m pytest orders/test $(ARGS)
	coverage run --append -m pytest products/test $(ARGS)
#    coverage run --append -m pytest authentication/test $(ARGS)

coverage: test coverage-report coverage-html


############################################
########## DOCKER BUILD IMAGES #############
############################################

build-storage-base:
	# If the image already exists, not rebuild it
ifeq ("$(shell docker images | grep restaurant-base | cut -d ' ' -f 1)","")
	docker build --build-arg UID="$$(id -u)" --build-arg GID="$$(id -g)" --rm -t restaurant-base -f docker/docker.base .;
endif

build-wheel-builder: build-storage-base
	# If the image already exists, not rebuild it
ifeq ("$(shell docker images | grep restaurant-builder | cut -d ' ' -f 1)","")
	docker build --rm -t restaurant-builder -f docker/docker.build .;
endif

#run-wheel-builder: build-wheel-builder
#	for image in $(IMAGES) ; do make -C $$image run-wheel-builder; done

build-images: build-wheel-builder
	for image in $(CUSTOMIZED_IMAGES) ; do make -C $$image build; done

build: build-images

####################################################
########## DOCKER CLEAN CONTAINERS/IMAGES ##########
####################################################

# clean customized image
customized_image_clean:
	for image in $(CUSTOMIZED_IMAGES) ; do \
		docker rmi storage-$$image:dev_$$image; \
	done

# clean original image
original_image_clean:
	for image in $(ORIGINAL_IMAGES) ; do \
		docker rmi $$image; \
	done


# clean original container
original_container_clean:
	for container in $(ORIGINAL_CONTAINER) ; do \
		docker rm $$container; \
	done

# clean customized container
customized_container_clean:
	for container in $(CUSTOMIZED_CONTAINER) ; do \
		docker rm $$container ; \
	done

# clean all images
clean_images: customized_image_clean original_image_clean

# clean all containers
clean_containers: customized_container_clean original_container_clean

# clean all
clean: clean_containers clean_images


####################################################
########## DOCKER LOGIN PULL/PUSH ##################
####################################################

# Login docker hub
docker-login:
	docker login --email=$(DOCKER_EMAIL) --password=$(DOCKER_PASSWORD) --username=$(DOCKER_USERNAME)

# Push image to login
push-images: build
	for image in $(IMAGES) ; do make -C $$image push-image; done
