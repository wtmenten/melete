import typing

from django.db import models
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import ModelSerializerFactory


class ModelViewSetFactory:
    @staticmethod
    def get_view_set(m: typing.Type[models.Model], **kwargs):
        class MeleteViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
            serializer_class = ModelSerializerFactory.get_serializer(m)
            queryset = m.objects.all()
            lookup_field = kwargs.get('lookup_field', m._meta.pk.column)

        MeleteViewSet.__name__ = "%sViewSet" % m.__name__
        return MeleteViewSet
