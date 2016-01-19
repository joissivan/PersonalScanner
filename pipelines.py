# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem


class TorrentImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item["image_urls"]:
            if "http" not in image_url:
                image_url = item["base_url"] + image_url
            yield scrapy.Request(image_url, meta={"image_file_path": item["image_file_path"]})


    def item_completed(self, results, item, info):
        super(TorrentImagesPipeline, self).item_completed(results, item, info)


    def file_path(self, request, response=None, info=None):
        image_file_path = request.meta["image_file_path"] + request.url.split("/")[-1]
        return image_file_path

