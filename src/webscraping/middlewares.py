from random import randint
from urllib.parse import urlencode

import requests


class ScrapeOpsFakeBrowserHeadersMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get("SCRAPEOPS_API_KEY")
        self.scrapeops_endpoint = settings.get(
            "SCRAPEOPS_FAKE_HEADERS_ENDPOINT",
        )
        self.scrapeops_fake_headers_active = settings.get(
            "SCRAPEOPS_FAKE_HEADERS_ENABLED"
        )
        self.scrapeops_num_results = settings.get("SCRAPEOPS_NUM_RESULTS")
        self.headers_list = []
        self._get_headers_list()

    def _get_headers_list(self):
        payload = {"api_key": self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload["num_results"] = self.scrapeops_num_results
        response = requests.get(
            self.scrapeops_endpoint, params=urlencode(payload)
        )
        json_response = response.json()
        self.headers_list = json_response.get("result", [])

    def _get_random_header(self):
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]

    def process_request(self, request, spider):
        random_header = self._get_random_header()

        """
        Mudar:
        accept-Language: en-GB,en-US;q=0.9,en;q=0.8

        """
        for key, val in random_header.items():
            request.headers[key] = val

        request.header["accept-language"] = "pt-BR,pt;q=0.9,en;q=0.8"


class ScrapeOpsProxyMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get("SCRAPEOPS_API_KEY")
        self.scrapeops_endpoint = "https://proxy.scrapeops.io/v1/?"
        self.scrapeops_proxy_active = settings.get("SCRAPEOPS_PROXY_ENABLED")
        self.proxy_country = settings.get("SCRAPEOPS_PROXY_SETTINGS")["country"]

    @staticmethod
    def _replace_response_url(response):
        real_url = response.headers.get("Sops-Final-Url", def_val=response.url)
        return response.replace(url=real_url.decode(response.headers.encoding))

    def _get_scrapeops_url(self, request):
        payload = {
            "api_key": self.scrapeops_api_key,
            "url": request.url,
            "country": self.proxy_country,
        }
        proxy_url = self.scrapeops_endpoint + urlencode(payload)
        return proxy_url

    def _scrapeops_proxy_enabled(self):
        if (
            self.scrapeops_api_key is None
            or self.scrapeops_api_key == ""
            or self.scrapeops_proxy_active is False
        ):
            return False
        return True

    def process_request(self, request, spider):
        if (
            self._scrapeops_proxy_enabled is False
            or self.scrapeops_endpoint in request.url
        ):
            return None

        scrapeops_url = self._get_scrapeops_url(request)
        new_request = request.replace(
            cls=request, url=scrapeops_url, meta=request.meta
        )
        return new_request

    def process_response(self, request, response, spider):
        new_response = self._replace_response_url(response)
        return new_response
