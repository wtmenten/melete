import typing

from django.db import models
from polymorphic.models import PolymorphicModel
from rest_framework import serializers

# from rest_polymorphic.serializers import PolymorphicSerializer


class ModelSerializerFactory:

    @staticmethod
    def get_serializer(m: typing.Type[models.Model], **kwargs):
        class MeleteSerializer(serializers.ModelSerializer):
            class Meta:
                model = m
                all_fields = '__all__'
                # exclude = ['polymorphic_ctype']
                if issubclass(m, PolymorphicModel):
                    # print([x.name for x in m._meta.fields])
                    # print([x.name for x in m._meta.many_to_many])
                    all_fields = [
                        x.name for x in m._meta.fields
                        if x.name != 'polymorphic_ctype' and not x.name.endswith('_ptr')
                    ]
                    all_fields += [x.name for x in m._meta.many_to_many]

                fields = kwargs.get('fields', all_fields)
                extra_kwargs = kwargs.get('extra_kwargs', {})

        MeleteSerializer.__name__ = "%sSerializer" % m.__name__
        return MeleteSerializer
