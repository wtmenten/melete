import inflect as inflect
import stringcase
from django.conf import settings
from django.db.models import Model
from polymorphic.models import PolymorphicModel
from rest_framework.routers import DefaultRouter, SimpleRouter

import melete.core.models
from melete.core.api.views import ModelViewSetFactory
from melete.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
p = inflect.engine()
for name, c in melete.core.models.__all__:
    if issubclass(c, Model):
        kwargs = {}
        if getattr(c, 'lookup_field', False):
            kwargs['lookup_field'] = c.lookup_field
        if issubclass(c, PolymorphicModel):
            kwargs['lookup_field'] = kwargs.get('lookup_field', c._meta.pk.name)
        router.register(
            p.plural(stringcase.snakecase(stringcase.camelcase(name))),
            ModelViewSetFactory.get_view_set(c, **kwargs)
        )

# router.register("tickers", ModelViewSetFactory.get_view_set(Ticker, lookup_field='symbol'))
# router.register("aliases", ModelViewSetFactory.get_view_set(Alias, lookup_field='alias'))


app_name = "api"
urlpatterns = router.urls
