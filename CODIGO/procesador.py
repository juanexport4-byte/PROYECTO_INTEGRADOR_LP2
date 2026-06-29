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