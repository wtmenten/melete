from django.urls import path

from melete.core.views import (
    ticker_detail_view,
    ticker_redirect_view,
    ticker_update_view,
)

app_name = "core"
urlpatterns = [
    path("~redirect/", view=ticker_redirect_view, name="redirect"),
    path("~update/", view=ticker_update_view, name="update"),
    path("<str:symbol>/", view=ticker_detail_view, name="detail"),
]
