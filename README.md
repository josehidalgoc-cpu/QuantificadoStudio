# Ecuador Quantificado 2026: Análisis de la Canasta Familiar Básica (CFB)

Este repositorio contiene un entorno de análisis estadístico completamente contenedorizado y reproducible para evaluar la composición del costo de vida en el Ecuador, desarrollado para la convocatoria **Ecuador Quantificado 2026** organizada por *El Quantificador* y *LIDE*.

El objetivo del proyecto es desglosar los macrocomponentes económicos que dictan el presupuesto de un hogar tipo en el país, utilizando datos oficiales y un flujo de trabajo que mitiga por completo los conflictos de dependencias locales.

## Arquitectura del Proyecto

La solución se divide en tres componentes clave para garantizar la inmutabilidad y reproducibilidad del análisis:

* **`Dockerfile`**: Configura un contenedor basado en una imagen ligera de Linux (`python:3.11-slim`), encargándose de instalar de forma aislada las librerías estadísticas necesarias (`pandas`, `matplotlib`, `seaborn`).
* **`analisis_canasta.py`**: Script automatizado en Python encargado de la ingesta del reporte crudo del INEC, limpieza de tipos de datos, procesamiento y generación de la visualización.
* **`2. Serie historica de la CFB.csv`**: Set de datos oficiales emitidos por el Instituto Nacional de Estadística y Censos (INEC).

---

## Pipeline de Procesamiento de Datos (ETL)

Al ejecutar el contenedor, el algoritmo realiza de forma automática las siguientes transformaciones sobre el archivo del INEC:
1. **Salto de Metadatos:** Ignora las primeras 12 filas informativas y notas metodológicas del reporte del INEC para indexar directamente la cabecera de la tabla.
2. **Normalización Decimal:** Convierte los separadores decimales del formato regional de comas (`,`) al estándar computacional de puntos (`.`).
3. **Filtrado de Componentes:** Remueve los agregados totales y extrae únicamente los cuatro macrogrupos principales de consumo: *Alimentos y Bebidas*, *Vivienda*, *Misceláneos* e *Indumentaria*.
4. **Capa Visual:** Genera un gráfico de barras optimizado con etiquetas de datos directas (`data labels`) para evitar ambigüedades en la lectura.

---

## Instrucciones de Reproducción Estricta

Para auditar o replicar localmente este análisis sin necesidad de configurar Python ni instalar librerías en su sistema anfitrión, asegúrese de tener **Docker** iniciado y ejecute los siguientes comandos en su terminal (PowerShell o Bash) situándose en la raíz de este directorio:

```bash
# 1. Construir la imagen inmutable del entorno
docker build -t concurso-ecuador .

# 2. Ejecutar el contenedor y exportar el gráfico en caliente
docker run --rm -v "${PWD}:/app" concurso-ecuador

<img width="3600" height="2100" alt="grafico_canasta_ecuador" src="https://github.com/user-attachments/assets/95f1aba5-f0ab-40d1-a7df-50182206eba8" />
