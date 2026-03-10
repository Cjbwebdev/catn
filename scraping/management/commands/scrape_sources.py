from django.core.management.base import BaseCommand
from scraping.scrapers.gumtree_playwright import GumtreeScraper
from scraping.services import save_listings
from listings.models import SourceSite


class Command(BaseCommand):

    help = "Run scrapers"

    def handle(self, *args, **options):

        scrapers = [
            GumtreeScraper(),
        ]

        total = 0

        for scraper in scrapers:

            print(f"\nRunning scraper: {scraper.source_name}")

            source,_ = SourceSite.objects.get_or_create(
                name=scraper.source_name
            )

            listings = scraper.run(headless=False)

            print("Listings scraped:", len(listings))

            save_listings(source,listings)

            total += len(listings)

        print("\nTotal listings:", total)