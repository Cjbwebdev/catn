from django.core.management.base import BaseCommand
from scraping.scrapers.ebay import EbayScraper
from scraping.services import save_listings
from listings.models import SourceSite


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        scrapers = [
            EbayScraper(),
        ]

        for scraper in scrapers:

            source, _ = SourceSite.objects.get_or_create(
                name=scraper.source_name
            )

            listings = scraper.run()

            save_listings(source, listings)