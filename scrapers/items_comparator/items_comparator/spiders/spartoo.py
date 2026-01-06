import scrapy
import re

class SpartooSpider(scrapy.Spider):
    name = "spartoo"
    allowed_domains = ["spartoo.com"]

    def start_requests(self):
        url = "https://www.spartoo.com/modele-10704715-Nike-Dunk.php#rst"
        yield scrapy.Request(
            url,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    {"method": "wait_for_selector", "args": ["div.productlist_item", {"timeout": 10000}]},
                ],
            }
        )

    def parse(self, response):
        # On cible directement les conteneurs principaux utilisés par Spartoo
        products = response.css("div.productlist_item")

        for product in products:
            # 1. Extraction du Titre (plus simple)
            titre = product.css("span.productlist_name::text").get()
            if not titre:
                continue # Si pas de titre, on passe au suivant (inutile de comparer)

            # 2. Extraction et Nettoyage du Prix
            # On cherche le prix actuel (parfois en rouge si promo, parfois normal)
            prix_text = product.css("span.productlist_price::text, span.price::text").get()
            prix_propre = self.clean_price(prix_text)

            # 3. Extraction de l'Image et du Lien
            # On prend 'data-original' (lazy load) sinon 'src'
            image = product.css("img::attr(data-original)").get() or product.css("img::attr(src)").get()
            lien_relatif = product.css("a::attr(href)").get()

            yield {
                "site": "Spartoo",
                "titre": titre.strip(),
                "prix": prix_propre, # C'est maintenant un chiffre, prêt à être comparé
                "devise": "EUR",
                "image": response.urljoin(image),
                "lien": response.urljoin(lien_relatif),
            }

        # Pagination (Code conservé mais simplifié)
        next_page = response.css("a.pagination__next::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page, 
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        {"method": "wait_for_selector", "args": ["div.productlist_item", {"timeout": 10000}]},
                    ]
                }
            )

    def clean_price(self, price_str):
        """Transforme '119,99 €' en 119.99 (float)"""
        if not price_str:
            return None
        # On ne garde que les chiffres et la virgule/point
        clean_str = re.sub(r'[^\d,.]', '', price_str).replace(',', '.')
        try:
            return float(clean_str)
        except ValueError:
            return None