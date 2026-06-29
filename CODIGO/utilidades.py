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
        
    def extraer_tecnologias(self, texto):
        """
        Extrae tecnologías mencionadas en el texto 
        
        Args:
            texto (str): Texto de la descripción
            
        Returns:
            list: Lista de tecnologías encontradas (sin duplicados)
        """
        if not isinstance(texto, str) or pd.isna(texto):
            return []
        
        # Patrón para buscar tecnologías comunes
        patron = r'\b(Python|SQL|Java|JavaScript|React|Node\.js|AWS|Docker|Kubernetes|Git|Linux|TypeScript|Angular|Vue|C#|PHP|Ruby|Go|Rust|Elixir|Swift|Kotlin|Scala|Perl|Shell|Bash|PowerShell|Terraform|Ansible|Jenkins|GitLab|GitHub|Jira|Confluence|Slack|PostgreSQL|MySQL|MongoDB|Redis|Elasticsearch|Kafka|RabbitMQ|Nginx|Apache|Flask|Django|Spring|.NET|Express|Next\.js|GraphQL|REST|API|HTML|CSS|Sass|Tailwind|Bootstrap|Figma|Photoshop|Illustrator|Premiere|After Effects)\b'
        
        tecnologias = re.findall(patron, texto, re.IGNORECASE)
        
        # Convertir a conjunto para eliminar duplicados, luego a lista
        return list(set(tecnologias))
    
    def extraer_salario_texto(self, texto):
        """
        Extrae menciones de salario del texto 
        
        Args:
            texto (str): Texto de la descripción
            
        Returns:
            str: Rango salarial encontrado o None
        """
        if not isinstance(texto, str) or pd.isna(texto):
            return None
        
        # Patrón para buscar rangos salariales
        patrones = [
            r'\$?(\d{2,3}(?:,\d{3})?(?:k|K)?)\s*[-–]\s*\$?(\d{2,3}(?:,\d{3})?(?:k|K)?)',
            r'(?:USD|usd)?\s*(\d{2,3}(?:,\d{3})?(?:k|K)?)\s*[-–]\s*(\d{2,3}(?:,\d{3})?(?:k|K)?)',
            r'(\d{2,3}(?:,\d{3})?(?:k|K)?)\s*-\s*(\d{2,3}(?:,\d{3})?(?:k|K)?)'
        ]
        
        for patron in patrones:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                return f"${match.group(1)} - ${match.group(2)}"
        
        return None