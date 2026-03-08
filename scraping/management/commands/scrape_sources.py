from django.core.management.base import BaseCommand
from scraping.scrapers.ebay import EbayScraper
from scraping.scrapers.gumtree import GumtreeScraper
from scraping.scrapers.copart import CopartScraper
from scraping.services import save_listings
from listings.models import SourceSite

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        scrapers = [
            EbayScraper(),
            GumtreeScraper(),
            CopartScraper(),
        ]

        for scraper in scrapers:
            print(f"\nRunning scraper: {scraper.source_name}")

            source, _ = SourceSite.objects.get_or_create(
                name=scraper.source_name
            )

            listings = scraper.run()
            print(f"Listings scraped: {len(listings)}")

            save_listings(source, listings)
            print("Listings saved.")
        print("\nScraping completed.")