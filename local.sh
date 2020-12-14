#!/usr/bin/env bash

brew install python
brew info python

#sudo /usr/local/Cellar/python@3.9/3.9.1/bin/easy_install-3.9 virtualenv
#virtualenv venv --python=python3.9
source venv/bin/activate
python --version

pip3 install scrapy
pip3 install selenium
pip3 install requests
#pip3 freeze > requirements.txt
pip3 install --upgrade -r requirements.txt

#scrapy startproject youtube
#scrapy genspider -t crawl stack_crawler www.test.co.kr
#scrapy genspider stack_crawler www.test.co.kr

cd youtube
scrapy crawl youtube -a watch_id=ioNng23DkIM -o any_name.csv

brew cask install chromedriver

#pip install pytest

exit 0

#curl -X GET http://localhost:8000/aaa
curl -d "watch_id=ioNng23DkIM" -X POST http://localhost:8000/crawl

# make docker image
docker build -t tz-py-crawler .

docker run -d -v `pwd`/shared:/code -p 8000:8000 tz-py-crawler
docker run -v `pwd`/shared:/code -p 8000:8000 tz-py-crawler

#docker image ls
#docker container run -it --rm --name=debug2 -v `pwd`/shared:/shared 40ae7dc78fff /bin/sh

#python /code/youtube/server.py &
#cat /code/youtube/ioNng23DkIM.csv


