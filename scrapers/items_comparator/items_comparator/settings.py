# Scrapy settings for items_comparator project

BOT_NAME = "items_comparator"

SPIDER_MODULES = ["items_comparator.spiders"]
NEWSPIDER_MODULE = "items_comparator.spiders"

ADDONS = {}

# =========================
# USER-AGENT & ROBOTS
# =========================
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
)
ROBOTSTXT_OBEY = False

# =========================
# CONCURRENCY & DELAY
# =========================
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1.5

# =========================
# COOKIES
# =========================
COOKIES_ENABLED = True

# =========================
# HEADERS
# =========================
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# =========================
# AUTO THROTTLE
# =========================
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# =========================
# LOGS
# =========================
LOG_LEVEL = "INFO"

# =========================
# EXPORT
# =========================
FEED_EXPORT_ENCODING = "utf-8"

# =========================
# RETRIES (ANTI-BLOCAGE)
# =========================
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [403, 429, 500, 502, 503, 504]

# =========================
# SCRAPY + PLAYWRIGHT
# =========================
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 120000  # 30 secondes

# MySQL (XAMPP local)
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''   # ou ton mot de passe si tu l'as défini
MYSQL_DATABASE = 'price_comparator'

# Pipelines Scrapy
ITEM_PIPELINES = {
    "items_comparator.pipelines.MySQLPipeline": 300,
}

