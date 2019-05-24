#!/bin/sh

# Check if elasticsearch is up and running before starting the service.

until curl -f http://${ELASTICSEARCH_HOST}:9200
do
  echo "Waiting for Elasticsearch ............"
  sleep 5;
done

# Run Service
nameko run --config config.yml recommender.service --backdoor 3000
