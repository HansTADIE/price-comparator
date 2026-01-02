import scrapy
import re
from scrapy_playwright.page import PageMethod

class ZalandoSpider(scrapy.Spider):
    name = "zalando"
    site_name = "zalando"
    allowed_domains = ["zalando.fr"]

    def start_requests(self):
        url = "https://www.zalando.fr/enfant/?q=Dunk+low"
        yield scrapy.Request(
            url,
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    # On attend explicitement qu'un article soit là, rien d'autre
                    PageMethod("wait_for_selector", "article", timeout=30000),
                ],
                # AJOUT CRUCIAL : on n'attend pas le chargement complet (load)
                "playwright_context_kwargs": {
                    "ignore_https_errors": True,
                },
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
                "lien": response.urljoin(lien),
                "site": self.site_name
            }
