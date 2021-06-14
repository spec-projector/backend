#!/usr/bin/env sh

docker-compose -p sp \
               -f develop/docker-compose.base.yml \
               -f develop/docker-compose.docker.yml \
               up -d --remove-orphans
