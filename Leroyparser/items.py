# Define here the models for your scraped items
#
# See documentation in:

import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def clear_price(value):
    if not value:
        return None
    value = value.replace(' ', '')
    try:
        value = int(value)
    except:
        pass
    finally:
        return value



class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    # name = scrapy.Field()
    photo = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    # price = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    # url = scrapy.Field()
