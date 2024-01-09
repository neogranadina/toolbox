from django.contrib import admin
from .models import Documento, Lugar, Persona, Matrimonio, Bautismo, Entierro, Relationship

# Register your models here.

admin.site.register(Documento)
admin.site.register(Lugar)
admin.site.register(Persona)
admin.site.register(Relationship)
admin.site.register(Bautismo)
admin.site.register(Matrimonio)
admin.site.register(Entierro)