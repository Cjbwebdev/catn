import stripe
from django.conf import settings
from django.shortcuts import redirect


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request):

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        line_items=[{
            "price": settings.STRIPE_PRICE_ID,
            "quantity": 1,
        }],

        mode="subscription",

        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",

        customer_email=request.user.email,
    )

    return redirect(session.url)