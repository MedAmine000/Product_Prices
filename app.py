from flask import Flask, render_template, request, redirect
import json
import subprocess
import os
from pymongo import MongoClient

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

        # Lancer spiders et import
        subprocess.run(["python", "run_all_spiders.py"])
        subprocess.run(["python", "import_to_mongo.py"])

        return redirect("/results")

    return render_template("index.html")

@app.route("/results")
def results():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["price_monitor"]
    collections = db.list_collection_names()
    results = {}
    for name in collections:
        results[name] = list(db[name].find().sort("when", -1))

    return render_template("results.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
