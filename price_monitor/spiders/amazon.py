from .base_spider import BaseSpider
import json

class AmazonSpider(BaseSpider):
    name = "amazon"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.css("span#productTitle::text").extract_first("").strip()

        # Liste des sélecteurs à tester pour le prix
        selectors = [
            "span.a-offscreen::text",
            "span.a-price-whole::text",
            # Ajoute ici d'autres sélecteurs si besoin
        ]

        price_text = ""
        for selector in selectors:
            price_text = response.css(selector).extract_first("")
            if price_text:
                break

        # Nettoyage du texte du prix
        price_text = price_text.replace("$", "").replace(",", "").strip()
        try:
            item['price'] = float(price_text or 0)
        except ValueError:
            item['price'] = 0.0

        yield item