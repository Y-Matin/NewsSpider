import scrapy

from NewsSpider.endHandle.handler import removeTags, saveToText
from NewsSpider.items import NewsItem
from NewsSpider.readability.readability import Document


def saveToMongodb(title, contenPath, publish='', author='', time=''):
    item = NewsItem()
    if title:
        item['title'] = title
    if publish:
        item['publish'] = publish
    if author:
        item['author'] = author
    if time:
        item['time'] = time
    if contenPath:
        item['contenPath'] = contenPath

    yield item


class GetTextSpider (scrapy.Spider):
    name = 'getText'
    start_urls = ['https://m.sohu.com/a/295958372_267106?_f=m-index_top_news_3&spm=smwp.home.hot-news.2.1550717779845OwKNbGY'
                  ]

    def parse(self, response):
        html = response.text
        doc = Document(html)
        summary = doc.summary()
        title = doc.title()
        print(summary)
        text = removeTags(summary)
        contenPath = saveToText(title,text)
        # saveToMongodb(title,contenPath)
        item = NewsItem()
        item['title'] = title
        item['contenPath'] = contenPath
        yield item
