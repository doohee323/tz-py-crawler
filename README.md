# tz-py-crawler

Youtube crawler with scrapy and selenium(for lazy loading elements).

## -. Prep. 
``` 
    pip3 install scrapy
    pip3 install selenium
    pip3 install --upgrade -r requirements.txt
    
    brew cask install chromedriver
``` 

## -. Run crawl with CLI
```
    to test this url, https://www.youtube.com/watch?v=ioNng23DkIM,

    $> cd youtube
    $> crawl youtube -a watch_id=ioNng23DkIM -o test.csv
```

## -. Run crawl with curl
```
    $> cd tz-py-crawler
    $> python3 youtube/youtube/server.py
    Starting httpd server on localhost:8000
    
    $> curl -d "watch_id=ioNng23DkIM" -X POST http://localhost:8000/crawl
    csv files will be made under youtube folder.
```

## -. docker
```
    $> docker pull doohee323/tz-py-crawler:latest
    $> docker run -d -v `pwd`/youtube:/code/youtube -p 8000:8000 tz-py-crawler
    $> curl -d "watch_id=ioNng23DkIM" -X POST http://localhost:8000/crawl 

```
