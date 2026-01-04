# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
"""
from itemadapter import ItemAdapter


class ItemsComparatorPipeline:
    def process_item(self, item, spider):
        return item
"""
import os
import mysql.connector
from mysql.connector import Error

class MySQLPipeline:
    def __init__(self):
        # Utiliser les variables d'environnement définies dans docker-compose.yml
        self.host = os.getenv('MYSQL_HOST', 'db')
        self.user = os.getenv('MYSQL_USER', 'user')
        self.password = os.getenv('MYSQL_PASSWORD', 'password')
        self.database = os.getenv('MYSQL_DATABASE', 'price_comparator')
        self.port = int(os.getenv('MYSQL_PORT', 3306))

    def open_spider(self, spider):
        try:
            # Connexion au serveur MySQL
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                autocommit=True
            )
            self.cursor = self.conn.cursor()
            spider.logger.info(f"Connecté à MySQL {self.host}:{self.port}")

            # Créer DB si besoin
            self.cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{self.database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
            self.cursor.execute(f"USE `{self.database}`;")

            # Créer table si besoin
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titre VARCHAR(255),
                prix DECIMAL(10,2),
                image VARCHAR(500),
                lien VARCHAR(500),
                site VARCHAR(100),
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY ux_lien (lien(255))
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            self.cursor.execute(create_table_sql)
            spider.logger.info(f"Base et table prêtes: {self.database}.products")

        except Error as e:
            spider.logger.error(f"Erreur connexion/initialisation MySQL: {e}")
            raise

    def close_spider(self, spider):
        try:
            if getattr(self, 'cursor', None):
                self.cursor.close()
            if getattr(self, 'conn', None) and self.conn.is_connected():
                self.conn.close()
            spider.logger.info("Connexion MySQL fermée")
        except Exception as e:
            spider.logger.warning(f"Erreur fermeture MySQL: {e}")

    def process_item(self, item, spider):
        try:
            sql = """
                INSERT INTO products (titre, prix, image, lien, site)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    titre = VALUES(titre),
                    prix = VALUES(prix),
                    image = VALUES(image),
                    site = VALUES(site),
                    scraped_at = CURRENT_TIMESTAMP
            """
            values = (
                item.get('titre'),
                item.get('prix'),
                item.get('image'),
                item.get('lien'),
                item.get('site')
            )
            self.cursor.execute(sql, values)

        except Error as e:
            spider.logger.error("Erreur insertion MySQL: %s -- item: %s", e, dict(item))

        return item


    

