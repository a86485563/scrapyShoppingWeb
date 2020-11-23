# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
def serialize_data(value:str):
    return value.strip()


class ShoppingwebItem(scrapy.Item):
    name = scrapy.Field(serializer=serialize_data)
    price = scrapy.Field()
    status = scrapy.Field()
    link = scrapy.Field()
