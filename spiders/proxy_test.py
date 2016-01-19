# command:
# cd /Applications/acquia-drupal/python/cs
# scrapy crawl proxy > Results.log
__author__ = 'sivan'
import scrapy
from scrapy.http import Request
import datetime,time


class ProxySpider(scrapy.Spider):
    name = "proxy"

    allowed_domains = ["ip138.com"]
    start_urls = ["http://www.ip138.com"]


    def parse(self, response):
        iframe_url=response.xpath("//iframe/@src").extract()[0]
        yield(Request(iframe_url, callback = self.parse_iframe))


    def parse_iframe(self, response):
        for ip in response.xpath("//body/center/text()").extract():
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print now + " " + "".join(ip).encode("utf-8")

