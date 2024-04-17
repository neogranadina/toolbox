import pandas as pd
from functools import reduce
import os

dataframes = []

entierros = pd.read_csv("/home/sites/toolbox/toolboximport/importfiles/entierros.csv")
difuntos = pd.read_csv("/home/sites/toolbox/toolboximport/importfiles/difuntos.csv")

print(entierros.columns)
print(difuntos.columns)

# entierros merge by persona, difuntos merge by nombre_completo
difuntos.rename(columns={'nombre_completo':'persona'}, inplace=True)

entierros_new = pd.merge(entierros, difuntos, on=['persona', 'Unnamed: 0'])

reorder_columns = ['Unnamed: 0','acta_entierro','nombre','apellidos','persona','vecindad','condicion','fecha_nacimiento','lugar','doctrina','fecha','notas_fecha','lugar_declaracion','legitimidad_difunto','estado_difunto','padre','madre','conyuge','conyuge_sobrevive','tipo_de_entierro','causa_fallecimiento','auxilio_espiritual']

entierros_new = entierros_new[reorder_columns]


personas = pd.read_csv('/home/sites/toolbox/toolboximport/importfiles/personas.csv')
personas.drop(columns=['Unnamed: 0'], inplace=True)

padres = personas.rename(columns={
                        'nombre_completo': 'padre', 
                        'identificador': 'acta_entierro', 
                        'nombre': 'nombre_padre', 
                        'apellidos': 'apellidos_padre'
})

entierros_padres = pd.merge(entierros_new, padres, on=['padre', 'acta_entierro'], how='left')

reorder_columns_2 = ['Unnamed: 0','acta_entierro','nombre','apellidos','persona','vecindad','condicion','fecha_nacimiento','lugar','doctrina','fecha','notas_fecha','lugar_declaracion','legitimidad_difunto','estado_difunto','nombre_padre','apellidos_padre','padre','madre','conyuge','conyuge_sobrevive','tipo_de_entierro','causa_fallecimiento','auxilio_espiritual']

entierros_padres = entierros_padres[reorder_columns_2]

madres = personas.rename(columns={
                        'nombre_completo': 'madre', 
                        'identificador': 'acta_entierro', 
                        'nombre': 'nombre_madre', 
                        'apellidos': 'apellidos_madre'
})

entierros_madres = pd.merge(entierros_padres, madres, on=['madre', 'acta_entierro'], how='left')

reorder_columns_3 = ['Unnamed: 0','acta_entierro','nombre','apellidos','persona','vecindad','condicion','fecha_nacimiento','lugar','doctrina','fecha','notas_fecha','lugar_declaracion','legitimidad_difunto','estado_difunto','nombre_padre','apellidos_padre','padre', 'nombre_madre', 'apellidos_madre', 'madre','conyuge','conyuge_sobrevive','tipo_de_entierro','causa_fallecimiento','auxilio_espiritual']

entierros_madres = entierros_madres[reorder_columns_3]

entierros_madres.to_csv("/home/sites/toolbox/toolboximport/importfiles/a.csv", index=False)
