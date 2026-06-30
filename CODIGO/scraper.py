### AQUI VA EL CODIGO DE EXTRACCION USANDO LA API
import requests
import json
import time
import os


class ScraperHimalayas:
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

    def guardar_json(self, datos, nombre="datos/crudos/ofertas_himalayas.json"):
        """
        Guarda los datos obtenidos en un archivo JSON.
        """
        os.makedirs(os.path.dirname(nombre), exist_ok=True)

        with open(nombre, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

        print(f"Datos guardados en: {nombre}")

    def ejecutar_scraping(self, max_ofertas=100):
        """
        Ejecuta la extracción de ofertas utilizando paginación.
        """
        todas_las_ofertas = []
        offset = 0
        limite = 20  # Máximo permitido por solicitud

        while len(todas_las_ofertas) < max_ofertas:

            print(f"Obteniendo ofertas desde offset {offset}...")

            data = self.obtener_ofertas(limite=limite, offset=offset)

            if not data or not data.get("jobs"):
                print("No se encontraron más ofertas.")
                break

            ofertas_pagina = data["jobs"]
            todas_las_ofertas.extend(ofertas_pagina)

            print(f"→ {len(ofertas_pagina)} ofertas obtenidas")

            if offset + limite >= data.get("totalCount", 0):
                break

            offset += limite

            # Espera de 1 segundo entre solicitudes
            time.sleep(1)

        self.ofertas = todas_las_ofertas

        print(f"\nTotal de ofertas obtenidas: {len(self.ofertas)}")

        return self.ofertas


if __name__ == "__main__":

    scraper = ScraperHimalayas()

    ofertas = scraper.ejecutar_scraping(max_ofertas=100)

    scraper.guardar_json(ofertas)
