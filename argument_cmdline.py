import shlex

import pymongo
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
    fileList = filePath.split('|')
    for path in fileList:
        print('正在解析"%s"' % path)
        # 实现实时刷新界面，一般用于耗时的程序或者会对界面修改的程序
        parseLocalFile(path)
        print("解析" + path + "完成！！")

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
    '''测试后台日志信息获取'''
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
            line = p.stdout.readline().decode('utf-8','ignore')
            line = line.strip()
            if line:
                print('output: [{}]'.format(line))
        if p.returncode == 0:
            print('Subprogram success')

        else:
            print('Subprogram failed')

    except BaseException as e:
        print('程序发生异常：',e.traceback.print_exc())

def testForMongodb(mongo_url,dbName,item):
    '''测试后台数据库连接'''
    client = pymongo.MongoClient(mongo_url)
    db = client[dbName]
    db[dbName].insert(dict(item))
    client.close()



def main():
    # # 测试批量
    # excleFilePath = r'c:\Users\YDS\Desktop\file\testForMore - 副本.xlsx'  # testForMore.xlsx ; urls.xlsx
    # testForExcleFile(excleFilePath)
    # # 测试单次
    # urlForSouhu = 'http://www.sohu.com/c/8/1460'
    # urlForQQ = 'https://news.qq.com/'
    # urlForToutiao = 'https://www.toutiao.com/ch/news_hot/'
    # url = urlForQQ
    # testForUrl(url)
    # 测试本地
    htmlFilePath = "C:/Users/YDS/Desktop/file/html/10年前让“清华”破例降60分录取的女生蒋方舟，现在过得如何了？.html|C:/Users/YDS/Desktop/file/html/69人院内感染丙肝，规则失守是最大敌人_江苏东台.html|C:/Users/YDS/Desktop/file/html/高考狂人张非4次高考、2次清华、1次北大、1次复旦，现在如何？.html|C:/Users/YDS/Desktop/file/html/个别标准组织暂停与华为合作 华为：不影响公司正常运作_产业.html|C:/Users/YDS/Desktop/file/html/还原南阳水氢车技术争议：专家称只加水是误解，关键在于制氢材料_汽车.html|C:/Users/YDS/Desktop/file/html/什么样的家庭出学霸？大数据研究结果，颠覆你的认知！.html|C:/Users/YDS/Desktop/file/html/微软、通用电气等致信美国政府：封杀中国企业将“引火烧身”.html|C:/Users/YDS/Desktop/file/html/微软等警告特朗普政府：封杀华为将削弱美创新能力--今日热点--国际--首页.html|C:/Users/YDS/Desktop/file/html/习近平总书记重要指示催人奋进 老英雄张富清事迹彰显奉献精神--高层--时政要闻--时政--首页.html"

    testForHtmlFile(htmlFilePath)
if __name__ == '__main__':
    main()

