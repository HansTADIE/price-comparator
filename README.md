# Price Comparator — Comparateur de prix (Projet académique)

> **Résumé simple**  
> Ce projet rassemble automatiquement des informations (prix, images, lien) de chaussures sur trois sites marchands (Zalando, Courir, Spartoo), stocke ces données dans une base et propose une interface web pour comparer les articles.

---

## Public visé
Ce README s’adresse à :
- des personnes non techniques qui veulent comprendre à quoi sert le projet ;
- des développeurs qui veulent l’installer et le tester ;
- des évaluateurs pédagogiques souhaitant vérifier le fonctionnement.

---

## 1) À quoi sert ce projet ? (explication non technique)
Le but est de **comparer les prix et les informations produits** trouvés sur plusieurs sites de vente en ligne.

Fonctionnalités principales :
- Récupération automatique des données depuis 3 sites de e-commerce (spiders).
- Stockage des données dans une base de données (MySQL).
- Interface web simple : bouton pour lancer le scraping et page pour afficher un tableau comparatif (photo, prix, lien).
- Le tout s’exécute dans des **conteneurs Docker** pour simplifier l’installation.

---

## 2) Structure du projet (explication simple)
price-comparator/
├── docker-compose.yml # orchestration des conteneurs
├── scrapers/ # projet Scrapy (spiders pour chaque site)
│ ├── Dockerfile
│ └── items_comparator/ # spiders, pipelines, settings...
├── webapp/ # application Flask (interface web)
│ ├── Dockerfile
│ ├── app.py
│ └── templates/, static/
├── database/
│ └── init.sql # script d'initialisation de la base
└── README.md

---

## 3) Description simple du flux (ce qui se passe réellement)
1. Tu cliques sur **"Scraper"** dans l’interface web.  
2. Le serveur lance, dans l’ordre, trois petits programmes (les spiders) qui visitent Zalando, Courir et Spartoo et récupèrent titre, prix, image et lien de chaque produit.  
3. Les résultats sont insérés dans la table `products` de la base MySQL.  
4. La page **/products** affiche un tableau comparatif avec les images (liens affichés comme images) et les hyperliens vers les fiches produits.

---

## 4) Exemple simple de données (ligne de la table `products`)
| id | titre                  | prix   | image                          | lien                          | site     | scraped_at           |
|----|------------------------|--------|--------------------------------|-------------------------------|----------|----------------------|
| 1  | "Sneaker XYZ"          | 89.99  | https://.../image.jpg          | https://.../product.html      | zalando  | 2025-12-29 18:15:32  |

La table contient un identifiant, le titre (nom), le prix, l’URL de l’image, le lien du produit, le nom du site et la date du scraping.

---

## 5) Installation et exécution (recommandé : Docker)

### Prérequis
- Installer **Docker** et **Docker Compose** (version 2+).
- Cloner le dépôt :
git clone <ton-repo-url>
cd price-comparator
Lancer les services (manuel simple)
Arrêter d’éventuels conteneurs précédents :

bash
Copier le code
docker-compose down -v
Construire les images et installer les dépendances :

bash
Copier le code
docker-compose build --no-cache
Démarrer les services :

bash
Copier le code
docker-compose up
Accès
Interface web (Flask) : http://localhost:5000

Page principale avec bouton Scraper

Page résultats : http://localhost:5000/products

phpMyAdmin (si inclus) : http://localhost:8080 (pour inspecter la base)

Connexion MySQL : user / password (configurable dans docker-compose.yml)

---

## 6) Commandes utiles pour debug
Entrer dans le conteneur webapp :

bash
Copier le code
docker exec -it price_comparator_webapp bash
python -m scrapy version   # vérifier que Scrapy est disponible
Lancer un spider manuellement (dans le conteneur qui contient les spiders) :

bash
Copier le code
cd /app/items_comparator
python -m scrapy crawl zalando
Se connecter à la base MySQL :

bash
Copier le code
docker exec -it price_comparator_db mysql -uuser -ppassword price_comparator
puis ex: SELECT * FROM products LIMIT 20;

---

## 7) Problèmes fréquents et solutions
Erreur scrapy-playwright introuvable lors du pip install
→ utiliser une version compatible (ex. scrapy-playwright==0.0.44) dans requirements.txt, puis rebuild.

Erreur MySQL Unknown MySQL server host 'db'
→ cela signifie que le conteneur qui essaye de joindre la base n’est pas sur le même réseau Docker. Vérifier docker-compose.yml : tous les services (webapp, scrapers, db) doivent être sur le même réseau.

scrapy: command not found dans Flask
→ vérifier que Scrapy est bien installé dans l’image webapp ou utiliser python -m scrapy pour garantir le même interpréteur Python.

---

## 8) Exécuter sans Docker (optionnel, pour développeurs)
Créer un environnement Python :

bash
Copier le code
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r webapp/requirements.txt
pip install -r scrapers/requirements.txt
Lancer MySQL séparément (par exemple via Docker), configurer MYSQL_HOST dans les variables d’environnement, puis lancer Flask :

bash
Copier le code
cd webapp
python app.py
Remarque : l’exécution hors Docker peut nécessiter des ajustements de chemins (SCRAPERS_PATH) et l’installation de dépendances système (Playwright, etc.).

---

## 9) Licence et crédits
Auteurs : Irina LEYOU, Maeva SALONG, Hans TADIE

Contexte : projet réalisé dans le cadre de la formation Big Data pour la Transformation Numérique.

Licence : MIT

---

## 10) Contact / support
Pour toute question : ton-email@exemple.com

Bugs / améliorations : ouvrir une issue sur GitHub.