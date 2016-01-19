# command:
# cd /Applications/acquia-drupal/python/cs
# scrapy crawl cs > Results.log
__author__ = 'sivan'
import scrapy
from scrapy.http import Request
from django.utils.encoding import smart_str, smart_unicode
import re

class CsSpider(scrapy.Spider):
    name = "cs"

    base_url = "dev.consumersearch.com"
    #base_url = "test.python.com"
    start_url = "http://" + base_url ##maybe changed by "https"

    http_user = 'imgchina'
    http_pass = 'F9jtP3ipxY'

    allowed_domains = [base_url]
    start_urls = [start_url]
    source = set()


    def parse(self, response):

        # get external sources (CSS & JS)
        added = False
        for src in response.xpath("//*[not(name()='img')]/@src|//link/@href").extract():
            if self.base_url not in src and "http://" in src and src not in self.source: #start with http://, but not inner links
                self.source.add(src)
                print src
                added = True
        if added:
            print "FROM Response URL: " + response.url + "\n-----------------------------------------------"


        # run all ConsumerSearch.com links
        for href in response.xpath("//a/@href").extract():
            if "http" in href and self.base_url not in href: #outer links
                continue
            links = re.split(r'[#?]+', href)
            link = links[0]
            if link != "" and "sitemap" not in link: #not sitemap links
                if "http" in link:
                    absolute_path = link
                else:
                    if self.base_url in link:
                        absolute_path = "http:" + link ##maybe changed by "https
                    else:
                        if link[0] == "/":
                            absolute_path = self.start_url + link
                        else:
                            absolute_path = self.start_url + "/" + link
                #print smart_str(absolute_path)
                yield Request(smart_str(absolute_path), callback=self.parse)

