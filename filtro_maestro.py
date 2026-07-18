import pandas as pd
import re

print("Ejecutando el Filtro Maestro de Inteligencia Artificial...")

# 1. Leer los 207 artículos aprobados
# Asegúrate de que el nombre coincida con tu archivo
df = pd.read_excel("Lista_Final_Ingenieria.xlsx") 
df_approved = df[df['Sugerencia_Enfoque'].str.contains('APROBADO', na=False)].copy()

# 2. Algoritmo de Evaluación Semántica Ponderada (Filtro Master)
def semantic_score(row):
    text = (str(row['Title']) + " " + str(row['Abstract'])).lower()
    score = 0
    
    # Penalización estricta (Elimina los universitarios que se pudieron colar)
    higher_ed_terms = ['higher education', 'higher-education', 'university', 'undergraduate', 'college']
    if any(re.search(r'\b' + term + r'\b', text) for term in higher_ed_terms):
        score -= 50 
        
    # Bonificación poblacional estricta (K-12 explícito)
    k12_terms = ['k-12', 'high school', 'middle school', 'primary school', 'secondary school', 'elementary']
    if any(re.search(r'\b' + term + r'\b', text) for term in k12_terms):
        score += 20
        
    # Criterio de Comparación EXACTO (Pregunta Master: "en comparación con métodos tradicionales")
    comparison_patterns = [
        r'compared to traditional', r'compared with traditional', r'control group', 
        r'experimental group', r'quasi-experimental', r'traditional teaching', 
        r'conventional method', r'traditional method'
    ]
    if any(re.search(pattern, text) for pattern in comparison_patterns):
        score += 30
        
    # Criterio Tecnológico
    tech_terms = ['architecture', 'framework', 'machine learning', 'artificial intelligence', 'neural network', 'tutoring system', 'adaptive learning']
    tech_count = sum(1 for term in tech_terms if re.search(r'\b' + term + r'\b', text))
    score += (tech_count * 5)
    
    # Criterio de Resultados (Motivación / Rendimiento)
    outcome_terms = ['academic performance', 'learning outcome', 'engagement', 'motivation', 'personaliz']
    outcome_count = sum(1 for term in outcome_terms if re.search(r'\b' + term + r'\b', text))
    score += (outcome_count * 10)
    
    return score

# 3. Aplicar IA y filtrar la Élite
df_approved['Nivel_Relevancia'] = df_approved.apply(semantic_score, axis=1)
# Nos quedamos con los que tienen una puntuación excelente (Puntaje >= 40)
df_golden = df_approved[df_approved['Nivel_Relevancia'] >= 40].sort_values(by='Nivel_Relevancia', ascending=False).copy()

# 4. Preparar la Matriz de Extracción para las RQ
columnas_mantener = ['Title', 'Authors', 'Year', 'Journal', 'DOI', 'Abstract']
df_matriz = df_golden[columnas_mantener].copy()

# Crear las columnas vacías para que extraigas la información
df_matriz['RQ1_Poblacion_Exacta'] = ""
df_matriz['RQ2_Tecnologia_y_Algoritmo'] = ""
df_matriz['RQ3_Metodo_Tradicional_Comparado'] = ""
df_matriz['RQ4_Resultados_Rendimiento_Motivacion'] = ""
df_matriz['RQ5_Desafios_Tecnicos'] = ""

# 5. Exportar
nombre_salida = "Matriz_Extraccion_Final_RQ.xlsx"
df_matriz.to_excel(nombre_salida, index=False)

print("-" * 60)
print("¡FILTRO MAESTRO COMPLETADO!")
print(f"De 207 artículos, hemos extraído los {len(df_golden)} artículos de ÉLITE.")
print(f"Archivo generado: {nombre_salida}")
print("El archivo ya incluye las columnas en blanco para que respondas las RQ.")
print("-" * 60)