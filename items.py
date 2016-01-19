# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WebsiteItem(scrapy.Item):
    # define the fields for your item here like:

    name = scrapy.Field() #Site name

    base_url = scrapy.Field() #Home page
    start_url = scrapy.Field() #Langding page

    method = scrapy.Field() #Post or Get
    form_data = scrapy.Field() #Post data

    link_xpath = scrapy.Field() #Crawling Page
    image_xpath = scrapy.Field()

    torrent_type = scrapy.Field() #FTP or Torrent
    torrent_title = scrapy.Field()
    torrent_xpath = scrapy.Field()


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    username = scrapy.Field()
    password = scrapy.Field()



class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    base_url = scrapy.Field()
    image_urls = scrapy.Field()
    image_file_path = scrapy.Field()
    images = scrapy.Field()