from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Room


@login_required
def status_index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("name")

    # Render that in the index template
    return render(request, "pages/status.html", {
        "rooms": rooms,
    })
