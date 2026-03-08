from django.shortcuts import render, get_object_or_404, redirect
from .models import VehicleListing, SourceSite


def listing_list(request):

    listings = VehicleListing.objects.filter(status="active")

    source = request.GET.get("source")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    q = request.GET.get("q")

    if source:
        listings = listings.filter(source__name=source)

    if min_price:
        listings = listings.filter(price__gte=min_price)

    if max_price:
        listings = listings.filter(price__lte=max_price)

    if q:
        listings = listings.filter(title__icontains=q)

    listings = listings.select_related("source").order_by("-first_seen")

    return render(request, "listings/list.html", {"listings": listings})

def listing_detail(request, pk):

    listing = get_object_or_404(VehicleListing, pk=pk)

    if request.user.is_authenticated:

        if not request.user.has_full_access:
            if request.user.free_views_used >= 10:
                return redirect("billing:paywall")

            request.user.free_views_used += 1
            request.user.save()

    else:

        views = request.session.get("free_views_used", 0)

        if views >= 10:
            return redirect("accounts:signup")

        request.session["free_views_used"] = views + 1

    return render(request, "listings/detail.html", {"listing": listing})