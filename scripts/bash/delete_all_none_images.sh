#!/bin/bash
# CHAUTRAN


docker rmi $(docker images|grep "<none>"|awk '$1=="<none>" {print $3}')
