from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import (SituacionLugar, TiposInstitucion, Documento)

class DocumentoResource(resources.ModelResource):
    documento_id = Field(attribute='documento_id', column_name='documento_id', saves_null_values=False)
    
    class Meta:
        model = Documento
        import_id_fields = ['documento_id']
        fields = ('documento_id', 'documento_idno', 'archivo', 'fondo', 'subfondo', 'serie', 'subserie', 'tipo_udc', 'unidad_documental_compuesta', 'tipo_documento', 'sigla_documento', 'titulo', 'descripcion', 'deteriorado', 'fecha_inicial', 'fecha_inicial_aproximada', 'fecha_final', 'fecha_final_aproximada', 'lugar_de_produccion', 'folio_inicial', 'folio_final', 'evento_valor_sp', 'evento_forma_de_pago', 'evento_total', 'notas', 'created_at', 'updated_at')
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