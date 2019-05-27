# -*- coding: utf-8 -*-
import json
from urllib.parse import urlparse

import requests

import scrapy
import xlrd

from NewsSpider.endHandle.handler import removeTags, saveToText, getHeader, not_empty
from NewsSpider.items import NewsItem
from NewsSpider.readability.readability import Document


# 示例1：scrapy crawl argumentsSpider -a flag=url -a data=https://baijiahao.baidu.com/s?id=1626484333026259692
# 示例2：scrapy crawl argumentsSpider -a flag=file -a data=c:\Users\YDS\Desktop\urls.xlsx

class ArgumentsSpider(scrapy.Spider):
    name = 'argumentsSpider'
    start_urls = []
    domainURLS = {
        'www.sohu.com/c/': ['http://v2.sohu.com/public-api/feed?scene=CATEGORY','http://www.sohu.com/a/'],
        'news.qq.com/': 'https://pacaio.match.qq.com/irs/rcd?cid=137&token=d0f13d594edfc180f5bf6b845456f3ea&id=&ext=top',
        'www.toutiao.com/ch/':'https://www.toutiao.com/api/pc/feed/?utm_source=toutiao&widen=1'}

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
            #  插入 批量提取函数
            listForURLs = self.returnRightURL(self.data)
            self.start_urls.extend(listForURLs)

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
            number=None
            try:
                number= sheet.cell(i,1).value
            except BaseException as e:
                pass
            #  插入 批量提取函数
            listForURLs = self.returnRightURL(url,number)
            self.start_urls.extend(listForURLs)

    def returnRightURL(self,url,number=None):
        ''' 判断url是否在可批量提取范围内，如果是，在调用对应的提取函数'''
        # 解析url
        urlParse = urlparse(url)
        # print(urlParse)
        yuming = urlParse.netloc
        path = urlParse.path
        pathlist = path.split('/')
        # 去掉最后为空的path：以/结尾的url，统一管理。如https://www.toutiao.com/ch/news_hot/
        newList = list(filter(not_empty, pathlist))
        urlCommon = yuming+path
        # 初始化number
        if number == None:
            number = '0-20'
        for domain in self.domainURLS:
            if domain in urlCommon and 'www.sohu.com'.__eq__(yuming):
                index = newList[-1]
                result =  self.returnSohuURLs(index,number,self.domainURLS[domain])
                print('由链接“%s”批量提取到%d条网页URL'%(url,len(result)))
                # print(result)
                return result
            if domain in urlCommon and 'news.qq.com'.__eq__(yuming) and len(newList)==0:
                result =  self.returnQQURLs(number,self.domainURLS[domain])
                print('由链接“%s”批量提取到%d条网页URL' % (url, len(result)))
                # print(result)
                return result
            if domain in urlCommon and 'www.toutiao.com'.__eq__(yuming):
                # 过滤掉空的path，便于确定 模块 index
                index = newList[-1]
                result = self.returnTouTiaoURLs(index,number,self.domainURLS[domain])
                print('由链接“%s”批量提取到%d条网页URL' % (url, len(result)))
                # print(result)
                return result

        urls = [url]
        return urls

    def returnSohuURLs(self,index,number,dataList):
        '''用于批量提取搜狐新闻
            过程：先模拟后台请求，得到json数据，分析得到文章的id，再将文章的网页前缀与文章id拼接，得到详情页地址'''
        extends = '&sceneId=1460&page=1&size=20'
        page = ''
        rang = number.split('-')

        start = int(rang[0])
        end = int(rang[1])

        pageSize = end -start
        if pageSize <=0:
            print('后缀为：'+index+'的url所配置的数量不合法==>'+range[0]+':'+range[1])
        parameter = '&sceneId='+index
        page = int(end/pageSize)
        parameter =parameter +'&page='+str(page)+'&size='+str(pageSize)
        # response = requests.get(dataList[0]+parameter)

        # 请求头 添加cookie信息
        cookies = requests.cookies.RequestsCookieJar()
        # 添加请求头和cookies
        response = requests.get(dataList[0]+parameter, headers=getHeader(), cookies=cookies)
        content = response.text
        # 将conten字符格式转化为json格式，便于操作
        data = json.loads(content)
        urls = []
        for temp in (data):
            url = dataList[1] + str(temp['id']) + '_' + str(temp['authorId'])
            urls.append(url)
        # print(urls)
        return urls

    def returnQQURLs(self,number,req):
        '''用于批量提取腾讯新闻  只提取新闻，不提取专题
           过程：后台请求时，会携带上次请求所得的id作为参数'''
        # 腾讯新闻一次返回10 个新闻
        pageSize = 10
        rang = number.split('-')
        start = int(rang[0])
        end = int(rang[1])
        pageCount = int((end -start)/pageSize)
        urlList = []
        expIdsList = []

        # 请求头 添加cookie信息
        cookies = requests.cookies.RequestsCookieJar()
        for i in range(pageCount):
            if i == 0:
                url2 = req + '&page=' + str(i) + '&expIds='
            else:
                url2 = req + '&page=' + str(i) + '&expIds=' + '|'.join(str(id) for id in expIdsList)
            expIdsList.clear()
            # response = requests.get(url2)
            # 添加请求头和cookies
            response = requests.get(url2, headers=getHeader(), cookies=cookies)
            # 将数据转为json格式
            conten = json.loads(response.text)
            dataList = conten.get('data')
            for temp in dataList:
                # article_tple为11代表该条新闻指定的是一个专题
                if  (temp['article_type'])!=11:
                    url = temp['vurl']
                    id = temp['id']
                    urlList.append(url)
                    expIdsList.append(id)
                else:
                    pass
                    # print('专题链接：'+temp['vurl'])
        # print('腾讯新闻url数量：%d'%len(urlList))
        # print(urlList)
        return urlList

    def returnTouTiaoURLs(self,index,number,req):
        '''用于批量提取今日头条的新闻
           过程：后台请求时，会携带上次请求中的max_behot_time的值作为参数'''
        max_behot_time = max_behot_time_tmp = 0
        category = index
        rang = number.split('-')
        start = int(rang[0])
        end = int(rang[1])
        pageSize = 10
        pageCount = int((end -start) / pageSize)
        urlList = []
        # 请求头 添加cookie信息
        cookies = requests.cookies.RequestsCookieJar()
        for i in range(pageCount):
            reqUrl = req + '&category=%s&max_behot_time=%d&max_behot_time_tmp=%d' % (
            category, max_behot_time, max_behot_time_tmp)

            print(reqUrl)
            # 添加请求头和cookies
            response = requests.get(reqUrl, headers=getHeader(), cookies=cookies)
            cookies.update(response.cookies)
            content = json.loads(response.text)
            dataList = content['data']
            for data in dataList:
                if 'article'.__eq__(data['article_genre']):
                    itemId = data['item_id']
                    # 请求得到的json数据中，不会包含完整的详情页地址，需要与详情页前缀拼接
                    newsUrl = 'https://www.toutiao.com/a%s' % (itemId)
                    urlList.append(newsUrl)
            # print('urlList长度：%d'%(len(urlList)))
            nextDic = content['next']
            nextId = nextDic['max_behot_time']
            max_behot_time = max_behot_time_tmp = nextId
        # print(urlList)
        return urlList