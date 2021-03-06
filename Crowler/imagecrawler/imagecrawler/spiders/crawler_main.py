import scrapy
import re
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector


class Scraper(scrapy.Spider):
    name = "reddit"

    # Define the regex we'll need to filter the returned links
    url_matcher = re.compile('^https:\/\/www\.pexels\.com\/photo\/')

    # Create a set that'll keep track of ids we've crawled
    crawled_ids = set()

    src_extractor = re.compile('src="([^"]*)"')
    tags_extractor = re.compile('alt="([^"]*)"')

    def start_requests(self):
        url = "https://www.reddit.com/r/PewdiepieSubmissions/"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        #print response
        body = Selector(text=response.body)
        #print body
        images = body.xpath('//*[@id="t3_9psz3h"]/div[2]/div[3]/div/div[2]').extract()[0] #//*[@id="t3_9psz3h"]/div[2]/div[3]/div/div[2]
        #print images


        # body.css().extract() returns a list which might be empty
        #for image in images:
        img_url = Scraper.src_extractor.findall(images)[0]
        img_url = img_url.split('amp;')
        img_url = ''.join(img_url)
        print img_url

        """
        link_extractor = LinkExtractor(allow=Scraper.url_matcher)
        next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)]

        # Crawl the filtered links
        for link in next_links:
            yield scrapy.Request(link, self.parse)

    def is_extracted(self, url):
        # Image urls are of type: https://www.pexels.com/photo/asphalt-blur-clouds-dawn-392010/
        id = int(url.split('/')[-2].split('-')[-1])
        if id not in Scraper.crawled_ids:
            Scraper.crawled_ids.add(id)
            return False
        return True
"""
