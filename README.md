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
    $> cd projects/tz-py-crawler
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

## -. k8s in Jenkins
``` 
    # Jenkins global settings
        http://dooheehong323:31000/configure
        Global properties > Environment variables > Add
        ORGANIZATION_NAME: doohee323
        YOUR_DOCKERHUB_USERNAME: doohee323

    # make a project in Jenkins
        new item
        name: tz-k8s-vagrant
        type: multibranch Pipeline
        Display Name: tz-k8s-vagrant
        Branch Sources: GitHub
            Credential: Jenkins
                Username: doohee323 # github id
                Password: xxxx
                    https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token
                ID: GitHub
            Owener: doohee323
    
        Repository HTTPS URL: git clone https://github.com/doohee323/tz-k8s-vagrant.git

    # Run the project

    ## checking the result 
        k get all | grep tz-k8s-vagrant
```