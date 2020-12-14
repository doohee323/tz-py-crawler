#!/usr/bin/env bash

cd ..

brew install python
brew info python

#sudo /usr/local/Cellar/python@3.9/3.9.1/bin/easy_install-3.9 virtualenv
#virtualenv venv --python=python3.9
source venv/bin/activate
python --version

pip3 install scrapy
pip3 install selenium
pip3 install requests
#pip3 freeze > scripts/requirements.txt
pip3 install --upgrade -r scripts/requirements.txt

#scrapy startproject youtube
#scrapy genspider -t crawl stack_crawler www.test.co.kr
#scrapy genspider stack_crawler www.test.co.kr

cd youtube
scrapy crawl youtube -a watch_id=ioNng23DkIM -o any_name.csv

brew cask install chromedriver

#pip install pytest

#curl -X GET http://localhost:8000/aaa
curl -d "watch_id=ioNng23DkIM" -X POST http://localhost:8000/crawl

