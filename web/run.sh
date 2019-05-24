#!/bin/sh

# Run Service
# nameko run --config config.yml web.service --backdoor 3000

echo "Start successfully";

cd web/;

npm run start;
