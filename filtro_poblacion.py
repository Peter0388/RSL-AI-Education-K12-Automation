import pandas as pd
import re

print("Iniciando lectura de resúmenes con Inteligencia Artificial (Filtro de Población)...")

#Cargar el archivo sin duplicados ( Revision_Sistematica_Sin_Duplicados.xlsx)
df = pd.read_excel("Revision_Sistematica_Sin_Duplicados.xlsx")

#Unir Título y Resumen y convertirlos a minúsculas para facilitar la búsqueda
df['Title'] = df['Title'].fillna("")
df['Abstract'] = df['Abstract'].fillna("")
df['Texto_Busqueda'] = (df['Title'] + " " + df['Abstract']).str.lower()

#Diccionarios de palabras clave (en inglés)

# Palabras que indican exclusión (Educación superior, adultos, profesionales)
excluir_keywords = [
    'higher education', 'university', 'universities', 'college', 'undergraduate', 
    'postgraduate', 'tertiary education', 'higher-education', 'medical student', 
    'nursing student', 'adult learner', 'workplace', 'corporate', 'vocational'
]

# Palabras que indican inclusión (Educación Básica)
incluir_keywords = [
    'k-12', 'k12', 'primary education', 'secondary education', 'high school', 
    'middle school', 'elementary', 'kindergarten', 'pupils', 'school students', 
    'basic education', 'early childhood', 'primary school', 'secondary school',
    '1st grade', '2nd grade', '3rd grade', '4th grade', '5th grade', '6th grade',
    '7th grade', '8th grade', '9th grade', '10th grade', '11th grade', '12th grade'
]

#Función de clasificación lógica
def clasificar_poblacion(texto):
    tiene_superior = any(word in texto for word in excluir_keywords)
    tiene_basica = any(word in texto for word in incluir_keywords)
    
    # Si menciona básica, lo mantenemos (incluso si compara con universidad)
    if tiene_basica:
        return "🟢 Mantener (Educación Básica)"
    # Si solo menciona superior y no básica, se va
    elif tiene_superior and not tiene_basica:
        return "🔴 Excluir (Universitario/Adultos)"
    # Si no especifica (solo dice "students" o "learners")
    else:
        return "🟡 Ambiguo (No especifica)"

#Aplicar el filtro a los 1,920 artículos
df['Sugerencia_Poblacion'] = df['Texto_Busqueda'].apply(clasificar_poblacion)

#Limpiar columna temporal de búsqueda y ordenar
df = df.drop(columns=['Texto_Busqueda'])
df = df.sort_values(by='Sugerencia_Poblacion')

#Guardar el nuevo Excel
nombre_salida = "Cribado_Fase_Poblacion.xlsx"
df.to_excel(nombre_salida, index=False)

#Contar los resultados
conteos = df['Sugerencia_Poblacion'].value_counts()

print("-" * 50)
print("¡CRIBADO COMPLETADO EN SEGUNDOS!")
print("-" * 50)
print("Resultados de la clasificación automática:")
for categoria, cantidad in conteos.items():
    print(f"{categoria}: {cantidad} artículos")
print("-" * 50)
print(f"Archivo guardado como: {nombre_salida}")
print("¡Ahora solo debes enfocarte en revisar los artículos clasificados como 🟢!")