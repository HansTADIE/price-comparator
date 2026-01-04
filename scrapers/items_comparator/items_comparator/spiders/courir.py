# price-comparator/scrapers/items_comparator/items_comparator/spiders/courir.py
import scrapy
import re

class CourirSpider(scrapy.Spider):
    name = "courir"
    site_name = "courir"
    allowed_domains = ["courir.com"]

    def start_requests(self):
        # URL de recherche fournie
        url = "https://www.courir.com/fr/search?q=DUNK+LOW+&lang=fr_FR"
        yield scrapy.Request(
            url,
            callback=self.parse,
            meta={
                "playwright": True,
                # On scroll pour charger les éléments lazy / paginés
                "playwright_page_methods": [
                    # Attendre que les produits soient chargés
                    {"method": "wait_for_selector", "args": ["a.product__link", {"timeout": 5000}]},
                    # Scroll down plusieurs fois pour forcer le chargement dynamique
                    {"method": "evaluate", "args": ["window.scrollTo(0, document.body.scrollHeight)"]},
                    {"method": "wait_for_timeout", "args": [1500]},
                    {"method": "evaluate", "args": ["window.scrollTo(0, document.body.scrollHeight)"]},
                    {"method": "wait_for_timeout", "args": [1500]},
                    {"method": "evaluate", "args": ["window.scrollTo(0, document.body.scrollHeight)"]},
                    {"method": "wait_for_timeout", "args": [2000]},
                ],
                "playwright_page_coroutines": []
            },
        )

    def parse(self, response):
        """
        Parcourt chaque produit contenu dans <a class="product__link js-product-link" ...>
        et extrait titre, prix, image et lien.
        """
        # Sélecteur principal : chaque produit est rendu dans un <a class="product__link ...">
        products = response.css("a.product__link")
        self.logger.info("Produits détectés sur la page: %d", len(products))

        for product in products:
            # Titre : <span class="product__name__product js-product-name_product">dunk low</span>
            titre = product.css("span.product__name__product::text").get()
            
            # Prix : <span data-update-key="defaultPrice"> 120,00 € </span>
            prix_brut = product.css('span[data-update-key="defaultPrice"]::text').get()
            
            # Images : PRIORITÉ À data-frz-src (image réelle) puis fallback vers src
            image = product.css("img::attr(data-frz-src)").get()
            if not image:
                image = product.css("img::attr(src)").get()
            
            # Filtrer les images placeholder base64
            if image and image.startswith("data:image"):
                self.logger.warning(f"Image placeholder base64 détectée pour {titre}, tentative alternative...")
                # Essayer d'autres attributs possibles
                image = product.css("img::attr(data-src)").get()
                if not image or image.startswith("data:image"):
                    image = None
            
            # Lien : <a class="product__link js-product-link" href="/fr/p/nike-dunk-low-1606573.html">
            lien = product.attrib.get("href") or product.css("::attr(href)").get()

            # Nettoyage du prix en float
            prix = None
            if prix_brut:
                # Exemple : " 120,00 € " -> 120.00
                s = prix_brut.strip()
                s = s.replace("€", "").replace("\u00A0", "").replace(" ", "")
                s = s.replace(",", ".")
                try:
                    prix = float(re.findall(r"[\d.]+", s)[0])
                except Exception:
                    prix = None

            # Ne yielder que si on a les données principales
            if titre:
                yield {
                    "titre": titre.strip() if isinstance(titre, str) else titre,
                    "prix": prix,
                    "image": response.urljoin(image) if image else None,
                    "lien": response.urljoin(lien) if lien else None,
                    "site": self.site_name
                }

        # Optionnel : suivre pagination si présente
        next_page = response.css("a.pagination__next::attr(href), a.next::attr(href), a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page, 
                callback=self.parse, 
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        {"method": "wait_for_selector", "args": ["a.product__link", {"timeout": 5000}]},
                        {"method": "evaluate", "args": ["window.scrollTo(0, document.body.scrollHeight)"]},
                        {"method": "wait_for_timeout", "args": [2000]},
                    ]
                }
            )