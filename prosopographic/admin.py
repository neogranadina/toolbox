from django.contrib import admin
from .models import (Documento, Lugar, Persona, Matrimonio, Bautismo, Entierro, Relationship, Archivo)
from import_export.admin import ImportExportModelAdmin
from toolboximport.resources import (ArchivoResource, DocumentoResource, LugarResource,
                                     PersonaResource, EntierroResource, BautismoResource)

# Register your models here.

class ArchivoAdmin(ImportExportModelAdmin):
    resource_class = ArchivoResource

class DocumentoAdmin(ImportExportModelAdmin):
    resource_class = DocumentoResource
    
class LugarAdmin(ImportExportModelAdmin):
    resource_class = LugarResource
    
class PersonaAdmin(ImportExportModelAdmin):
    resource_class = PersonaResource
    
class BautismoAdmin(ImportExportModelAdmin):
    resource_class = BautismoResource
    
class EntierroAdmin(ImportExportModelAdmin):
    resource_class = EntierroResource

admin.site.register(Archivo, ArchivoAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Lugar, LugarAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Relationship, ImportExportModelAdmin)
admin.site.register(Bautismo, BautismoAdmin)
admin.site.register(Matrimonio, ImportExportModelAdmin)
admin.site.register(Entierro, EntierroAdmin)