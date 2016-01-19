# -*- coding: utf-8 -*-
# command:
# cd /Applications/acquia-drupal/python/cs
# scrapy crawl youkucapture > Results.log
__author__ = 'sivan'
import scrapy
from scrapy.http import Request
from django.utils.encoding import smart_str, smart_unicode
import re
#from scrapy import Selector

class YoukuCaptureSpider(scrapy.Spider):
    name = "youkucapture"

    base_url = "www.youku.com"
    start_url = "http://" + base_url + "/playlist_show/id_23304992_ascending_1_page_1.html"

    allowed_domains = [base_url]
    start_urls = [start_url]


    def parse(self, response):

        # Capture Something
        tag_a = response.xpath("//li[@class='v_title']/a")
        for src in tag_a:
            title = ''.join(src.xpath('@title').extract()).encode("utf-8")
            link = ''.join(src.xpath('@href').extract()).encode("utf-8")
            print "[" + title + "] " + link


        # run all next page links
        for href in response.xpath("//div[@class='page f_r']/a/@href").extract():
            yield Request(smart_str(href), callback=self.parse)

