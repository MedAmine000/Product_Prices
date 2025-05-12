# 📦 Price Monitor — Suivi automatique des prix

Ce projet est une plateforme complète de **monitoring de prix multi-sites** (Amazon, eBay, BestBuy), intégrant des spiders Scrapy, une base MongoDB, une interface Flask et une automatisation via cron ou tâches Windows.

---

## 🧰 Technologies utilisées

- Python 3.10+
- Scrapy
- BestBuy API
- Selenium (pour pages dynamiques)
- Flask (interface web)
- MongoDB (stockage structuré)
- Chart.js (visualisation des prix)
- Cron / Planificateur de tâches (pour l’automatisation)

---

## 🚀 Fonctionnalités

- Ajout d’un produit + 3 liens (Amazon, eBay, BestBuy)
- Lancement automatique des spiders selon les URL
- Insertion intelligente dans MongoDB (évite les doublons)
- Visualisation web des prix et de leur évolution
- Mise à jour manuelle ou automatique (journalier)

---

## 🖥️ Installation

### 1. Clone du projet

```bash
git clone https://github.com/MedAmine000/price_monitor.git
cd price_monitor
```

### 2. Environnement virtuel (Optionnel)

```bash
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate sur Windows
```

### 3. Dépendances

```bash
pip install -r requirements.txt
```

### 4. Installez MongoDB

- [MongoDB Community Edition](https://www.mongodb.com/try/download/community)
- Lancer MongoDB sur `mongodb://localhost:27017`



### 5. Configuration du driver Selenium

Pour scraper des pages dynamiques (ex : Amazon), Selenium nécessite un driver adapté à votre navigateur (ex : ChromeDriver pour Chrome).

1. **Téléchargez le driver** :
    - [ChromeDriver](https://sites.google.com/chromium.org/driver/)
    - [GeckoDriver (Firefox)](https://github.com/mozilla/geckodriver/releases)

2. **Placez le fichier du driver** dans un dossier. Par défaut, le webdriver Chrome est attendu à l’emplacement `C:/Drivers/chromedriver-win64/chromedriver.exe`. Créez ce dossier et placez-y le fichier du driver pour un fonctionnement immédiat, sans modification du code.

3. **Exemple d’utilisation dans un spider** :

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')  # Optionnel : mode sans interface
driver = webdriver.Chrome(options=options, executable_path='C:/Drivers/chromedriver-win64/chromedriver.exe')
driver.get('https://www.amazon.com/')
# ...  code de scraping ...
driver.quit()
```


> **Astuce :** Vérifiez que la version du driver correspond à celle de votre navigateur.


---

## 🕸️ Exécution Manuelle

### 1. Lancer les spiders

Dans `configs/Urls.json`, ajoutez une entrée pour chaque produit à surveiller, par exemple :

```json
{
  "IPHONE 14": [
    "https://www.amazon.com/Apple-iPhone-Starlight-T-Mobile-Renewed/dp/B0BN74TKH5",
    "https://www.bestbuy.com/site/apple-iphone-14-128gb-unlocked-blue/6507560.p?skuId=6507560",
    "https://www.ebay.com/itm/226447947273"
  ]
}
```

Ensuite, exécutez la commande suivante en remplaçant `<nom_du_produit>` par le nom ou l'identifiant du produit à surveiller :

```bash
python run_all_spiders.py --product <nom_du_produit>
```


Cela déclenchera les spiders pour le produit spécifié et collectera les prix sur les différents sites.

---
---

### 🔑 Accès aux données BestBuy

#### Méthode alternative (sans clé API)

Au lieu d'utiliser l'API officielle BestBuy qui nécessite une clé, nous utilisons une approche asynchrone qui :
- Fait des requêtes HTTP directes
- Utilise le SKU extrait de l'URL du produit
- Récupère les données via les endpoints publics de BestBuy

```python
# Exemple d'extraction du SKU depuis une URL BestBuy
url = "https://www.bestbuy.com/site/apple-iphone-14-128gb-unlocked-blue/6507560.p"
sku = "6507560"  # Extrait de l'URL

# L'URL de requête utilisée
api_url = f"https://www.bestbuy.com/api/tcfb/model.json?paths=%5B%5B%22shop%22%2C%22scds%22%2C%22v2%22%2C%22page%22%2C%22tenants%22%2C%22bbypres%22%2C%22pages%22%2C%22globalnavigationv5sv%22%2C%22header%22%5D%2C%5B%22shop%22%2C%22buttonstate%22%2C%22v5%22%2C%22item%22%2C%22skus%22%2C{sku}%5D%5D&method=get"
```

#### Avantages de cette approche
- Pas besoin de clé API
- Données en temps réel
- Requêtes asynchrones plus rapides
- Même format de données que l'API officielle

---
---


### 2. Importer dans MongoDB

```bash
python import_to_mongo.py
```

---

## 🌐 Interface web (Flask)

### Lancer le serveur

```bash
python app.py
```

### Accès

> Ouvrir [http://127.0.0.1:5000](http://127.0.0.1:5000) dans votre navigateur

---


## 📁 Structure

```
.
├── app.py                # Interface Flask
├── configs/Urls.json     # URLs utilisateur
├── outputs/              # Fichiers JSON générés
├── import_to_mongo.py    # Insertion MongoDB
├── run_all_spiders.py    # Orchestrateur de spiders
├── price_monitor/
│   └── spiders/
│       ├── amazon.py
│       ├── bestbuy.py
│       └── ebay.py
├── templates/            # HTML Flask
└── static/               # CSS, JS
```

---


---

## 🤝 Auteurs

- Projet conçu par **MedAmine** — École IPSSI M1

---

## 📝 Licence

Projet éducatif — usage académique uniquement.
