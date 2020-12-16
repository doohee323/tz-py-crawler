#!/usr/bin/env bash

set -x

#bash build.sh latest
#bash build.sh debug2

#bash /vagrant/projects/tz-py-crawler/build.sh debug3

TZ_PROJECT=tz-py-crawler
cd /vagrant/tz-local/resource/${TZ_PROJECT}

VERSION='latest'
if [[ "$1" != "" ]]; then
  VERSION=$1
fi

echo "## [ Make an jenkins env ] #############################"
if [[ -f "/vagrant/tz-local/resource/dockerhub" ]]; then
  export DOCKER_ID=`grep 'docker_id' /vagrant/tz-local/resource/dockerhub | awk '{print $3}'`
  export DOCKER_PASSWD=`grep 'docker_passwd' /vagrant/tz-local/resource/dockerhub | awk '{print $3}'`

  docker build -t ${TZ_PROJECT}:${VERSION} .
  docker login -u="$DOCKER_ID" -p="$DOCKER_PASSWD"
  docker tag ${TZ_PROJECT}:${VERSION} ${DOCKER_ID}/${TZ_PROJECT}:${VERSION}
  docker push ${DOCKER_ID}/${TZ_PROJECT}:${VERSION}
fi

exit 0

docker rmi tz-py-crawler:latest
docker rmi doohee323/tz-py-crawler:latest

docker run -d -v `pwd`/youtube:/code/youtube -p 8000:8000 tz-py-crawler
docker run -v `pwd`/youtube:/code/youtube -p 8000:8000 tz-py-crawler
#docker exec -it kind_benz /bin/bash

#docker image ls
#docker container run -it --rm --name=debug2 -v `pwd`/youtube:/code/youtube -p 8000:8000 cd0dad6e335a /bin/sh
docker run --rm -it --name=debug2 -v `pwd`/youtube:/code/youtube -p 8000:8000 0a3353d03153

#python /code/youtube/youtube/server.py &
#cat /code/youtube/youtube/ioNng23DkIM.csv

curl -d "watch_id=ioNng23DkIM" -X POST http://localhost:8000/crawl
