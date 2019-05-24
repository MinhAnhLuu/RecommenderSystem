#!/bin/bash
# CHAUTRAN

###################### RUN THIS SCRIPT CAREFULLY ######################
###################### IT WILL ERASE ALL CONTAINERS BUILT FROM DOCKERS IN YOUR LOCAL SYSTEM ######################## 

# Delete all containers
docker rm $(docker ps -a -q)
