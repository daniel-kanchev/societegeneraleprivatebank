import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from societegeneraleprivatebank.items import Article


class SocietegeneraleprivatebankSpider(scrapy.Spider):
    name = 'societegeneraleprivatebank'
    start_urls = ['https://www.privatebanking.societegenerale.ch/fr/presse/communiques-presse/']

    def parse(self, response):
        links = response.xpath('//div[@class="wallCardItems"]//div[@class="wallCardRow wallCardRow_card"]//a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="mainTitle"]//text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="sgnews_single_date"]/text()').get()
        if date:
            date = date.strip()
        else:
            return

        content = response.xpath('//div[@class="sgnews_single_content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
