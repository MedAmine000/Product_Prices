from .base_spider import BaseSpider
from price_monitor.utils import get_bestbuy_product_data  # adapte selon l’emplacement de ta fonction

class BestbuySpider(BaseSpider):
    name = "bestbuy"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url

        # Appeler la fonction externe
        product_data = get_bestbuy_product_data(response.url)

        if product_data:
            item['title'] = product_data.get("Titre")
            item['price'] = product_data.get("price")
        else:
            item['title'] = None
            item['price'] = None

        yield item
