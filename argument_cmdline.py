import shlex

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

from NewsSpider.endHandle.handler import parseLocalFile, removeTags, saveToText
from NewsSpider.items import NewsItem
from NewsSpider.readability.readability import Document


def testForExcleFile(filePath):
    '''测试批量提取功能'''
    # cmdline.execute(("scrapy crawl argumentsSpider -a flag=file -a data="+filePath).split())
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl('argumentsSpider', flag='file', data=filePath)
    process.start()

def testForUrl(url):
    '''测试单次提取功能'''
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    process = CrawlerProcess(get_project_settings())
    process.crawl('argumentsSpider', flag='url', data=url)
    process.start()

def testForHtmlFile(filePath):
    '''测试本地导入功能'''
    parseLocalFile(filePath)

def testForExcute(html):
    '''测试提取功能'''
    doc = Document(html)
    summary = doc.summary()
    title = doc.title()
    # print(summary)
    text = removeTags(summary)
    contenPath = saveToText(title, text)
    print(contenPath)

def testForLog(shell_cmd):
    pass
    cmd = "scrapy crawl argumentsSpider -a flag=url -a data="
    # cmdline.execute((cmd + url).split())
    try:
        # os.system(cmd + url)
        # process.crawl('argumentsSpider', flag='url', data=url)
        # process.start()

        cmd = shlex.split(shell_cmd)
        import subprocess
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            # line = p.stdout.readline().decode('utf-8', 'ignore')
            line = p.stdout.readline().decode('utf-8',ignore)
            line = line.strip()
            if line:
                print('output: [{}]'.format(line))
        if p.returncode == 0:
            print('Subprogram success')

        else:
            print('Subprogram failed')

    except BaseException as e:
        print('程序发生异常：',e.traceback.print_exc())

def main():
    # 测试批量
    excleFilePath = r'c:\Users\YDS\Desktop\file\testForMore - 副本.xlsx'  # testForMore.xlsx ; urls.xlsx
    testForExcleFile(excleFilePath)
    # 测试单次
    urlForSouhu = 'http://www.sohu.com/c/8/1460'
    urlForQQ = 'https://news.qq.com/'
    urlForToutiao = 'https://www.toutiao.com/ch/news_hot/'
    url = urlForQQ
    testForUrl(url)
    # 测试本地
    htmlFilePath = "C:\\Users\\YDS\Desktop\\html\\湖南道县通报“学校克扣学生伙食”：不实，符合伙食成本要求.htm"
    testForHtmlFile(htmlFilePath)
if __name__ == '__main__':
    main()

