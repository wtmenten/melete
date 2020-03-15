from django.contrib import admin
from django.db import models

import melete.core.models

model_members = melete.core.models.__all__

for name, c in model_members:
    if issubclass(c, models.Model):
        admin.site.register(c)
