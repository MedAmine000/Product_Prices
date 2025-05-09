from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
import scrapy
import time
import logging


from .base_spider import BaseSpider


import scrapy

class BestbuySpider(BaseSpider):
    name = "bestbuy"

    # def __init__(self, *args, **kwargs):
    #     logging.info("Initializing BestbuySpider")
    #     super().__init__(*args, **kwargs)
    #     chrome_options = Options()
    #     chrome_options.add_argument("--headless")  # Run in headless mode
    #     chrome_options.add_argument("--disable-gpu")
    #     chrome_options.add_argument("--no-sandbox")
    #     self.driver = webdriver.Chrome(service=Service("C:/Drivers/chromedriver-win64/chromedriver.exe"), options=chrome_options)

    # async def start(self):
    #     logging.info("Executing start method")
    #     url = "https://www.bestbuy.ca/fr-ca/produit/16553671"  # Replace with a valid Best Buy product URL
    #     yield scrapy.Request(url, callback=self.parse)

    # def parse(self, response):
    #     logging.info("Executing parse method for URL: %s", response.url)

    #     self.driver.get(response.url)
    #     time.sleep(10)  # Wait for the JavaScript to load
    #     logging.info("Page loaded successfully")

    #     # Simulate a Scrapy response using the rendered page source
    #     rendered_body = self.driver.page_source
    #     response = HtmlResponse(url=self.driver.current_url, body=rendered_body, encoding='utf-8')

    #     # Log the rendered HTML for debugging
    #     with open("rendered_page.html", "w", encoding="utf-8") as f:
    #         f.write(rendered_body)

    #     item = response.meta.get('item', {})
    #     item['url'] = response.url
    #     item['title'] = response.css("h1.font-best-buy::text").extract_first("").strip()
    #     item['price'] = float(
    #         response.css("span[data-automation='product-price'] span::text")
    #         .re_first(r"(\d+\.\d+)") or 0
    #     )
    #     yield item

    # def closed(self, reason):
    #     self.driver.quit()

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.css("h1.font-best-buy::text").extract_first("").strip()
        item['price'] = float(
            response.css("span[data-automation='product-price'] span::text")
            .re_first(r"(\d+\.\d+)") or 0
        )
        yield item