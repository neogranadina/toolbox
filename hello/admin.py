from django.contrib import admin
from .models import CaObject, CaEntityLabel

# Register your models here.

admin.site.register(CaObject)
admin.site.register(CaEntityLabel)