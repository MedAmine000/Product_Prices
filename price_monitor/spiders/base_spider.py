import json
import scrapy
from datetime import datetime
import os


class BaseSpider(scrapy.Spider):

    def start_requests(self):
        path = os.path.join(os.path.dirname(__file__), '..', '..', 'configs', 'urls.json')
        with open(path, encoding='utf-8') as f:
            products = json.load(f)

        for name, urls in products.items():
            for url in urls:
                if self.name in url:
                    now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                    item = {'product_name': name, 'retailer': self.name, 'when': now}
                    yield scrapy.Request(url, meta={'item': item})
