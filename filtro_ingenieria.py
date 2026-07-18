import pandas as pd

print("Iniciando Fase 2 (Corregida): Buscando artículos con enfoque en Ingeniería y Desarrollo...")

#Cargar la base de los 288 artículos de educación básica
df = pd.read_excel("Cribado_Fase_Poblacion.xlsx")

#Trabajar solo con los aprobados en la Fase 1
df_fase2 = df[df['Sugerencia_Poblacion'].str.contains('Mantener', na=False)].copy()

#Unir Título y Resumen y convertirlos a minúsculas
df_fase2['Title'] = df_fase2['Title'].fillna("")
df_fase2['Abstract'] = df_fase2['Abstract'].fillna("")
df_fase2['Texto_Busqueda'] = (df_fase2['Title'] + " " + df_fase2['Abstract']).str.lower()

#Palabras clave del área de INGENIERÍA DE SOFTWARE Y SISTEMAS
terminos_ingenieria = [
    'architecture', 'framework', 'algorithm', 'system design', 'development',
    'implementation', 'machine learning model', 'accuracy', 'rmse', 'f1-score',
    'neural network', 'reinforcement learning', 'fuzzy logic', 'data mining',
    'decision tree', 'predictive model', 'software engineering', 'dataset',
    'computational', 'system architecture'
]

#Función de clasificación con enfoque técnico
def clasificar_enfoque(texto):
    tiene_ingenieria = any(word in texto for word in terminos_ingenieria)
    
    if tiene_ingenieria:
        return "✅ APROBADO FINAL (Enfoque en Sistema/Algoritmo)"
    else:
        return "❌ Excluir (Enfoque puramente pedagógico/No detalla el sistema)"

#Aplicar el filtro
df_fase2['Sugerencia_Enfoque'] = df_fase2['Texto_Busqueda'].apply(clasificar_enfoque)

#Limpiar y ordenar
df_fase2 = df_fase2.drop(columns=['Texto_Busqueda', 'Sugerencia_Poblacion'])
df_fase2 = df_fase2.sort_values(by='Sugerencia_Enfoque')

#Guardar el archivo final
nombre_salida = "Lista_Final_Ingenieria.xlsx"
df_fase2.to_excel(nombre_salida, index=False)

#Contar los resultados
conteos = df_fase2['Sugerencia_Enfoque'].value_counts()

print("-" * 60)
print("¡CRIBADO TÉCNICO COMPLETADO!")
print("-" * 60)
print("De tus 288 artículos, el sistema detectó:")
for categoria, cantidad in conteos.items():
    print(f"{categoria}: {cantidad} artículos")
print("-" * 60)
print(f"Archivo guardado como: {nombre_salida}")