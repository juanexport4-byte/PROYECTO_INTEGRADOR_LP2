"""
Clase para extraer información usando expresiones regulares (regex)
"""

import re
import pandas as pd
import os

class ExtractorRegex:
    """
    Clase que se usa para extraer información
    de las descripciones de ofertas de trabajo
    """
    
    def __init__(self, ruta_csv="datos/procesados/ofertas_limpias.csv"):
        """
        Inicializa el extractor cargando el CSV limpio
        El argumento ruta_csv (str): Ruta al archivo CSV con datos ya limpios
        """
        self.ruta_csv = ruta_csv
        self.df = None
        self._cargar_datos()
    
    def _cargar_datos(self):
        """
        Carga el CSV que genera procesador.py y lo convierte a DataFrame de pandas
        """
        try:
            self.df = pd.read_csv(self.ruta_csv, encoding='utf-8-sig')
            print(f"Datos cargados: {len(self.df)} ofertas")
            print(f" Columnas disponibles: {list(self.df.columns)}")
            return self.df
        except FileNotFoundError:
            print(f"ERROR: No se encontró el archivo: {self.ruta_csv}")
            print(" Verifica que hayas ejecutado primero el procesador")
            self.df = pd.DataFrame()
            return self.df