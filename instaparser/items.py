# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    followerid = scrapy.Field()
    followername = scrapy.Field()
    followerphoto = scrapy.Field()

    followingid = scrapy.Field()
    followingname = scrapy.Field()
    followingphoto = scrapy.Field()






