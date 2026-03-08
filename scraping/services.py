from listings.models import VehicleListing, SourceSite


def save_listings(source, scraped_listings):

    for data in scraped_listings:

        listing, created = VehicleListing.objects.update_or_create(

            source=source,
            external_id=data["external_id"],

            defaults={
                "title": data["title"],
                "description": data["description"],
                "price": data["price"],
                "location": data["location"],
                "listing_url": data["listing_url"],
                "image_urls": data["image_urls"],
                "status": "active",
            }
        )