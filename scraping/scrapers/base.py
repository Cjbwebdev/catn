import requests


class BaseScraper:

    source_name = None
    start_url = None

    def fetch(self):
        r = requests.get(self.start_url)
        r.raise_for_status()
        return r.text

    def parse(self, html):
        raise NotImplementedError

    def run(self):

        html = self.fetch()
        listings = self.parse(html)

        return listings