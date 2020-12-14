# tz-py-crawler

Youtube crawler with scrapy and selenium(for lazy loading elements).

## -. Prep. 
``` 
    pip3 install scrapy
    pip3 install selenium
    pip3 install --upgrade -r scripts/requirements.txt
    
    brew cask install chromedriver
``` 

## -. Run crawl
```
    to test this url, https://www.youtube.com/watch?v=ioNng23DkIM,

    cd youtube
    crawl youtube -a watch_id=ioNng23DkIM -o test.csv
```
