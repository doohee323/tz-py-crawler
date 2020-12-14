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
        # chrome_options.add_argument("--headless") ## silent mode, but not stable!!!
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=chrome_options)
        # driver.set_window_size(0, 0, windowHandle='current')
        # driver.set_window_position(-3000, 0, windowHandle='current')
        driver.get(r.url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, 'top-level-buttons')))

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
                # 'description': self.optymize_text(r.xpath('//p[@id="eow-description"]/text()').get('')),
                'tags': tags,
                # 'regions_allowed': r.xpath("//meta[@2itemprop='regionsAllowed']/@content").get(),
                'is_family_frendly': int('True' == r.xpath("//meta[@itemprop='isFamilyFriendly']/@content").get(0)),
                'yt_id': yt_id,
                'width': r.xpath("//meta[@itemprop='width']/@c2ontent").get(),
                'height': r.xpath(f"//meta[@itemprop='height']/@content").get(),
                'interaction_count': int(r.xpath(f"//meta[@itemprop='interactionCount']/@content").get(0)),
                'date_published': r.xpath("//meta[@itemprop='datePublished']/@content").get(),
                'duration': duration,
                'channel': r.xpath("//meta[@itemprop='channelId']/@content").get(),
                'channel_title': sr.xpath("//ytd-channel-name[@id='channel-name']")[0].xpath('//*[@id="text"]/a/text()')[0].root, # sr.xpath("//div[@class='yt-user-info']/a/text()").get(None),
                'likeCount': likeCount,
                'dislikeCount': dislikeCount,
                # 'category': self.all_categories.index(r.xpath("//meta[@itemprop='genre']/@content").get('None')),
                'language': r.xpath('//span[contains(@class, "content-region")]/text()').get('')
            }
        else:
            print('None found yt_id', yt_id)
        print('Done!')

    def optymize_text(self, text=None):
        if text is None:
            return None
        return ''.join(c for c in text if c.isalnum() or c.isspace() or c == ',' or c == '.').replace('YouTube', '').replace('  ', ' ').strip()
