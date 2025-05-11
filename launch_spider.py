# launch_spider.py
import sys
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from importlib import import_module
import os

def main():
    spider_name = sys.argv[1]
    product_name = sys.argv[2]
    urls = json.loads(sys.argv[3])  # on passe la liste de start_urls encodée
    
    os.makedirs("outputs", exist_ok=True)

    filename = f"outputs/{spider_name}_{product_name.replace(' ', '_')}.json"
    # Supprimer le contenu du fichier s'il existe
    open(filename, "w").close()

    settings = get_project_settings()
    settings.set("FEEDS", {
        filename: {
            "format": "json",
            "encoding": "utf8",
            "overwrite": True
        }
    })
    # settings = get_project_settings()
    process = CrawlerProcess(settings)

    spider_module = f"price_monitor.spiders.{spider_name}"
    spider_class = getattr(import_module(spider_module), f"{spider_name.capitalize()}Spider")

    process.crawl(spider_class, product_name=product_name, start_urls=urls)
    process.start()


if __name__ == "__main__":
    main()
