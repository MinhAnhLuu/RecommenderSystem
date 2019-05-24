#!/bin/bash
# CHAUTRAN

if [ "$1" == "-h" ] ; then
    echo "Usage: script container_id image_id "
    exit 0
fi

container_id=$1
image_id=$2

###################### RUN THIS SCRIPT CAREFULLY ######################

# Delete one container
docker rm $container_id
# Delete one image
docker rmi $image_id
