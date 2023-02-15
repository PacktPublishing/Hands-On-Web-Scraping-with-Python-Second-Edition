# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    no_review = scrapy.Field()
    upc = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    stock = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    
    pass
