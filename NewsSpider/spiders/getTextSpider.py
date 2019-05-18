import scrapy

from NewsSpider.endHandle.handler import removeTags, saveToText
from NewsSpider.items import NewsItem
from NewsSpider.readability.readability import Document


class GetTextSpider (scrapy.Spider):
    name = 'getText'
    start_urls = ['http://news.iciba.com/study/bilingual/1580005.shtml']

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
        item['url'] = response.url
        item['contenPath'] = contenPath
        yield item
