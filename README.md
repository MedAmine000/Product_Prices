

---


#### b. **Installer les Bibliothèques Python**
- Installez les bibliothèques nécessaires en exécutant la commande suivante dans un terminal :
  ```bash
  pip install scrapy selenium
  ```

#### c. **Télécharger Chrome et ChromeDriver**
- Téléchargez et installez Google Chrome.
- Téléchargez la version correspondante de ChromeDriver depuis [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads).
- Placez le fichier `chromedriver.exe` dans un dossier accessible, par exemple : chromedriver-win64.

---



#### a. **Structure du Projet**
Voici la structure du projet que tu dois avoir :
```
price_monitor/
├── price_monitor/
│   ├── spiders/
│   │   ├── base_spider.py
│   │   ├── bestbuy.py
│   ├── settings.py
├── outputs/
├── congigs/
│   ├── Urls.json
```

- Placez le fichier bestbuy.py dans le dossier `spiders`.

#### b. **Vérifier le Chemin de ChromeDriver**
- Dans le fichier bestbuy.py, vérifiez que le chemin vers `chromedriver.exe` est correct :
  ```python
  self.driver = webdriver.Chrome(service=Service("C:/Drivers/chromedriver-win64/chromedriver.exe"), options=chrome_options)
  ```

---

### 3. **Exécuter le Script**
exécuter le script en suivant ces étapes :

#### a. **Se Placer dans le Répertoire du Projet**
- Ouvrez un terminal et naviguez vers le dossier racine du projet :
  ```bash
  cd path/to/price_monitor
  ```

#### b. **Lancer le Spider**
- Exécutez la commande suivante pour lancer le spider et sauvegarder les résultats dans un fichier JSON :
  ```bash
  scrapy crawl bestbuy.com -o outputs/bestbuy.json
  ```

#### c. **Vérifier les Résultats**
- Les résultats seront sauvegardés dans le fichier bestbuy.json.

---

### 4. **Dépannage**
Si tu rencontre des problèmes

#### a. **Problème avec ChromeDriver**
- Vérifiez que la version de ChromeDriver correspond à la version de Google Chrome installée.
- Si nécessaire, téléchargez la bonne version depuis [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads).

#### b. **Problème avec les Sélecteurs CSS**
- Si les données ne sont pas extraites correctement, vérifiez les sélecteurs CSS dans le fichier bestbuy.py :
  - **Titre** : `h1.font-best-buy::text`
  - **Prix** : `span[data-automation='product-price'] span::text`

#### c. **Problème avec `robots.txt`**
- Si le spider est bloqué par `robots.txt`, désactivez cette restriction dans `settings.py` :
  ```python
  ROBOTSTXT_OBEY = False
  ```

---

### 5. **Personnalisation**
Si votre collègue souhaite scraper d'autres pages ou produits, il peut modifier l'URL dans la méthode `start` :
```python
url = "https://www.bestbuy.ca/fr-ca/produit/16553671"
```

---

### 6. **Documentation**
Fournissez également une brève explication du fonctionnement du script :
- **`start`** : Démarre le scraping avec une URL spécifique.
- **`parse`** : Utilise Selenium pour charger la page, extrait les données (titre et prix), et les sauvegarde.

---

Avec ces instructions, votre collègue devrait être en mesure de configurer et d'exécuter le script de scraping pour Best Buy.