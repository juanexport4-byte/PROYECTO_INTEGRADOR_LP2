INDICACIONES INICIALES PARA EL TRABAJO : 

proyecto-integrador-lp2/          # Carpeta principal del proyecto
│
├── src/                          # CÓDIGO FUENTE (archivos .py)
│   ├── __init__.py               # Convierte src en un paquete Python
│   ├── scraper.py                # MERLY - Clase ScraperHiringCafe
│   ├── procesador.py             # SAMUEL - Clase ProcesadorDatos
│   ├── visualizador.py           # ALEX - Clase VisualizadorGraficos
│   └── utils.py                  # JUAN - Funciones con regex
│
├── data/                         # DATOS (archivos .json, .csv)
│   ├── raw/                      # Datos sin procesar
│   │   └── datos.json   # Generado por scraper.py
│   └── processed/                # Datos ya limpios
│       └── datos_limpios.csv       # Generado por procesador.py
│
├── notebooks/                    # ANÁLISIS (archivos .ipynb)
│   └── analisis_final.ipynb      # NATHALY - Notebook final
│
├── requirements.txt              # Librerías necesarias
├── README.md                     # explicación del proyecto
└── .gitignore                    # Archivos a ignorar en Git
