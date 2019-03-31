# -*- coding: utf-8 -*-
import scrapy
import xlrd

from NewsSpider.endHandle.handler import removeTags, saveToText
from NewsSpider.items import NewsItem
from NewsSpider.readability.readability import Document


# 示例1：scrapy crawl argumentsSpider -a flag=url -a data=https://baijiahao.baidu.com/s?id=1626484333026259692
# 示例2：scrapy crawl argumentsSpider -a flag=file -a data=c:\Users\YDS\Desktop\urls.xlsx

class ArgumentsSpider(scrapy.Spider):
    name = 'argumentsSpider'
    start_urls = []


    def __init__(self,flag,data, *args, **kwargs):
        ''' 从命令行中获取数据
        :param flag: 有两种情况，‘url’ 代表data的值为一个url; 'file' 代表data的值为一个file的路径
        :param data: 可以为url 或者是一个文件的路径
        :param args: 待定
        :param kwargs: 待定
        '''
        super(ArgumentsSpider, self).__init__(*args, **kwargs)
        self.flag = flag
        self.data = data
        if flag:
            if (flag =='url'):
                self.getUrl()
            elif (flag =='file'):
                self.getFile()
            else:
                self.logger.error('入参flag的值不合法！flag='+flag)
        else:
            self.logger.info('请注意入参个数计格式，flag疑似为空！')

    def parse(self, response):
        self.logger.info(response.status)
        html = response.text
        doc = Document(html)
        summary = doc.summary()
        title = doc.title()
        # print(summary)
        text = removeTags(summary)
        contenPath = saveToText(title, text)
        item = NewsItem()
        item['title'] = title
        item['url'] = response.url
        item['contenPath'] = contenPath
        yield item


    def getUrl(self):
        if self.data:
            self.start_urls.append(self.data)

    def getFile(self):
        # 文件路径中文转码
        # filePath = self.data.encode('utf-8')
        excle = xlrd.open_workbook(self.data)
        sheet = excle.sheet_by_index(0)  # 索引的方式，从0开始
        # sheet = excle.sheet_by_name('sheet2')  # 名字的方式
        nrows = sheet.nrows  # 行
        ncols = sheet.ncols  # 列
        for i in range(1,nrows):
            url = sheet.cell(i,0).value
            self.start_urls.append(url)
