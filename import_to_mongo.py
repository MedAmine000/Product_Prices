import os
import json
from pymongo import MongoClient
from datetime import datetime
from hashlib import md5

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["price_monitor"]  # nom de la base de données

# Dossier contenant les fichiers JSON générés par les spiders
OUTPUT_DIR = "outputs"

# Parcours de tous les fichiers .json dans le dossier
for filename in os.listdir(OUTPUT_DIR):
    if filename.endswith(".json"):
        product_collection = filename.replace(".json", "")  # nom de la collection
        collection = db[product_collection]
        file_path = os.path.join(OUTPUT_DIR, filename)

        with open(file_path, encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data, list) and data:
                    inserted = 0
                    for item in data:
                        item['imported_at'] = datetime.utcnow()
                        key = item["url"] + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        item['unique_key'] = md5(key.encode()).hexdigest()
                        if not collection.find_one({"unique_key": item['unique_key']}):
                            collection.insert_one(item)
                            inserted += 1
                    if inserted > 0:
                        print(f"✅ {inserted} éléments insérés dans '{product_collection}'")
                    else:
                        print(f"⚠️ Aucun nouvel élément inséré pour '{product_collection}'")
                elif isinstance(data, list) and not data:
                    print(f"⚠️ Fichier vide : {filename}")
                else:
                    print(f"❌ Format inattendu dans : {filename}")
            except json.JSONDecodeError as e:
                print(f"❌ Erreur JSON dans {filename}: {e}")
        # Suppression du fichier après traitement
        os.remove(file_path)
