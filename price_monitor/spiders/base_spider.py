import json
import scrapy
from datetime import datetime
import os




class BaseSpider(scrapy.Spider):
    def __init__(self, product_name="", start_urls=None, *args, **kwargs):
        self.product_name = product_name
        self.start_urls = start_urls or []
        super().__init__(*args, **kwargs)

    def start_requests(self):
        now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        for url in self.start_urls:
            meta = {
                'product_name': self.product_name,
                'retailer': self.name,
                'when': now
            }
            yield scrapy.Request(url=url, meta={'item': meta})

