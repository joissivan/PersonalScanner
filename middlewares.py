__author__ = 'sivan'
from scrapy import signals
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy import log
import os, time, random
from scrapy.conf import settings


class SaveErrorsMiddleware(object):
    def __init__(self, crawler):
        crawler.signals.connect(self.close_spider, signals.spider_closed)
        crawler.signals.connect(self.open_spider, signals.spider_opened)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def open_spider(self, spider):
        self.output_file = open('HttpError.log', 'w')

    def close_spider(self, spider):
        self.output_file.close()

    def process_spider_exception(self, response, exception, spider):
        self.output_file.write('[' + str(response.status) + ']' + response.url +  '\n')


class SaveRetryFailedMiddleware(RetryMiddleware):

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        if retries <= self.max_retry_times:
            log.msg(format="Retrying %(request)s (failed %(retries)d times): %(reason)s",
                    level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            # do something with the request: inspect request.meta, look at request.url...
            log.msg(format="Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                    level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)
            self.output_file = open('RetryFailed.log', 'a')
            self.output_file.write("[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "] " + request.url + '\n')
            self.output_file.close()


class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):

        user_agent  = random.choice(settings.get('USER_AGENT_LIST'))
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)


class ProxyMiddleware(object):

    def process_request(self, request, spider):

        file = open(settings.get('HTTP_PROXY'))
        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            #for http_proxy in lines:
            #    request.meta['proxy'] = "http://" + http_proxy.strip("\n") #"".join(http_proxy.split("\n"))

            http_proxy  = random.choice(lines)
            request.meta['proxy'] = "http://" + http_proxy.strip("\n")






