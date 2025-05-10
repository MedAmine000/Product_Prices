from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
import scrapy
import time
import re
import logging
from .base_spider import BaseSpider


class EbaySpider(BaseSpider):
    name = "ebay"

    def __init__(self, *args, **kwargs):
        logging.info("Initialisation du spider eBay")
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(service=Service("C:/Drivers/chromedriver-win64/chromedriver.exe"), options=chrome_options)

    def parse(self, response):
        logging.info("Chargement de la page eBay : %s", response.url)

        self.driver.get(response.url)
        time.sleep(5)

        rendered_body = self.driver.page_source
        response = HtmlResponse(
            url=self.driver.current_url,
            body=rendered_body,
            encoding='utf-8',
            request=response.request
        )

        # Sauvegarder le HTML rendu pour le débogage
        # with open("ebay_rendered.html", "w", encoding="utf-8") as f:
        #     f.write(rendered_body)

        item = response.meta.get('item', {})
        item['url'] = response.url

        # Extraction du titre
        title = response.css("h1.x-item-title__mainTitle span::text").get()
        item['title'] = title.strip() if title else ""

        # Extraction du prix
        price_text = response.css("div.x-price-primary span.ux-textspans::text").get()
        if price_text:

            # Nettoyage complet du texte
            clean_price = re.findall(r"[\d\.,]+", price_text)
            if clean_price:
                item['price'] = float(clean_price[0].replace(",", ""))
            else:
                item['price'] = None
        else:
            item['price'] = None

        logging.info(f"Titre : {item['title']}")
        logging.info(f"Prix : {item['price']}")

        yield item

    def closed(self, reason):
        self.driver.quit()
