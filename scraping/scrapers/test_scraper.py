class TestScraper:

    source_name = "TestData"

    def run(self):

        listings = []

        for i in range(20):

            listings.append({
                "external_id": f"test-{i}",
                "title": f"BMW 320D Cat N Vehicle {i}",
                "description": "Test listing for catn.site",
                "price": "£3500",
                "location": "London",
                "listing_url": "https://example.com",
                "image_urls": [
                    "https://upload.wikimedia.org/wikipedia/commons/6/6e/BMW_320d.jpg"
                ],
            })

        print("[Test] Created 20 vehicles")

        return listings