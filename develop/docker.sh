#!/usr/bin/env sh

docker-compose -f develop/docker-compose.base.yml \
               -f develop/docker-compose.docker.yml \
               up -d --remove-orphans
