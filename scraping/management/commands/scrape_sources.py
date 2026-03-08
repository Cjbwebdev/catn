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

            print(f"Running scraper: {scraper.source_name}")

            source, _ = SourceSite.objects.get_or_create(
                name=scraper.source_name
            )

            listings = scraper.run()

            print(f"Listings scraped: {len(listings)}")

            save_listings(source, listings)

            print("Listings saved.")