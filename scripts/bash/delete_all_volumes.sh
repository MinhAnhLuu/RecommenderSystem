#!/bin/bash
# CHAUTRAN


docker volume rm $(docker volume ls | awk '$1=="local" {print $2}')
