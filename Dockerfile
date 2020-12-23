#FROM ubuntu:18.04
FROM python:3.8

RUN apt-get update && apt-get install -y curl build-essential
#RUN apt-get update && apt-get install -y python3.8 python3.8-dev python3.8-distutils
#RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
#RUN update-alternatives --set python /usr/bin/python3.8
#RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
#    python get-pip.py --force-reinstall && \
#    rm get-pip.py
#RUN apt-get install -y unzip xvfb libxi6 libgconf-2-4

RUN apt-get install -y rsync

# Install Chrome for Selenium
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf
RUN rm /chrome.deb

# Install chromedriver for Selenium
RUN curl https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip -o chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY youtube/ .

EXPOSE 8000
## local debugging
#CMD [ "python", "/code/youtube/youtube/server.py" ]
# run in k8s
CMD [ "python", "/code/youtube/server.py" ]
#CMD python -m http.server 8000
