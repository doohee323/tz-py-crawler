#!/usr/bin/env bash

#set -x

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd ${CURDIR}
#docker-compose -f docker-compose.yml up --build -d
docker-compose -f docker-compose.yml up -d
#	docker-compose scale kafka=3
# docker-compose stop
