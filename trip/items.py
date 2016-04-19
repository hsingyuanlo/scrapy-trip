# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class TripItem(Item):
    pass


class CountyUrlItem(Item):
    name = Field()
    link = Field()


class CountyViewUrlItem(Item):
    name = Field()
    county = Field()
    category = Field()
    link = Field()


class ViewItem(Item):
    name = Field()
    county = Field()
    category = Field()
    contact = Field()
    address = Field()
    latitude = Field()
    longitude = Field()


class LocationItem(Item):
    id = Field()
    pid = Field()
    name = Field()


class WeatherItem(Item):
    id = Field()
    temp_c = Field()
    pop = Field()
