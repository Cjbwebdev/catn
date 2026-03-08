from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    has_full_access = models.BooleanField(default=False)
    free_views_used = models.IntegerField(default=0)


class Subscription(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)

    active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} subscription"