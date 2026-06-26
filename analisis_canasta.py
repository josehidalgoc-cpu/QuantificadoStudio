import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

archivo = "2. Serie historica de la CFB.csv"

if not os.path.exists(archivo):
    print(f"Error: No se encuentra el archivo {archivo}")
    exit(1)

# Leer el archivo con el separador correcto (punto y coma) saltando el encabezado del INEC (fila 13 reales)
df = pd.read_csv(archivo, sep=';', encoding='utf-8', skiprows=12)

# Limpiar espacios en los nombres de las columnas
df.columns = df.columns.str.strip()

# Filtrar las columnas que nos interesan y limpiar filas vacías o nulas
df = df[['Grupos y Subgrupos de Consumo', 'Costo Actual en Dólares']].dropna()

# Convertir el costo a número flotante, corrigiendo la coma decimal
df['Costo Actual en Dólares'] = df['Costo Actual en Dólares'].astype(str).str.replace(',', '.')
df['Costo Actual en Dólares'] = pd.to_numeric(df['Costo Actual en Dólares'], errors='coerce')

# Eliminar la fila del TOTAL para graficar solo los componentes principales
df_componentes = df[df['Grupos y Subgrupos de Consumo'].str.contains('TOTAL') == False].dropna()

# Filtrar solo los 4 grupos principales de la Canasta Básica
grupos_principales = ['ALIMENTOS Y BEBIDAS', 'VIVIENDA', 'INDUMENTARIA', 'MISCELÁNEOS']
df_filtrado = df_componentes[df_componentes['Grupos y Subgrupos de Consumo'].str.strip().isin(grupos_principales)]

# --- CONFIGURAR EL GRÁFICO (Este script SÍ genera un gráfico de barras limpio) ---
plt.figure(figsize=(12, 7)) # Tamaño un poco más grande
sns.set_theme(style="whitegrid")

# Gráfico de barras de los componentes con paleta de azules
ax = sns.barplot(
    data=df_filtrado, 
    x='Grupos y Subgrupos de Consumo', 
    y='Costo Actual en Dólares', 
    palette='Blues_r',
    hue='Grupos y Subgrupos de Consumo', # Requerido por Seaborn moderno
    legend=False
)

# Añadir etiquetas de valor arriba de cada barra de forma clara
for p in ax.patches:
    if p.get_height() > 0: # Solo si hay valor
        ax.annotate(f"${p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height() + 5),
                    ha='center', va='center', fontsize=12, color='black', xytext=(0, 7),
                    textcoords='offset points', fontweight='bold')

plt.title("Ecuador: Distribución del Costo de la Canasta Familiar Básica (Mayo 2026)", fontsize=14, fontweight='bold')
plt.xlabel("Grupo de Consumo", fontsize=12)
plt.ylabel("Costo en USD ($)", fontsize=12)
plt.ylim(0, max(df_filtrado['Costo Actual en Dólares']) + 50) # Espacio para las etiquetas

# Guardar el output como 'grafico_canasta_ecuador.png'
os.makedirs("output", exist_ok=True)
plt.tight_layout()
plt.savefig("output/grafico_canasta_ecuador.png", dpi=300)
print("¡Proceso completado con éxito! Gráfico guardado en output/grafico_canasta_ecuador.png")