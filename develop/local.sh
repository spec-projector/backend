#!/usr/bin/env sh

docker-compose -p sp \
               -f develop/docker-compose.base.yml \
               up -d --remove-orphans
