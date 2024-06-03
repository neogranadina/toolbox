from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

# resources

from .resources import (ArchivoResource, SituacionLugarResource, TipoInstitucionResource, DocumentoResource, LugarResource,
                        PersonaEsclavizadaResource, PersonaNoEsclavizadaResource, ActividadesResource,
                        HispanizacionResource)

# Register your models here.
from .models import Lugar, PersonaRolEvento
from .models import Archivo, Documento
from .models import Calidades, Actividades, Hispanizaciones, Etonimos
from .models import SituacionLugar, TipoDocumental, TipoLugar, TiposInstitucion
from .models import PersonaEsclavizada, PersonaNoEsclavizada, Corporacion
from .models import PersonaRelaciones, PersonaLugarRel, RolEvento, Relationship

class DocumentoResourceAdmin(ImportExportModelAdmin):
    resource_class = DocumentoResource

class LugarResourceAdmin(ImportExportModelAdmin):
    resource_class = LugarResource

class SituacionLugarAdmin(ImportExportModelAdmin):
    resource_class = SituacionLugarResource
    
class TipoInstitucionAdmin(ImportExportModelAdmin):
    resource_class = TipoInstitucionResource
    
class PersonaEsclavizadaAdmin(ImportExportModelAdmin):
    resource_class = PersonaEsclavizadaResource
    
class PersonaNoEsclavizadaAdmin(ImportExportModelAdmin):
    resource_class = PersonaNoEsclavizadaResource
    
class ActividadesAdmin(ImportExportModelAdmin):
    resource_class = ActividadesResource
    
class HispanizacionesAdmin(ImportExportModelAdmin):
    resource_class = HispanizacionResource
    
class ArchivoAdmin(ImportExportModelAdmin):
    resource_class = ArchivoResource

admin.site.register(Archivo, ArchivoAdmin)
admin.site.register(Calidades, ImportExportModelAdmin)
admin.site.register(Documento, DocumentoResourceAdmin)
admin.site.register(Actividades, ActividadesAdmin)
admin.site.register(Etonimos, ImportExportModelAdmin)
admin.site.register(Hispanizaciones, HispanizacionesAdmin)
admin.site.register(Lugar, LugarResourceAdmin)
admin.site.register(PersonaEsclavizada, PersonaEsclavizadaAdmin)
admin.site.register(PersonaNoEsclavizada, PersonaNoEsclavizadaAdmin)
admin.site.register(PersonaRelaciones, ImportExportModelAdmin)
admin.site.register(PersonaLugarRel, ImportExportModelAdmin)
admin.site.register(SituacionLugar, SituacionLugarAdmin)
admin.site.register(TipoDocumental, ImportExportModelAdmin)
admin.site.register(TipoLugar, ImportExportModelAdmin)
admin.site.register(RolEvento, ImportExportModelAdmin)
admin.site.register(TiposInstitucion, TipoInstitucionAdmin)
admin.site.register(Corporacion, ImportExportModelAdmin)
admin.site.register(PersonaRolEvento, ImportExportModelAdmin)
admin.site.register(Relationship, ImportExportModelAdmin)
