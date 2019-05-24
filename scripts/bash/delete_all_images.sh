#!/bin/bash
# CHAUTRAN

###################### RUN THIS SCRIPT CAREFULLY ######################
###################### IT WILL ERASE ALL IMAGES BUILT FROM DOCKERS IN YOUR LOCAL SYSTEM ######################## 

# Delete all images
docker rmi $(docker images -q)
