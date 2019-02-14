import scrapy

from NewsSpider.readability.readability import Document


class GetTextSpider (scrapy.Spider):
    name = 'getText'
    start_urls = ['https://baijiahao.baidu.com/s?id=1625409909818613828&wfr=spider&for=pc']

    def parse(self, response):
        html = response.text
        doc = Document(html)
        text = doc.summary()
        print(text)