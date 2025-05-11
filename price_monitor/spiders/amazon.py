from .base_spider import BaseSpider
import json


class AmazonSpider(BaseSpider):
    name = "amazon"


    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.css("span#productTitle::text").extract_first("").strip()
        price_text = response.css("span.a-offscreen::text").extract_first("")
        item['price'] = float(price_text.replace("$", "").replace(",", "").strip() or 0)

        yield item

