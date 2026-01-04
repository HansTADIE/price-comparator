from flask import Flask, render_template, jsonify
import mysql.connector
import subprocess
import os

app = Flask(__name__)

# Configuration de la base de données
DB_CONFIG = {
    'host': 'db',
    'port': 3306,
    'user': 'user',
    'password': 'password',
    'database': 'price_comparator'
}

# Mapping des articles : {article_num: {site: id}}
ARTICLES_MAPPING = {
    1: {'zalando': 1, 'courir': 30, 'spartoo': 72},
    2: {'zalando': 13, 'courir': 45, 'spartoo': 98},
    3: {'zalando': 21, 'courir': 55, 'spartoo': 68},
    4: {'zalando': 4, 'courir': 50, 'spartoo': 89},
    5: {'zalando': 24, 'courir': 51, 'spartoo': 187},
    6: {'zalando': 18, 'courir': 34, 'spartoo': 168},
    7: {'zalando': 10, 'courir': 35, 'spartoo': 130},
    8: {'zalando': 5, 'courir': 41, 'spartoo': 68},
    9: {'zalando': 9, 'courir': 30, 'spartoo': 153},
    10: {'zalando': 14, 'courir': 47, 'spartoo': 68},
    11: {'zalando': 24, 'courir': 51, 'spartoo': 90},
    12: {'zalando': 6, 'courir': 59, 'spartoo': 73},
    13: {'zalando': 11, 'courir': 28, 'spartoo': 66},
    14: {'zalando': 2, 'courir': 59, 'spartoo': 89},
    15: {'zalando': 3, 'courir': 35, 'spartoo': 66},
    16: {'zalando': 4, 'courir': 56, 'spartoo': 72},
    17: {'zalando': 8, 'courir': 25, 'spartoo': 68},
    18: {'zalando': 12, 'courir': 45, 'spartoo': 118},
    19: {'zalando': 16, 'courir': 35, 'spartoo': 66},
    20: {'zalando': 17, 'courir': 45, 'spartoo': 190}
}

def get_db_connection():
    """Créer une connexion à la base de données"""
    return mysql.connector.connect(**DB_CONFIG)

def get_product_by_id(product_id):
    """Récupérer un produit par son ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        return product
    except Exception as e:
        print(f"Erreur lors de la récupération du produit {product_id}: {e}")
        return None

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    """Lancer le scraping des trois sites dans l'ordre"""
    try:
        # Chemin vers le dossier des scrapers
        scrapers_path = os.environ.get(
            "SCRAPERS_PATH",
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),  # webapp/
                    os.pardir,                   # price-comparator/
                    "scrapers",
                    "items_comparator"
                )
            )
        )

        # DEBUG: affiche pour vérifier que le chemin est correct (retire ces prints en prod)
        print("SCRAPERS_PATH resolved to:", scrapers_path)
        print("scrapy.cfg exists:", os.path.isfile(os.path.join(scrapers_path, "scrapy.cfg")))
        
        # Ordre de scraping
        spiders = ['zalando', 'courir', 'spartoo']
        results = []
        
        for spider in spiders:
            result = subprocess.run(
                ['scrapy', 'crawl', spider],
                cwd=scrapers_path,
                capture_output=True,
                text=True
            )
            
            status = 'success' if result.returncode == 0 else 'error'
            results.append({
                'spider': spider,
                'status': status,
                'message': f"{spider.capitalize()} scraping completed" if status == 'success' else result.stderr
            })
        
        return jsonify({'status': 'success', 'results': results})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/products')
def get_products():
    """Récupérer les produits à afficher selon le mapping"""
    try:
        products_data = []
        
        for article_num in range(1, 21):
            article_ids = ARTICLES_MAPPING[article_num]
            
            # Récupérer les produits pour chaque site
            zalando_product = get_product_by_id(article_ids['zalando'])
            courir_product = get_product_by_id(article_ids['courir'])
            spartoo_product = get_product_by_id(article_ids['spartoo'])
            
            # Utiliser le titre de Spartoo
            titre = spartoo_product['titre'] if spartoo_product else f"Article {article_num}"
            
            products_data.append({
                'article_num': article_num,
                'titre': titre,
                'zalando': {
                    'prix': float(zalando_product['prix']) if zalando_product and zalando_product['prix'] else None,
                    'image': zalando_product['image'] if zalando_product else None,
                    'lien': zalando_product['lien'] if zalando_product else None
                },
                'courir': {
                    'prix': float(courir_product['prix']) if courir_product and courir_product['prix'] else None,
                    'image': courir_product['image'] if courir_product else None,
                    'lien': courir_product['lien'] if courir_product else None
                },
                'spartoo': {
                    'prix': float(spartoo_product['prix']) if spartoo_product and spartoo_product['prix'] else None,
                    'image': spartoo_product['image'] if spartoo_product else None,
                    'lien': spartoo_product['lien'] if spartoo_product else None
                }
            })
        
        return jsonify({'status': 'success', 'products': products_data})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)