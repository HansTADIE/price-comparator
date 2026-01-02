from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="db", # Nom du service dans docker-compose
        user="root",
        password="root",
        database="price_comparator"
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # On récupère les produits triés par titre puis par prix
    cursor.execute("SELECT * FROM products ORDER BY titre, prix ASC")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)