### AQUI VA EL CODIGO DE EXTRACCION USANDO LA API
import requests
import json
import time
import os


class ScraperHiringCafe:
    """
    Clase para extraer ofertas de trabajo de Himalayas.app vía API.
    """

    def __init__(self):
        self.base_url = "https://himalayas.app/jobs/api"
        self.ofertas = []

    def obtener_ofertas(self, limite=20, offset=0):
        """
        Obtiene una página de ofertas de trabajo desde la API.
        """
        params = {
            "limit": limite,
            "offset": offset
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos: {e}")
            return None
        
def guardar_json(self, datos, nombre="datos/crudos/ofertas_hiringcafe.json"):
    """
    Guarda los datos obtenidos en un archivo JSON.
    """
    os.makedirs(os.path.dirname(nombre), exist_ok=True)

    with open(nombre, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

    print(f"Datos guardados en: {nombre}")