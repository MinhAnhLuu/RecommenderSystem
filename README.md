# Restaurant Microservices
## Food application handler
Order products in restaurants

## Prerequisites

* [Python 3](https://www.python.org/downloads/)
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

## Overview

### Repository structure

### Services

#### Products Service

#### Orders Service

Responsible for storing and managing orders information and exposing RPC Api that can be consumed by other services.

This service is using PostgreSQL database to persist order information.
- [nameko-sqlalchemy](https://pypi.python.org/pypi/nameko-sqlalchemy)  dependency is used to expose [SQLAlchemy](http://www.sqlalchemy.org/) session to the service class.
- [Alembic](https://pypi.python.org/pypi/alembic) is used for database migrations.

#### Gateway Service

Is a service exposing HTTP Api to be used by external clients e.g., Web and Mobile Apps. It coordinates all incoming requests and composes responses based on data from underlying domain services.

[Marshmallow](https://pypi.python.org/pypi/marshmallow) is used for validating, serializing and deserializing complex Python objects to JSON and vice versa in all services.

## Running examples

Quickest way to try out examples is to run them with Docker Compose

`$ docker-compose up`

Docker images for [RabbitMQ](https://hub.docker.com/_/rabbitmq/), [PostgreSQL](https://hub.docker.com/_/postgres/) and [Redis](https://hub.docker.com/_/redis/) will be automatically downloaded and their containers linked to example service containers.

When you see `Connected to amqp:...` it means services are up and running.

Gateway service with HTTP Api is listening on port 8003 and these endpoitns are available to play with:

#### Create Product

#### Get Product

```sh
```
#### Create Order

```sh
```

#### Get Order

```sh
```

## Running tests

Ensure RabbitMQ, PostgreSQL and Redis are running and `config.yaml` files for each service are configured correctly.

`$ make coverage`
