__author__ = 'sivan'
# -*- coding: utf-8 -*-
# command: scrapy crawl torrent -a keyword=lost -a perfect=1
__author__ = 'sivan'
import scrapy
from scrapy.http import Request, FormRequest
from scrapy import signals
from scrapy.mail import MailSender
from django.utils.encoding import smart_str, smart_unicode
import urllib, os
from cs.items import WebsiteItem
from cs.items import ImageItem


class TorrentSpider(scrapy.Spider):
    name = "torrent"
    keyword = ""
    perfect = "0"
    websites = set()
    default_dir = download_dir = "/Applications/acquia-drupal/python/cs/torrent/" # default download dir
    email_content = ""


    def __init__(self, keyword = None, perfect = None):
        self.keyword = keyword
        self.perfect = perfect
        self.download_dir += keyword + "/"
        if not os.path.exists(self.download_dir):
            os.mkdir(self.download_dir)

        # add websites here
        ibtzz = WebsiteItem()
        ibtzz["name"] = "ibtzz"
        ibtzz["base_url"] = "http://www.ibtzz.com"
        ibtzz["start_url"] = "http://www.ibtzz.com/?s=" + keyword
        ibtzz["method"] = "Get"
        ibtzz["link_xpath"] = "//div[contains(@class, 'post-grid')]/div/a/@href|//a[@class='nextpostslink']/@href"
        ibtzz["image_xpath"] = "//div[contains(@class, 'entry-content')]/p/img[not(contains(@src,'https'))]/@src"
        ibtzz["torrent_type"] = "redirect"
        ibtzz["torrent_title"] = "//h1/a/text()"
        ibtzz["torrent_xpath"] = "//a[contains(@href, 'dl_id')]/@href"
        self.websites.add(ibtzz)

        dtoo = WebsiteItem()
        dtoo["name"] = "dtoo"
        dtoo["base_url"] = "http://www.3dtoo.com"
        dtoo["start_url"] = "http://www.3dtoo.com/tags.php?/1080p/"
        dtoo["method"] = "Get"
        dtoo["link_xpath"] = "//div[@class='listbox']/ul/li/a[@class='title' and contains(text(), " + keyword.decode("utf-8") + ")]/@href"+\
                               "|//ul[@class='pagelist']/li/a[not(contains(@href, '-'))]/@href"
        dtoo["image_xpath"] = "//div[@id='mbtxfont']/table/tr/td/div/img[not(contains(@src,'https'))]/@src"
        dtoo["torrent_type"] = "download"
        dtoo["torrent_title"] = "//h1/text()"
        dtoo["torrent_xpath"] = "//a[contains(@href, 'uploads')]/@href"
        self.websites.add(dtoo)

        poxiao = WebsiteItem()
        poxiao["name"] = "poxiao"
        poxiao["base_url"]  = "http://www.poxiao.com"
        poxiao["start_url"] = "http://www.poxiao.com/e/search/index22.php"
        poxiao["method"] = "Post"
        poxiao["form_data"] = {'show': 'title,smalltext', 'tempid': '1', 'keyboard': keyword.decode("utf-8").encode("gb2312")}
        poxiao["link_xpath"] = "//div[@class='content']/ul/li/h3/a/@href|//div[@class='list-pager']/a/@href"
        poxiao["image_xpath"] = "//div[@class='detail_pic']/span/img[not(contains(@src,'https'))]/@src"
        poxiao["torrent_type"] = "ftp"
        poxiao["torrent_title"] = "//h1/em/text()"
        poxiao["torrent_xpath"] = "//div[@class='resourcesmain']/table/tr/td/input[@type='checkbox']/@value"
        self.websites.add(poxiao)

        dy2018 = WebsiteItem()
        dy2018["name"] = "dy2018"
        dy2018["base_url"]  = "http://www.dy2018.com"
        dy2018["start_url"] = "http://www.dy2018.com/e/search/index.php"
        dy2018["method"] = "Post"
        dy2018["form_data"] = {'show': 'title,smalltext', 'tempid': '1', 'keyboard': keyword.decode("utf-8").encode("gb2312")}
        dy2018["link_xpath"] = "//a[@class='ulink']/@href|//div[@class='x']/a/@href"
        dy2018["image_xpath"] = "//div[@id='Zoom']/p/img[not(contains(@src,'https'))]/@src"
        dy2018["torrent_type"] = "ftp"
        dy2018["torrent_title"] = "//h1/text()"
        dy2018["torrent_xpath"] = "//a[contains(@href, 'ftp')]/@href"
        self.websites.add(dy2018)


    def start_requests(self):
        # define start url
        for website in self.websites:
            if website["method"] == "Post":
                yield FormRequest(website["start_url"], formdata=website["form_data"], meta={'website': website}, callback=self.parse)
            else:
                yield Request(website["start_url"], meta={'website': website}, callback=self.parse)


    def close(spider, reason):
        # send email when spider closed
        if spider.email_content.strip():
            mailer = MailSender(mailfrom="joissivan@gmail.com", smtphost="smtp.gmail.com", smtpport=587, smtpuser="joissivan@gmail.com",smtppass="6380sivan6756")
            mailer.send(to=["joissivan@139.com", "13564608090@139.com"], cc=["jois4mac@gmail.com"], subject= "[Movies Here] " + spider.keyword + " is coming!!!", body=spider.email_content)

        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)


    def parse(self, response):
        #TESTING FOR LINK
        #for link in response.xpath(response.meta['website']["link_xpath"]).extract():
        #    print "<" + response.url + "> " + link
        #return

        #TESTING FOR TORRENT
        #for href in response.xpath(response.meta['website']["torrent_xpath"]).extract():
        #    print ''.join(href).encode("utf-8")

        website = response.meta['website']
        torrent_xpath = response.xpath(website["torrent_xpath"]).extract()
        if torrent_xpath:
            # perfect matched
            torrent_title = ''.join(response.xpath(website["torrent_title"]).extract()).encode("utf-8").replace('/', '')
            if self.perfect == "1" and self.keyword not in torrent_title:
                return

            # if find torrent(s), create website folder </Applications/acquia-drupal/python/cs/torrent/{keyword}/{website_name}>
            website_dir = self.download_dir + website["name"] + "/"
            if not os.path.exists(website_dir):
                os.mkdir(website_dir)

            # if there's no folder </Applications/acquia-drupal/python/cs/torrent/{keyword}/{website_name}/{torrent_name}>, create it & save torrents
            torrent_dir = website_dir + torrent_title + "/"
            if not os.path.exists(torrent_dir):
                os.mkdir(torrent_dir)
                for href in torrent_xpath:

                    # complete link
                    if not "http" in href:
                        href = website["base_url"] + href
                    if website["torrent_type"] == "redirect":
                        # save torrent
                        urllib.urlretrieve(smart_str(href), torrent_dir + torrent_title + ".torrent")
                    elif website["torrent_type"] == "download":
                        # save torrent
                        urllib.urlretrieve(smart_str(href), torrent_dir + torrent_title + "." + smart_str(href).split(".")[-1])
                    elif (website["torrent_type"] == "ftp" and "ftp://" in href):
                        # write ftp address(es) into file
                        txt = open(torrent_dir + torrent_title + ".txt", "a")
                        str = ''.join(href).encode("utf-8").split("ftp://")
                        txt.write("ftp://" + str[1] + '\n')
                        txt.close()

                    # write email content
                    self.email_content += "[" + website["name"] + "]" + torrent_title + "\n"

                    # save pictures
                    image = ImageItem()
                    image["base_url"] = website["base_url"]
                    image["image_urls"] = response.xpath(website["image_xpath"]).extract()
                    image["image_file_path"] = torrent_dir.replace(self.default_dir, "")
                    yield image

        # Go to search results' link
        for link in response.xpath(website["link_xpath"]).extract():
            if not "http" in link:
                link = website["base_url"] + link
            yield Request(smart_str(link), meta={'website': website}, callback=self.parse)

