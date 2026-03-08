from django.db import models


class SourceSite(models.Model):
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VehicleListing(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("expired", "Expired"),
    ]

    source = models.ForeignKey(
        SourceSite,
        on_delete=models.CASCADE,
        related_name="listings"
    )

    external_id = models.CharField(max_length=255)

    title = models.CharField(max_length=500)
    description = models.TextField()

    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    location = models.CharField(max_length=255, blank=True)

    listing_url = models.URLField()

    image_urls = models.JSONField(default=list)

    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("source", "external_id")
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return self.title