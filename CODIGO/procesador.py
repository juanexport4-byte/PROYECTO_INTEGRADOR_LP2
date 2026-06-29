import pandas as pd
import json
import os

class ProcesadorDatos:
    """
    Clase para procesar y limpiar los datos de ofertas de trabajo
    """
    
    def __init__(self, archivo_json="datos/crudos/ofertas_hiringcafe.json"):
        """
        Inicializa el procesador cargando los datos del JSON
        """
        self.ruta_json = archivo_json
        self.df = None
        self._cargar_datos()
        
    def _cargar_datos(self):
        """
        Carga el archivo JSON y lo convierte a DataFrame de pandas
        Método interno (empieza con _)
        """
        try:
            with open(self.ruta_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.df = pd.DataFrame(data)
            print(f"Datos cargados correctamente: {len(self.df)} ofertas")
            print(f"   Columnas disponibles: {list(self.df.columns)}")
            return self.df
        except FileNotFoundError:
            print(f"ERROR: No se encontró el archivo: {self.ruta_json}")
            print("   Asegúrate de haber ejecutado primero el scraper")
            self.df = pd.DataFrame()
            return self.df