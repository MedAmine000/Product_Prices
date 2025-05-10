import json
import subprocess

def main():
    with open("configs/urls.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for product_name, urls in data.items():
        print(f"🔍 Produit : {product_name}")
        urls_by_retailer = {
            "amazon": [],
            "bestbuy": [],
            "ebay": []
        }

        for url in urls:
            for retailer in urls_by_retailer:
                if retailer in url:
                    urls_by_retailer[retailer].append(url)

        for retailer, retailer_urls in urls_by_retailer.items():
            if not retailer_urls:
                continue

            print(f"▶ Lancement du spider {retailer} pour {product_name}")
            subprocess.run([
                "python", "launch_spider.py",
                retailer,
                product_name,
                json.dumps(retailer_urls)
            ])


if __name__ == "__main__":
    main()
