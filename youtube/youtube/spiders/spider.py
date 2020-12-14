from scrapy import Spider, Request
import urllib.parse as urlparse
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class YoutubeSpider(Spider):
    name = 'youtube'
    allowed_domains = ['www.youtube.com']
    youtube: str = 'https://www.youtube.com/'
    start_urls = []

    def __init__(self, watch_id='', **kwargs):
        self.start_urls = [f"{self.youtube}watch?v={watch_id}"]
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse_url(self, url, param='v'):
        parsed = urlparse.urlparse(url)
        return urlparse.parse_qs(parsed.query)[param]

    def parse(self, r):

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--whitelisted-ips")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option(
            'prefs', {
                'download.default_directory': '/tmp',
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
            })
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
        # driver.set_window_size(0, 0, windowHandle='current')
        # driver.set_window_position(-3000, 0, windowHandle='current')
        driver.get(r.url)
        driver.implicitly_wait(10)
        driver.find_element_by_id('top-level-buttons')
        # wait = WebDriverWait(driver, 30)
        # wait.until(EC.element_to_be_clickable((By.ID, 'top-level-buttons')))

        sr = Selector(text=driver.page_source)
        yt_id = r.xpath("//meta[@itemprop='videoId']/@content").get(self.parse_url(r.url, 'v')[0])
        if yt_id:
            tags = r.xpath("//meta[@property='og:video:tag']/@content").getall()
            tags = ','.join(set(x.lower() for x in tags))
            tags = self.optymize_text(tags)

            duration = r.xpath("//meta[@itemprop='duration']/@content").get('PT0M0S')
            duration_minutes, duration_sec = duration[2:-1].split('M')
            duration = int(duration_minutes) * 60 + int(duration_sec)
            # r.xpath('//yt-formatted-string[@class='style-scope ytd-toggle-button-renderer style-text')
            sentiments = sr.xpath("//yt-formatted-string[@class='style-scope ytd-toggle-button-renderer style-text']")
            likeCount = int(sentiments[0].attrib['aria-label'].replace(' likes', '').replace(',', ''))
            dislikeCount = int(sentiments[1].attrib['aria-label'].replace(' dislikes', '').replace(',', ''))

            yield {
                'title': self.optymize_text(r.xpath('//title/text()').get(None)),
                'tags': tags,
                'is_family_frendly': int('True' == r.xpath("//meta[@itemprop='isFamilyFriendly']/@content").get(0)),
                'yt_id': yt_id,
                'interaction_count': int(r.xpath(f"//meta[@itemprop='interactionCount']/@content").get(0)),
                'date_published': r.xpath("//meta[@itemprop='datePublished']/@content").get(),
                'duration': duration,
                'channel': r.xpath("//meta[@itemprop='channelId']/@content").get(),
                'channel_title': sr.xpath("//ytd-channel-name[@id='channel-name']")[0].xpath('//*[@id="text"]/a/text()')[0].root, # sr.xpath("//div[@class='yt-user-info']/a/text()").get(None),
                'likeCount': likeCount,
                'dislikeCount': dislikeCount,
                'language': r.xpath('//span[contains(@class, "content-region")]/text()').get('')
            }
        else:
            print('None found yt_id', yt_id)
        print('Done!')
        driver.quit()

    def optymize_text(self, text=None):
        if text is None:
            return None
        return ''.join(c for c in text if c.isalnum() or c.isspace() or c == ',' or c == '.').replace('YouTube', '').replace('  ', ' ').strip()

