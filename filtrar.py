import pandas as pd
import numpy as np
import string

#Documentos en csv y xls con los datos de Scopus y Web of Science respectivamente
archivo_scopus = "scopus.csv"
archivo_wos = "wos.xls" 

print("Cargando bases de datos, por favor espera...")
scopus_df = pd.read_csv(archivo_scopus)
wos_df = pd.read_excel(archivo_wos)

#Estandarizar columnas de Scopus
scopus_clean = scopus_df[['Title', 'Authors', 'Year', 'Source title', 'DOI', 'Abstract', 'Document Type']].copy()
scopus_clean.rename(columns={'Source title': 'Journal'}, inplace=True)
scopus_clean['Database'] = 'Scopus'

#standarizar columnas de Web of Science
wos_clean = wos_df[['Article Title', 'Authors', 'Publication Year', 'Source Title', 'DOI', 'Abstract', 'Document Type']].copy()
wos_clean.rename(columns={'Article Title': 'Title', 'Publication Year': 'Year', 'Source Title': 'Journal'}, inplace=True)
wos_clean['Database'] = 'Web of Science'

#Unir ambas bases de datos en una sola lista gigante
combined_df = pd.concat([scopus_clean, wos_clean], ignore_index=True)

#Funciones para limpiar el texto y comparar exactamente igual
def clean_doi(doi):
    if pd.isna(doi): return np.nan
    return str(doi).strip().lower()

def clean_title(title):
    if pd.isna(title): return ""
    t = str(title).lower().strip()
    t = t.translate(str.maketrans('', '', string.punctuation))
    return " ".join(t.split())

combined_df['Clean_DOI'] = combined_df['DOI'].apply(clean_doi)
combined_df['Clean_Title'] = combined_df['Title'].apply(clean_title)

#Proceso de eliminación de duplicados
# Fase A: Eliminar duplicados buscando el mismo código DOI
has_doi = combined_df.dropna(subset=['Clean_DOI'])
no_doi = combined_df[combined_df['Clean_DOI'].isna()]
dedup_by_doi = has_doi.drop_duplicates(subset=['Clean_DOI'], keep='first')

# Fase B: Unir los que no tenían DOI y buscar duplicados por Título idéntico
step1_df = pd.concat([dedup_by_doi, no_doi], ignore_index=True)
dedup_final = step1_df.drop_duplicates(subset=['Clean_Title'], keep='first')

# Limpiar las columnas temporales de ayuda
dedup_final = dedup_final.drop(columns=['Clean_DOI', 'Clean_Title'])

#Guardar el archivo final unificado en Excel
nombre_salida = "Revision_Sistematica_Sin_Duplicados.xlsx"
dedup_final.to_excel(nombre_salida, index=False)

#Resuemnen del proceso
print("-" * 40)
print("¡PROCESO COMPLETADO CON ÉXITO!")
print(f"Registros iniciales en Scopus: {len(scopus_df)}")
print(f"Registros iniciales en WoS: {len(wos_df)}")
print(f"Total bruto inicial: {len(scopus_df) + len(wos_df)}")
print(f"Duplicados eliminados: {(len(scopus_df) + len(wos_df)) - len(dedup_final)}")
print("-" * 40)
print(f"TOTAL DE REGISTROS ÚNICOS (Para Screening): {len(dedup_final)}")
print(f"Archivo generado: {nombre_salida}")
print("-" * 40)