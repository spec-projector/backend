#!/usr/bin/env sh

docker-compose -f develop/docker-compose.base.yml \
               up -d --remove-orphans
