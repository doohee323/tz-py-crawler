#!/usr/bin/env bash

#set -x

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${CURDIR}

if [ $1 == 'up' ]; then
  #docker-compose -f docker-compose.yml up --build -d
  docker-compose -f docker-compose.yml up -d
elif [ $1 == 'down' ]; then
  docker-compose stop
else
  echo "bash run.sh up / down"
fi

#	docker-compose scale kafka=3


