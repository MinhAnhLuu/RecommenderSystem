#!/bin/sh

# Check if postgres is up and running before starting the service.

until pg_isready --host=${DB_HOST} --port=5432 --username=${DB_USER}
do
  echo "Waiting for postgres ............"
  sleep 5;
done


# Run the service

#nameko run --config config.yml authentication.authentication.service
echo "Migrating db..."
python manage.py migrate

echo "Calling uwsgi..."
uwsgi --ini ./uwsgi/webserver.ini &

echo "Initializing django server..."
python manage.py  runserver 0.0.0.0:8080
