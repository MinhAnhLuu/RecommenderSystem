#!/bin/sh

# Check if rabbit is up and running before starting the service.

until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 5
done

# Check if postgres is up and running before starting the service.

until pg_isready --host=${DB_HOST} --port=5432 --username=${DB_USER}
do
  echo "Waiting for postgres ............"
  sleep 5;
done

# Run Migrations

# alembic upgrade head

# Run Service

nameko run --config config.yml orders.service --backdoor 3000
