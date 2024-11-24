import os

from modulos.uteis import carregar_env, meu_tempo

carregar_env.carregar_env()

BOT_NAME = "webscraping"

SPIDER_MODULES = ["webscraping.spiders"]
NEWSPIDER_MODULE = "webscraping.spiders"

CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = False
REDIRECT_ENABLED = False
COOKIES_ENABLED = False

SCRAPEOPS_API_KEY = os.getenv("SCRAPEOPS_API_KEY")

# HTTP Headers
SCRAPEOPS_FAKE_HEADERS_ENABLED = True
SCRAPEOPS_FAKE_HEADERS_ENDPOINT = (
    "http://headers.scrapeops.io/v1/browser-headers?"
)
SCRAPEOPS_FAKE_HEADERS_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 100

# Proxy
SCRAPEOPS_PROXY_ENABLED = True
SCRAPEOPS_PROXY_SETTINGS = {"country": "br"}

DOWNLOADER_MIDDLEWARES = {
    "webscraping.middlewares.ScrapeOpsFakeBrowserHeadersMiddleware": 400,
    "webscraping.middlewares.ScrapeOpsProxyMiddleware": 725,
    "scrapeops_scrapy.middleware.retry.RetryMiddleware": 550,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
}

DOWNLOAD_TIMEOUT = 121

# Monitoring
EXTENSIONS = {
    "scrapeops_scrapy.extension.ScrapeOpsMonitor": 500,
}

FEEDS = {
    f"../dados/nao_processados/tenis_corrida_{meu_tempo.data_agora_simplificada_com_underline()}.json": {
        "format": "json",
        "overwrite": True,
        "encoding": "utf8",
    },
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
