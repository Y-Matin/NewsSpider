from scrapy import cmdline
import sys

import NewsSpider.settings
import NewsSpider.spiders

import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.dupefilters
import scrapy.squeues
import scrapy.extensions.spiderstate
import scrapy.extensions.corestats
import scrapy.extensions.telnet
import scrapy.extensions.logstats
import scrapy.extensions.memusage
import scrapy.extensions.memdebug
import scrapy.extensions.feedexport
import scrapy.extensions.closespider
import scrapy.extensions.debug
import scrapy.extensions.httpcache
import scrapy.extensions.statsmailer
import scrapy.extensions.throttle
import scrapy.core.scheduler
import scrapy.core.engine
import scrapy.core.scraper
import scrapy.core.spidermw
import scrapy.core.downloader
import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.useragent
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.ajaxcrawl
import scrapy.downloadermiddlewares.decompression
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpcompression
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.robotstxt
import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength
import scrapy.pipelines
import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.contextfactory

from NewsSpider.endHandle.handler import parseLocalFile


def testForExcleFile(filePath):

    # cmdline.execute(("scrapy crawl argumentsSpider -a flag=file -a data="+filePath).split())
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())  # 程序意外出错
    process.crawl('argumentsSpider', flag='file', data=filePath)
    process.start()

def testForUrl(url):
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    process = CrawlerProcess(get_project_settings())  # 程序意外出错
    process.crawl('argumentsSpider', flag='url', data=url)
    process.start()



def testForHtmlFile(filePath):
    parseLocalFile(filePath)

def main():
    excleFilePath = r'c:\Users\YDS\Desktop\testForMore.xlsx'  # testForMore.xlsx ; urls.xlsx
    testForExcleFile(excleFilePath)

    # urlForSouhu = 'http://www.sohu.com/c/8/1460'
    # urlForQQ = 'https://news.qq.com/'
    # urlForToutiao = 'https://www.toutiao.com/ch/news_hot/'
    # testForUrl(url)

    # htmlFilePath = ''
    # testForHtmlFile(htmlFilePath)
if __name__ == '__main__':
    main()

