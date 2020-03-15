from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from melete.core.models.entities import Ticker


class TickerDetailView(LoginRequiredMixin, DetailView):

    model = Ticker
    slug_field = "symbol"
    slug_url_kwarg = "symbol"


ticker_detail_view = TickerDetailView.as_view()


class TickerUpdateView(LoginRequiredMixin, UpdateView):

    model = Ticker
    fields = ["symbol"]

    def get_success_url(self):
        return reverse("tickers:detail", kwargs={"symbol": self.request.ticker.symbol})

    def get_object(self):
        return Ticker.objects.get(username=self.request.ticker.symbol)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


ticker_update_view = TickerUpdateView.as_view()


class TickerRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("tickers:detail", kwargs={"symbol": self.request.user.symbol})


ticker_redirect_view = TickerRedirectView.as_view()
