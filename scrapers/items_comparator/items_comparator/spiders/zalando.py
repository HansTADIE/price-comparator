import scrapy
import re

class ZalandoSpider(scrapy.Spider):
    name = "zalando"
    allowed_domains = ["zalando.fr"]

    def start_requests(self):
        url = "https://www.zalando.fr/enfant/?q=Dunk+low"
        yield scrapy.Request(
            url,
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    # Attendre que les articles soient chargés
                    {"name": "wait_for_selector", "args": ["article"]}
                ],
            }
        )

    def parse(self, response):
        self.logger.info("Page chargée : %s", response.url)

        products = response.css("article")
        self.logger.info("Articles trouvés : %d", len(products))

        for product in products:
            titre = product.css("h3 span:last-child::text").get()
            prix_brut = product.css("span::text").re_first(r"\d+,\d+\s*€")
            image = product.css("img::attr(src)").get()
            lien = product.css("a::attr(href)").get()

            prix = None
            if prix_brut:
                prix = float(prix_brut.replace("€", "").replace(",", ".").strip())

            yield {
                "titre": titre,
                "prix": prix,
                "image": image,
                "lien": response.urljoin(lien)
            }
