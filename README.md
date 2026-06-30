# Proyecto integrador

## 👥 Integrantes del Grupo
* **20241372	Aguilar Farfán, Juan Fernando** - [@juanexport4-byte](https://github.com/juanexport4-byte)
* **20241384	Guevara Alvarado, Samuel Christian** - [@chrissg05](https://github.com/chrissg05)
* **20241392	Pacheco Pampas, Merly Vanessa** - [@usuario_github3](https://github.com/usuario_github3)
* **20241402	Santillan Santa Cruz Alex** - [@jois-2003](https://github.com/usuario_github3)
* **20201406	Delgado Conzuero Nathaly** - [@NathalyDC](https://github.com/NathalyDC)

---

# Proyecto Integrador - Lenguaje de Programación II

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un sistema completo de **análisis de ofertas de trabajo** utilizando técnicas de Web Scraping, procesamiento de datos y visualización. El objetivo principal es extraer información de ofertas de empleo del sector tecnológico, procesarla y generar insights relevantes sobre el mercado laboral actual.

El proyecto aplica los siguientes conceptos:
- **Programación Orientada a Objetos (POO)** con tres clases principales
- **Programas en red** con solicitudes HTTP a una API pública
- **Expresiones regulares (Regex)** para extraer información estructurada de textos no estructurados
- **Procesamiento de datos** con pandas para limpieza y transformación
- **Visualización** de datos con matplotlib y seaborn
- **Trabajo colaborativo** con Git y GitHub

### Problema que Resuelve

En el mercado laboral actual, existe una gran cantidad de información dispersa en diferentes plataformas. Este proyecto centraliza y analiza datos de ofertas de trabajo para responder preguntas como:

- ¿Qué tecnologías son más demandadas?
- ¿Qué empresas ofrecen mejores salarios?
- ¿Predomina el trabajo remoto, híbrido o presencial?
- ¿Qué nivel de experiencia solicitan las empresas?
- ¿Cuáles son los rangos salariales promedio por tecnología?

---

## Pipeline del Proyecto

```
El proyecto sigue un flujo de procesamiento de datos en 5 etapas:
┌─────────────────────────────────────────────────────────────────────┐
│ PIPELINE DE DATOS │
├─────────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ SCRAPER │ → │ LIMPIEZA │ → │ REGEX │ → │ GRÁFICOS │ │
│ │ (API) │ │ (PANDAS) │ │(EXTRACCIÓN) │(VISUALIZAR) │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│ ↓ ↓ ↓ ↓ │
│ datos/crudos/ datos/procesados/ datos/procesados/ graficos/ │
│ ofertas_ ofertas_limpias.csv ofertas_con_regex.csv *.png │
│ hiringcafe.json │
│ │
│ ↓ │
│ ┌──────────────────┐ │
│ │ NOTEBOOK │ │
│ │ (ANÁLISIS FINAL) │ │
│ └──────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────┘
```

### Explicación de cada etapa:

| Etapa | Integrante | Entrada | Salida | Descripción |
|-------|------------|---------|--------|-------------|
| **1. Scraper** | Integrante 1 | API de Himalayas | `datos/crudos/ofertas_hiringcafe.json` | Extrae ofertas de trabajo desde la API pública |
| **2. Limpieza** | Integrante 2 | JSON crudo | `datos/procesados/ofertas_limpias.csv` | Limpia duplicados, nulos y formatea los datos |
| **3. Regex** | Integrante 3 | CSV limpio | `datos/procesados/ofertas_con_regex.csv` | Extrae tecnologías, salarios, modalidad, nivel y años de experiencia |
| **4. Visualizador** | Integrante 4 | CSV enriquecido | `graficos/*.png` | Genera 5 gráficos diferentes |
| **5. Notebook** | Integrante 5 | Todos los anteriores | `cuadernos/analisis_final.ipynb` | Integra y presenta el análisis completo |

---

## Estructura del Proyecto

```
proyecto-integrador-lp2/
│
├── codigo/ # Código fuente (archivos .py)
│ ├── init.py # Convierte la carpeta en un paquete Python
│ ├── scraper.py # Extrae datos de la API
│ ├── procesador.py # Limpia y transforma datos
│ ├── utilidades.py # Extrae con expresiones regulares
│ └── visualizador.py # Genera gráficos
│
├── datos/ # Datos (JSON, CSV)
│ ├── crudos/ # Datos sin procesar
│ │ └── ofertas_hiringcafe.json # JSON original extraído de la API
│ └── procesados/ # Datos ya procesados
│ ├── ofertas_limpias.csv # Datos limpios (eliminados duplicados, nulos)
│ └── ofertas_con_regex.csv # Datos enriquecidos con nuevas columnas
│
├── graficos/ # Imágenes generadas
│ ├── salarios_empresa.png # Gráfico 1: Top empresas con mejor salario
│ ├── modalidades.png # Gráfico 2: Distribución de modalidades
│ ├── tecnologias.png # Gráfico 3: Tecnologías más demandadas
│ ├── niveles_experiencia.png # Gráfico 4: Niveles de experiencia requeridos
│ └── heatmap_tecnologias_modalidad.png # Gráfico 5: Relación tecnologías-modalidad
│
├── cuadernos/ # Jupyter Notebooks
│ └── analisis_final.ipynb # Análisis 
│
├── requirements.txt # Librerías necesarias para ejecutar
├── README.md # Documentación del proyecto (este archivo)
└── .gitignore # Archivos ignorados por Git
```


### Explicación detallada de lo que contiene cada carpeta

```
| Carpeta | Propósito | ¿Qué archivos contiene? |
|---------|-----------|------------------------|
| **`codigo/`** | Código fuente de Python | 4 archivos `.py` con las clases del proyecto |
| **`datos/crudos/`** | Datos sin procesar | El JSON original extraído de la API |
| **`datos/procesados/`** | Datos procesados | CSVs limpios y enriquecidos con nuevas columnas |
| **`graficos/`** | Visualizaciones | 5 imágenes PNG generadas automáticamente |
| **`cuadernos/`** | Análisis interactivo | 1 Jupyter Notebook con el análisis final |
```

### Nuevas columnas agregadas en el procesamiento:

```
| Columna | Origen | Descripción |
|---------|--------|-------------|
| `rango_salarial` | Procesador | Rango salarial formateado (ej: "80000 - 120000 USD") |
| `salario_promedio` | Procesador | Promedio entre salario mínimo y máximo |
| `tipo_empleo_simple` | Procesador | Categoría simplificada (Full Time, Part Time, etc.) |
| `tecnologias` | Regex | Lista de tecnologías encontradas en la descripción |
| `salario_mencionado` | Regex | Rango salarial extraído del texto (si existe) |
| `modalidad` | Regex | Remoto, Híbrido, Presencial o No especificado |
| `nivel_experiencia` | Regex | Senior, Junior, Mid-Level, etc. |
| `anos_experiencia` | Regex | Años de experiencia requeridos (ej: "5+ años") |
```
