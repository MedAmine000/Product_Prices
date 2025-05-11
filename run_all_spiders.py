import json
import subprocess
import sys

def run_for_product(product_name, urls):
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

def main():
    try:
        # Si le script est appelé avec un argument --product "Nom produit"
        if "--product" in sys.argv:
            index = sys.argv.index("--product") + 1
            if index >= len(sys.argv):
                print("Erreur : nom du produit manquant après --product")
                sys.exit(1)

            product_to_run = sys.argv[index]
            with open("configs/urls.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            urls = data.get(product_to_run)
            if not urls:
                print(f"Aucune URL trouvée pour {product_to_run}")
                sys.exit(1)

            run_for_product(product_to_run, urls)
        else:
            # Cas normal : traitement de tous les produits
            with open("configs/urls.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            for product_name, urls in data.items():
                run_for_product(product_name, urls)
    except Exception as e:
        print(f"Erreur : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
