import stripe
from django.conf import settings
from accounts.models import User, Subscription
from django.http import HttpResponse


def stripe_webhook(request):

    payload = request.body
    sig = request.META["HTTP_STRIPE_SIGNATURE"]

    event = stripe.Webhook.construct_event(
        payload,
        sig,
        settings.STRIPE_WEBHOOK_SECRET
    )

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        email = session["customer_email"]

        user = User.objects.get(email=email)

        user.has_full_access = True
        user.save()

    return HttpResponse(status=200)