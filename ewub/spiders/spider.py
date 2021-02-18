import scrapy

from scrapy.loader import ItemLoader
from ..items import EwubItem
from itemloaders.processors import TakeFirst


class EwubSpider(scrapy.Spider):
	name = 'ewub'
	start_urls = ['https://www.ewub.lu/-Corporate-News-?lang=en']

	def parse(self, response):
		post_links = response.xpath('//article/h3')
		for post in post_links:
			url = post.xpath('./a/@href').get()
			date = post.xpath('./span/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h3/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::h3)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=EwubItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
