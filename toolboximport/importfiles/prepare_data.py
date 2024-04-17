import pandas as pd
import numpy as np
from unidecode import unidecode
import re
from datetime import datetime, timedelta


class Entierros:
    
    def __init__(self, df) -> None:
        self.df = df
        
    def prepare_places(self, df):
        
        # select columns with places information
        # 'Descriptor Geográfico 1', 'Descriptor Geográfico 2', 'Descriptor Geográfico 3', 'Descriptor Geográfico 4'
        
        concatenated_column = pd.concat([df['doctrina'],
                                         df['lugar_enterramiento'], 
                                         df['vecindad'],
                                 df['lugar_declaracion'], 
                                 df['Descriptor Geográfico 1'], 
                                 df['Descriptor Geográfico 2'], 
                                 df['Descriptor Geográfico 3'], 
                                 df['Descriptor Geográfico 4']], axis=0)
        
        new_df = pd.DataFrame(concatenated_column, columns=['nombre'])
        new_df.dropna(inplace=True, how='all')
        new_df['tipo'] = new_df['nombre'].apply(lambda x: x.split(',')[1].strip() if len(x.split(',')) > 1 else "")
        #new_df['nombre'] = new_df['nombre'].apply(lambda x: x.split(',')[0].strip())
        new_df['nombre'] = new_df['nombre'].replace('', np.nan)
        new_df = new_df.dropna(subset=['nombre'])
        new_df['nombre'] = new_df['nombre'].apply(lambda x: x.capitalize())
        new_df['nombre'] = new_df['nombre'].str.replace(r'[\/\[\]\.\(\)\"\"]', '', regex=True)

        new_df.drop_duplicates(subset=['nombre'], inplace=True)
        
        new_df.to_excel('toolboximport/importfiles/lugares.xlsx', index_label='id')
        new_df.to_csv('toolboximport/importfiles/lugares.csv', index_label='id', encoding='utf-8', index=False)

    def calculate_fecha_nacimiento(self, row):
        try:
            if pd.notnull(row['Edad']):
                edad = row['Edad'].lower()
                try:
                    edad_valor = int(list(filter(str.isdigit, edad))[0])
                except IndexError:
                    edad_valor = 0
                if 'año' in edad:
                    return datetime.strptime(row['fecha'], '%Y-%m-%d') - timedelta(days=edad_valor * 365)
                elif 'mes' in edad:
                    return datetime.strptime(row['fecha'], '%Y-%m-%d') - timedelta(weeks=edad_valor * 4)
                else:
                    return None
            else:
                return None
        except (ValueError, TypeError):
            return None

    def prepare_personas_entierros(self, df):
        # nombre, apellidos, nombre_completo, fecha_nacimiento, fecha_defuncion, lugar_nacimiento, vecindad, condicion
        
        df.rename(columns={
            'nombre_difunto': 'nombre',
            'apellido_difunto': 'apellidos'
        }, inplace=True)
        
        df['fecha_nacimiento'] = df.apply(self.calculate_fecha_nacimiento, axis=1)
        df['nombre_completo'] = df.apply(lambda x: f"{x['nombre']} {x['apellidos']}", axis=1)
        df['nombre_completo'] = df['nombre_completo'].apply(unidecode)
        df['vecindad'] = df['vecindad'].fillna(value='')
        df['vecindad'] = df['vecindad'].apply(lambda x: x.capitalize())
        df['vecindad'] = df['vecindad'].str.replace(r'[\/\[\]\.\(\)\"\"]', '', regex=True)
        
        df['nombre_completo'] = df.apply(lambda x: x.nombre_completo.replace('N N', f'N N {x.identificador}'), axis=1)
        
        save_difunto = df[['nombre', 'apellidos', 'nombre_completo', 'vecindad', 'condicion', 'fecha_nacimiento']].drop_duplicates()
        save_difunto.dropna(inplace=True, how='all')
        
        save_difunto.to_excel('toolboximport/importfiles/difuntos.xlsx', index_label='id')
        save_difunto.to_csv('toolboximport/importfiles/difuntos.csv', encoding='utf-8')


    def prepare_date(self, date_str):
        normalized_date = pd.NaT
        notes = date_str
        if pd.isnull(date_str):
            return normalized_date, ''
        elif isinstance(date_str, datetime):
            return date_str, ''
        elif isinstance(date_str, str):
            date_str = re.sub(r"[\[\]]", "", date_str)
        
        
        try:
            ensure_date = datetime.strptime(date_str, '%Y-%m-%d')
            return ensure_date, ''
        except ValueError:
            basepattern = re.compile(r"\d{4}-\d{2}-\d{2}")
            sept31 = re.compile(r"-09-31")
            justyear = re.compile(r"\d{4}-[A-Za-z]")
            justyearmonth = re.compile(r"\d{4}-\d{2}-[A-Za-z0-9\"][A-Za-z]")
            startswithstr = re.compile(r"^[A-Za-z]")
            if sept31.search(date_str):
                partial_date_match = re.search(r'\d{4}-\d{2}', date_str)
                if partial_date_match:
                    partial_date = partial_date_match.group()
                    normalized_date = datetime.strptime(partial_date, '%Y-%m')
                    return normalized_date, date_str
            elif justyearmonth.search(date_str):
                partial_date_match = re.search(r'\d{4}-\d{2}', date_str)
                if partial_date_match:
                    partial_date = partial_date_match.group()
                    normalized_date = datetime.strptime(partial_date, '%Y-%m')
                    return normalized_date, date_str
            elif justyear.search(date_str):
                partial_date_match = re.search(r'\d{4}', date_str)
                if partial_date_match:
                    partial_date = partial_date_match.group()
                    normalized_date = datetime.strptime(partial_date, '%Y')
                    return normalized_date, date_str
            elif startswithstr.match(date_str):
                find_pattern_match = re.search(basepattern, date_str)
                if find_pattern_match:
                    find_pattern = find_pattern_match.group()
                    normalized_date = datetime.strptime(find_pattern, '%Y-%m-%d')
                    return normalized_date, date_str
                else:
                    return '', date_str
            else:
                print(date_str)
                raise
        except:
            raise
        
        

    def prepare_personas_relacionadas(self, df):
        # 'Nombre del padre','Apellido del padre', 'Nombre de la madre', 'Apellido de la madre','Marido (añadir una + después del nombre si es difunto)','Esposa (añadir una + después del nombre si es difunta)'
        
        padres = pd.DataFrame()
        padres['nombre'] = df['nombre_padre']
        padres['apellidos'] = df['apellido_padre']
        padres['identificador'] = df['identificador']
        padres['nombre_completo'] = padres.apply(lambda x: f"{x['nombre']} {x['apellidos']}", axis=1)
        
        #padres['nombre_completo'] = padres.apply(lambda x: x.nombre_completo.replace('N N', f'N N {x.identificador}'), axis=1)
        
        
        madres = pd.DataFrame()
        madres['nombre'] = df['nombre_madre']
        madres['apellidos'] = df['apellido_madre']
        madres['identificador'] = df['identificador']
        madres['nombre_completo'] = madres.apply(lambda x: f"{x['nombre']} {x['apellidos']}", axis=1)
        
        #madres['nombre_completo'] = madres.apply(lambda x: x.nombre_completo.replace('N N', f'N N {x.identificador}'), axis=1)
        
        maridos = pd.DataFrame()
        maridos['nombre'] = df['marido'].apply(lambda x: x.split()[0] if isinstance(x, str) and len(x) > 1 else x)
        maridos['apellidos'] = df['marido'].apply(lambda x: ' '.join(x.split()[1:]) if isinstance(x, str) else x)
        maridos['identificador'] = df['identificador']
        
        maridos['nombre_completo'] = maridos.apply(lambda x: f"{x['nombre']} {x['apellidos']}", axis=1)
        #maridos['nombre_completo'] = maridos.apply(lambda x: x.nombre_completo.replace('N N', f'N N {x.identificador}'), axis=1)
        
        esposas = pd.DataFrame()
        esposas['nombre'] = df['esposa'].apply(lambda x: x.split()[0] if isinstance(x, str) and len(x) > 1 else x)
        esposas['apellidos'] = df['esposa'].apply(lambda x: ' '.join(x.split()[1:]) if isinstance(x, str) else x)
        esposas['identificador'] = df['identificador']
        esposas['nombre_completo'] = esposas.apply(lambda x: f"{x['nombre']} {x['apellidos']}", axis=1)
        
        #esposas['nombre_completo'] = esposas.apply(lambda x: x.nombre_completo.replace('N N', f'N N {x.identificador}'), axis=1)
        
        save_personas = pd.concat([padres, madres, maridos, esposas])
        save_personas.reset_index(inplace=True, drop=True)
        save_personas.index = save_personas.index + 1
        save_personas['nombre_completo'] = save_personas['nombre_completo'].apply(unidecode)
        
        save_personas.drop_duplicates(inplace=True)
        save_personas['nombre'] = save_personas['nombre'].replace('', np.nan)
        #save_personas.dropna(inplace=True, how='all')
        save_personas.dropna(subset=['nombre'], inplace=True)
        
        
        save_personas.to_excel('toolboximport/importfiles/personas.xlsx', index_label='id')
        save_personas.to_csv('toolboximport/importfiles/personas.csv', encoding='utf-8')
        
        df_difuntos = pd.read_excel('toolboximport/importfiles/difuntos.xlsx')
        
        df_personas_total = pd.concat([df_difuntos, save_personas])
        df_personas_total.reset_index(drop=True)
        df_personas_total.index = df_personas_total.index + 1
        
        df_personas_total.drop_duplicates(subset=['nombre_completo'], inplace=True)
        
        df_personas_total.to_excel('toolboximport/importfiles/personas_total.xlsx', index_label='id')
        df_personas_total.to_csv('toolboximport/importfiles/personas_total.csv', encoding='utf-8')

    def prepare_data(self):
        # archivo_id, archivo_idno, archivo_nombre, archivo_sigla
        
        redf = self.df.copy()
        
        redf.index = redf.index + 1
        
        columns_to_replace = redf.columns.difference(['Fecha aaaa-mm-dd'])
        redf[columns_to_replace] = redf[columns_to_replace].apply(lambda x: x.replace('-', '', regex=True))
        
        redf['archivo_nombre'] = "Archivo Histórico Parroquial de Aucará"
        redf['archivo_sigla'] = "AHPA"
        
        # documento_id, documento_idno, archivo, unidad_documental, identificador, titulo_documento, folios, rango_imagenes, notas, condicion_documento
        redf['archivo'] = 'AHPA'
        # lugar_id, lugar_idno, nombre, otros_nombres, tipo, lat, lon
        
        redf.rename(
            columns={
                'Unidad Documental Compuesta (a la que pertenece)': 'unidad_documental',
                'Identificador (es recomendable seguir una secuencia numeral como la mostrada en los ejemplos)': 'secuencia',
                'Título (incluir un título breve para cada documento)': 'titulo_documento',
                'Folio inicial del documento (convertir como se muestra abajo)': 'folio_inicial',
                'Folio final del documento (convertir como se muestra abajo)': 'folio_final',
                'Imagen inicial (estos valores serán añadidos cuando comience el proceso de revisión de imágenes)': 'img_inicial',
                'Imagen final (estos valores serán añadidos cuando comience el proceso de revisión de imágenes)': 'img_final',
                'Notas adicionales del documento': 'notas',
                'Caracterísitcas físicas (Estado de Conservación de los materiales fisicos)': 'condicion_documento',
                'Doctrina': 'doctrina',
                'Lugar donde se toma la declaración de fallecimiento / O desde donde se manda dar sepultura': 'lugar_declaracion',
                'Fecha aaaa-mm-dd': 'fecha',
                'Procedencia': 'vecindad',
                'Condición': 'condicion',
                'Marido (añadir una + después del nombre si es difunto)': 'marido',
                'Esposa (añadir una + después del nombre si es difunta)': 'esposa',
                'Tipo de entierro/Cruz Alta o Baja': 'tipo_entierro',
                'Nombre del difunto (a)': 'nombre_difunto',
                'Apellido del difunto (a)': 'apellido_difunto',
                'Lugar de enterramiento': 'lugar_enterramiento',
                'Hijo legítimo/ natural': 'legitimidad',
                'Nombre del padre': 'nombre_padre',
                'Apellido del padre': 'apellido_padre',
                'Nombre de la madre': 'nombre_madre',
                'Apellido de la madre': 'apellido_madre',
                'Causa de muerte': 'causa_muerte',
                'Recibió auxilio espiritual': 'auxilio_espiritual'
            }, inplace=True
        )
        
        # folios
        redf['unidad_documental'] = redf['unidad_documental'].fillna(value="Ninguna")
        redf['identificador'] = redf.apply(lambda x: f'{x.unidad_documental}-{x.secuencia}', axis=1)
        
        redf['folio_inicial'] = redf['folio_inicial'].fillna(' ')
        redf['folio_final'] = redf['folio_final'].fillna(' ')
        
        redf['folio_inicial'] = redf['folio_inicial'].apply(lambda x: f'{x}r' if isinstance(x, int) else x.lower())
        redf['folio_final'] = redf['folio_final'].apply(lambda x: f'{x}v' if isinstance(x, int) else x.lower())
        
        redf['folios'] = redf.apply(lambda x: f'{x.folio_inicial};{x.folio_final}' if x.folio_inicial != x.folio_final else x.folio_inicial, axis=1)
        redf['rango_imagenes'] = redf.apply(lambda x: f'{x.img_inicial};{x.img_final}' if x.img_inicial != x.img_final else x.img_inicial, axis=1)
        
        redf['titulo_documento'] = redf['titulo_documento'].fillna("Sin título")
        redf['folios'] = redf['folios'].apply(lambda x: x.replace('  ', '0r'))
        redf['identificador'] = redf['identificador'].fillna("Sin identificador")
        
        savearchivo = redf[['archivo_nombre', 'archivo_sigla']].drop_duplicates()
        savearchivo.dropna(inplace=True, how='all')
        
        savearchivo.to_excel('toolboximport/importfiles/archivo_entierros.xlsx', index_label='id')
        savearchivo.to_csv('toolboximport/importfiles/archivo_entierros.csv', encoding='utf-8')
        savedocumentos = redf[['archivo', 'unidad_documental', 'identificador', 'titulo_documento', 'folios', 'rango_imagenes', 'notas', 'condicion_documento']].drop_duplicates()
        savedocumentos.dropna(inplace=True, how='all')
        
        savedocumentos.to_excel('toolboximport/importfiles/documentos_entierros.xlsx', index_label='id')
        savedocumentos.to_csv('toolboximport/importfiles/documentos_entierros.csv', encoding='utf-8')
        
        self.prepare_places(redf)
        
        columns_to_replace = ['nombre_difunto', 'apellido_difunto', 'nombre_padre', 'apellido_padre', 'nombre_madre', 'apellido_madre']
        
        redf[columns_to_replace] = redf[columns_to_replace].apply(lambda x: x.replace('', np.nan, regex=False))
        redf[columns_to_replace] = redf[columns_to_replace].fillna("N")
        redf[columns_to_replace] = redf[columns_to_replace].apply(lambda x: x.replace(r'\.', '', regex=True))
        
        self.prepare_personas_entierros(redf)
        self.prepare_personas_relacionadas(redf)
        
        #entierro_id, entierro_idno, acta_entierro, persona, lugar, doctrina, fecha, lugar_declaracion, legitimidad_difunto, estado_difunto, padre, madre, conyuge, conyuge_sobrevive, tipo_de_entierro, causa_fallecimiento, auxilio_espiritual, denunciantes
        
        entierro = pd.DataFrame()
        entierro['acta_entierro'] = redf['identificador']
        entierro['persona'] = redf.apply(lambda x: f"{x['nombre']} {x['apellidos']}", axis=1)
        entierro['persona'] = entierro['persona'].apply(unidecode)
        entierro['persona'] = entierro.apply(lambda x: x.persona.replace('N N', f'N N {x.acta_entierro}'), axis=1)
        entierro['lugar'] = redf['lugar_enterramiento'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) else x)
        entierro['lugar'] = entierro['lugar'].fillna('Desconocido')
        entierro['doctrina'] = redf['doctrina'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) else x)
        entierro[['fecha', 'notas_fecha']] = redf.apply(lambda row: self.prepare_date(row['fecha']), axis=1, result_type='expand')
        entierro['lugar_declaracion'] = redf['lugar_declaracion'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) else x)
        entierro['legitimidad_difunto'] = redf['legitimidad']
        entierro['estado_difunto'] = redf['Estado']
        entierro['padre'] = redf.apply(lambda x: f"{x['nombre_padre']} {x['apellido_padre']}", axis=1)
        entierro['madre'] = redf.apply(lambda x: f"{x['nombre_madre']} {x['apellido_madre']}", axis=1)
        entierro['conyuge'] = redf.apply(lambda x: x['marido'] if x['marido'] else x['esposa'], axis=1)
        entierro['conyuge_sobrevive'] = redf.apply(lambda x: False if ('+' in str(x['marido']) or '+' in str(x['esposa'])) else None, axis=1)
        entierro['tipo_de_entierro'] = redf['tipo_entierro']
        entierro['tipo_de_entierro'] = entierro['tipo_de_entierro'].fillna("n/a")
        entierro['causa_fallecimiento'] = redf['causa_muerte']
        entierro['auxilio_espiritual'] = redf['auxilio_espiritual']
        
        entierro.fillna("", inplace=True)
        
        
        entierro.to_excel('toolboximport/importfiles/entierros.xlsx', index_label='id')
        entierro.to_csv('toolboximport/importfiles/entierros.csv', encoding='utf-8')



path = "/home/sites/toolbox/toolboximport/importfiles/Catalogación Archivo Parroquial de Aucará.xlsx"
excel = pd.read_excel(path, sheet_name=2)
prepare_documentos = Entierros(excel).prepare_data()