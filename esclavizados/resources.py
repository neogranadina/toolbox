from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import (Actividades, Archivo, Hispanizaciones, Lugar, PersonaEsclavizada, PersonaNoEsclavizada, SituacionLugar, TiposInstitucion, Documento)

class ArchivoResource(resources.ModelResource):
    archivo_id = Field(attribute='archivo_id', column_name='archivo_id', saves_null_values=False)
    
    class Meta:
        model = Archivo
        import_id_fields = ['archivo_id']
        fields = ('archivo_id', 'archivo_idno', 'nombre', 'nombre_abreviado', 'ubicacion_archivo', 
                  'created_at', 'updated_at')
        skip_unchanged = True
        report_skipped = False

class DocumentoResource(resources.ModelResource):
    documento_id = Field(attribute='documento_id', column_name='documento_id', saves_null_values=False)
    
    class Meta:
        model = Documento
        import_id_fields = ['documento_id']
        fields = ('documento_id', 'documento_idno', 'archivo', 'fondo', 'subfondo', 'serie', 'subserie', 'tipo_udc', 'unidad_documental_compuesta', 'tipo_documento', 'sigla_documento', 'titulo', 'descripcion', 'deteriorado', 'fecha_inicial', 'fecha_inicial_aproximada', 'fecha_final', 'fecha_final_aproximada', 'lugar_de_produccion', 'folio_inicial', 'folio_final', 'evento_valor_sp', 'evento_forma_de_pago', 'evento_total', 'notas', 'created_at', 'updated_at')
        skip_unchanged = True
        report_skipped = False

class LugarResource(resources.ModelResource):
    lugar_id = Field(attribute='lugar_id', column_name='lugar_id', saves_null_values=False)
    
    class Meta:
        model = Lugar
        import_id_fields = ['lugar_id']
        fields = (
            'lugar_id', 'nombre_lugar', 'otros_nombres', 'es_parte_de', 'lat', 'lon', 'tipo'
        )
        skip_unchanged = True
        report_skipped = False

class SituacionLugarResource(resources.ModelResource):
    situacion_id = Field(attribute='situacion_id', column_name='situacion_id', saves_null_values=False)
    situacion = Field(attribute='situacion', column_name='situacion')
    descripcion = Field(attribute='descripcion', column_name='descripcion')

    class Meta:
        model = SituacionLugar
        import_id_fields = ['situacion_id'] 
        fields = ('situacion_id', 'situacion', 'descripcion') 
        skip_unchanged = True
        report_skipped = False
        
class TipoInstitucionResource(resources.ModelResource):
    tipo_id = Field(attribute='tipo_id', column_name='tipo_id', saves_null_values=False)
    tipo = Field(attribute='tipo', column_name='tipo')
    descripcion = Field(attribute='descripcion', column_name='descripcion')
    
    class Meta:
        model = TiposInstitucion
        import_id_fields = ['tipo_id']
        fields = ('tipo_id', 'tipo', 'descripcion')
        skip_unchanged = True
        report_skipped = False
        

class PersonaEsclavizadaResource(resources.ModelResource):
    persona_id =  Field(attribute='persona_id', column_name='persona_id', saves_null_values=False)
    
    class Meta:
        model = PersonaEsclavizada
        import_id_fields = ['persona_id']
        fields = ('persona_id', 'persona_idno', 'documentos', 'nombres', 'apellidos', 'nombre_normalizado', 
                  'entidades_asociadas', 'calidades', 'fecha_nacimiento', 'fecha_nacimiento_factual', 
                  'lugar_nacimiento', 'fecha_defuncion', 'fecha_defuncion_factual', 'lugar_defuncion', 'sexo',
                  'ocupacion', 'ocupacion_categoria', 'notas', 'created_at', 'updated_at', 'edad', 'unidad_edad', 
                  'altura', 'cabello', 'ojos', 'hispanizacion', 'etnonimos', 'procedencia', 
                  'procedencia_adicional', 'marcas_corporales', 'conducta', 'salud', 'descriptor')
        skip_unchanged = True
        report_skipped = False
        
class PersonaNoEsclavizadaResource(resources.ModelResource):
    persona_id = Field(attribute='persona_id', column_name='persona_id', saves_null_values=False)
    
    class Meta:
        model = PersonaNoEsclavizada
        import_id_fields = ['persona_id']
        fields = ('persona_id', 'persona_idno', 'documentos', 'nombres', 'apellidos', 'nombre_normalizado', 
                  'entidades_asociadas', 'calidades', 'fecha_nacimiento', 'fecha_nacimiento_factual', 
                  'lugar_nacimiento', 'fecha_defuncion', 'fecha_defuncion_factual', 'lugar_defuncion', 
                  'sexo', 'ocupacion', 'ocupacion_categoria', 'notas', 'created_at', 'updated_at', 
                  'entidad_asociada', 'honorifico')
        skip_unchanged = True
        report_skipped = False
        

class ActividadesResource(resources.ModelResource):
    actividad_id = Field(attribute='actividad_id', column_name='actividad_id', saves_null_values=False)
    
    class Meta:
        model =  Actividades
        import_id_fields = ['actividad_id']
        fields = ('actividad_id', 'actividad', 'descripcion')
        skip_unchanged = True
        report_skipped = False
        
class HispanizacionResource(resources.ModelResource):
    hispanizacion_id = Field(attribute='hispanizacion_id', column_name='hispanizacion_id', saves_null_values=False)
    
    class Meta:
        model = Hispanizaciones
        import_id_fields = ['hispanizacion_id']
        fields = ('hispanizacion_id', 'hispanizacion', 'descripcion')
        skip_unchanged = True
        report_skipped = False