from flask import Flask, render_template, request, redirect
import json
import subprocess
import os
from pymongo import MongoClient
from collections import defaultdict


app = Flask(__name__)

URLS_PATH = "./configs/Urls.json"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        product_name = request.form["product_name"]
        amazon = request.form["amazon"]
        bestbuy = request.form["bestbuy"]
        ebay = request.form["ebay"]

        # Création du fichier s’il n’existe pas
        if not os.path.exists(URLS_PATH):
            with open(URLS_PATH, "w", encoding="utf-8") as f:
                json.dump({}, f)

        # Chargement du fichier
        with open(URLS_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

        # Ajout du produit
        data[product_name] = [amazon, bestbuy, ebay]

        with open(URLS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        

        # Lancer spiders et attendre la fin avant d'importer
        subprocess.run(["python", "run_all_spiders.py", "--product", product_name], check=True)
        subprocess.run(["python", "import_to_mongo.py"], check=True)

        return redirect("/results")

    return render_template("index.html")

@app.route("/results")
def results():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["price_monitor"]
    grouped = defaultdict(list)

    for collection in db.list_collection_names():
        for doc in db[collection].find().sort("when", -1):
            grouped[doc["product_name"]].append(doc)

    return render_template("results.html", grouped_results=grouped)


@app.route("/update/<product>", methods=["POST"])
def update_product(product):
    # Lire URLs.json
    with open(URLS_PATH, "r", encoding="utf-8") as f:
        url_data = json.load(f)

    urls = url_data.get(product, [])
    if not urls:
        return f"Aucune URL pour {product}", 400

    # Lancer run_all_spiders et import uniquement pour ce produit
    subprocess.run(["python", "run_all_spiders.py", "--product", product], check=True)
    subprocess.run(["python", "import_to_mongo.py"], check=True)
    return redirect("/results")


from collections import defaultdict

@app.route("/evolution/<product>")
def evolution(product):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["price_monitor"]

    # Regrouper les données par retailer
    data = defaultdict(list)

    for collection in db.list_collection_names():
        cursor = db[collection].find({"product_name": product}).sort("when", 1)
        for doc in cursor:
            data[doc["retailer"]].append({
                "price": float(doc["price"]),
                "when": doc["when"]
            })

    if not data:
        return render_template("evolution.html", product_name=product, chart_data={})

    # Préparer les données pour Chart.js
    chart_data = {}
    for retailer, records in data.items():
        chart_data[retailer] = {
            "dates": [r["when"] for r in records],
            "prices": [r["price"] for r in records]
        }

    return render_template("evolution.html", product_name=product, chart_data=chart_data)


@app.route("/schedule/<product>", methods=["POST"])
def schedule_cron(product):
    cron_hour = request.form["cron_hour"]
    hour, minute = map(int, cron_hour.split(":"))

    # Commande à exécuter
    cmd = f'"python {os.path.abspath("run_all_spiders.py")} --product \\"{product}\\" && python {os.path.abspath("import_to_mongo.py")}"'
    # Nom unique pour la tâche
    task_name = f"PriceMonitor_{product.replace(' ', '_')}"

    # Supprimer l'ancienne tâche si elle existe
    os.system(f'schtasks /Delete /TN "{task_name}" /F')

    # Créer la nouvelle tâche planifiée
    os.system(
        f'schtasks /Create /SC DAILY /TN "{task_name}" /TR {cmd} /ST {hour:02d}:{minute:02d} /F'
    )

    print(f"✅ Tâche planifiée pour {product} à {cron_hour}")

    return redirect("/results")



if __name__ == "__main__":
    app.run(debug=False)
