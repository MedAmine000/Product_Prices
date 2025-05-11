from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import scrapy
import time
import logging
from .base_spider import BaseSpider


class BestbuySpider(BaseSpider):
    name = "bestbuy"

    def __init__(self, *args, **kwargs):
        logging.info("Initialisation du spider BestBuy")
        super().__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=Service("C:/Drivers/chromedriver-win64/chromedriver.exe"), options=chrome_options)

    def parse(self, response):
        logging.info("Chargement de l'URL BestBuy avec bypass : %s", response.url)

        # Ajout du paramètre pour éviter la page de sélection
        url = response.url
        if "?" in url:
            url += "&intl=nosplash"
        else:
            url += "?intl=nosplash"

        self.driver.get(url)
        time.sleep(5)

        # Lire le contenu de la page rendue
        rendered_body = self.driver.page_source
        response = HtmlResponse(
            url=self.driver.current_url,
            body=rendered_body,
            encoding='utf-8',
            request=response.request  # Associer la requête originale
        )
        # Sauvegarder le HTML rendu pour le débogage
        # with open("bestbuy_rendered.html", "w", encoding="utf-8") as f:
        #     f.write(rendered_body)

        # Créer l’item
        item = response.meta.get('item', {})
        item['url'] = response.url

        # Extraire le titre en utilisant la méthode CSS
        title_css = response.css("div#sku-title > h1 ::text").extract_first()
        if title_css:
            item['title'] = title_css.strip()
        else:
            # Extraire le titre en utilisant la méthode XPath comme fallback
            title_xpath = response.xpath("//title/text()").get(default="")
            item['title'] = title_xpath.strip()

        # Extraire le prix
        price_text = response.css("div.priceView-hero-price span[aria-hidden='true']::text").get(default="")
        if price_text:
            item['price'] = float(price_text.replace("$", "").replace(",", "").strip())
        else:
            item['price'] = None

        logging.info(f"Titre : {item['title']}")
        logging.info(f"Prix : {item['price']}")

        yield item

    def closed(self, reason):
        self.driver.quit()