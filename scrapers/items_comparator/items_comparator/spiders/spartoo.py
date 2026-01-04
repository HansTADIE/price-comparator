import scrapy
import re

class SpartooSpider(scrapy.Spider):
    name = "spartoo"
    site_name = "spartoo"
    allowed_domains = ["spartoo.com"]

    def start_requests(self):
        # Page list / landing page for Nike Dunk models (user-provided)
        url = "https://www.spartoo.com/modele-10704715-Nike-Dunk.php#rst"
        yield scrapy.Request(
            url,
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    # Attendre que les images soient chargées
                    {"method": "wait_for_selector", "args": ["img[data-original]", {"timeout": 5000}]},
                ],
            }
        )

    def parse(self, response):
        # Chercher tous les conteneurs de produits
        # Spartoo utilise généralement des divs ou articles pour chaque produit
        product_containers = response.css("div.productlist_item, article.product, div.product-item")
        
        if not product_containers:
            # Fallback: chercher par lien de produit
            product_containers = response.xpath("//a[@class='displayLinkImg']/ancestor::div[1]")
        
        for container in product_containers:
            # Titre
            titre = container.css("span.productlist_name::text").get()
            if not titre:
                titre = container.css("span.productlist_name").xpath("normalize-space(.)").get()
            
            # Prix
            prix_brut = container.css("span.price::text, span.productlist_price::text").re_first(r"\d+,\d+\s*€")
            if not prix_brut:
                prix_brut = container.xpath(".//text()").re_first(r"\d+,\d+\s*€")
            
            prix = None
            if prix_brut:
                try:
                    prix = float(prix_brut.replace("€", "").replace(",", ".").strip())
                except:
                    prix = None
            
            # Image - essayer plusieurs attributs et sélecteurs
            image = None
            # 1. Essayer data-original en premier
            image = container.css("img::attr(data-original)").get()
            # 2. Si pas trouvé, essayer src
            if not image:
                image = container.css("img::attr(src)").get()
            # 3. Essayer avec un sélecteur plus spécifique
            if not image:
                image = container.xpath(".//img[@id[contains(., 'zoom_product_img')]]/@data-original").get()
            if not image:
                image = container.xpath(".//img[@id[contains(., 'zoom_product_img')]]/@src").get()
            
            # Lien
            lien = container.css("a.displayLinkImg::attr(href)").get()
            if not lien:
                lien = container.css("a::attr(href)").get()
            
            # Ne yielder que si on a au moins un titre
            if titre:
                yield {
                    "titre": titre.strip() if isinstance(titre, str) else titre,
                    "prix": prix,
                    "image": response.urljoin(image) if image else None,
                    "lien": response.urljoin(lien) if lien else None,
                    "site": self.site_name
                }

        # Pagination
        next_page = response.css("a.pagination__next::attr(href), a.next::attr(href), a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page, 
                callback=self.parse, 
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        {"method": "wait_for_selector", "args": ["img[data-original]", {"timeout": 5000}]},
                    ]
                }
            )