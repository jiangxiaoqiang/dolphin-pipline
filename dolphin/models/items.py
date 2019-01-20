import scrapy

class IndustryIdentifiersItem(scrapy.Item):
    type = scrapy.Field()
    identifier = scrapy.Field()

class BookItem(scrapy.Item):
    name = scrapy.Field()
    isbn = scrapy.Field()
    publisher = scrapy.Field()
    author = scrapy.Field()
    publish_year = scrapy.Field()
    binding = scrapy.Field()
    price = scrapy.Field()
    subtitle = scrapy.Field()
    original_name = scrapy.Field()
    translator = scrapy.Field()
    pages = scrapy.Field()
    issuer = scrapy.Field()
    creator = scrapy.Field()
    douban_id = scrapy.Field()
    source = scrapy.Field()
    isbn10 = scrapy.Field()
    industry_identifiers = scrapy.Field(serializer=IndustryIdentifiersItem)

