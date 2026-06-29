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
     # ========== MÉTODOS DE EXTRACCIÓN CON REGEX ==========
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
    
    def extraer_modalidad(self, texto):
        """
        Extrae la modalidad de trabajo del texto 
        
        Args:
            texto (str): Texto de la descripción
            
        Returns:
            str: Modalidad encontrada o 'No especificado'
        """
        if not isinstance(texto, str) or pd.isna(texto):
            return 'No especificado'
        
        # Patrón para buscar modalidades
        patron = r'\b(Remote|Hybrid|Onsite|Presencial|Remoto|Híbrido|Hibrido|Home Office|Teletrabajo)\b'
        
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            # Convertir a formato consistente
            modalidad = match.group(1).lower()
            if modalidad in ['remote', 'remoto', 'home office', 'teletrabajo']:
                return 'Remoto'
            elif modalidad in ['hybrid', 'híbrido', 'hibrido']:
                return 'Híbrido'
            elif modalidad in ['onsite', 'presencial']:
                return 'Presencial'
        
        return 'No especificado'
    
    def extraer_nivel_experiencia(self, texto):
        """
        Extrae el nivel de experiencia requerido 
        
        Args:
            texto (str): Texto de la descripción
            
        Returns:
            str: Nivel de experiencia o 'No especificado'
        """
        if not isinstance(texto, str) or pd.isna(texto):
            return 'No especificado'
        
        patron = r'\b(Senior|Junior|Entry Level|Mid-Level|Lead|Principal|Staff|Intern|Trainee|Associate)\b'
        
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            return match.group(1).title()
        
        return 'No especificado'
    
    def extraer_años_experiencia(self, texto):
        """
        Extrae los años de experiencia requeridos usando regex
        
        Args:
            texto (str): Texto de la descripción
            
        Returns:
            str: Años de experiencia o None
        """
        if not isinstance(texto, str) or pd.isna(texto):
            return None
        
        patron = r'(\d+)\+?\s*(?:-?\s*(\d+))?\s*(?:years|años|yr|yrs)'
        
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            if match.group(2):  # Rango: X-Y años
                return f"{match.group(1)}-{match.group(2)} años"
            return f"{match.group(1)}+ años"  # X+ años
        
        return None
    
    # ========== MÉTODO PRINCIPAL ==========

    def procesar_dataset(self):
        """
        Aplica todas las extracciones al dataset y agrega nuevas columnas
        """
        if self.df.empty:
            print("No hay datos para procesar")
            return self.df
        
        print("\nEXTRACCIÓN CON EXPRESIONES REGULARES")
        print("=" * 50)
        
        # Aplicar cada extracción a la columna 'description'
        print("   Extrayendo tecnologías...")
        self.df['tecnologias'] = self.df['description'].apply(self.extraer_tecnologias)
        
        print("   Extrayendo salarios mencionados...")
        self.df['salario_mencionado'] = self.df['description'].apply(self.extraer_salario_texto)
        
        print("   Extrayendo modalidad de trabajo...")
        self.df['modalidad'] = self.df['description'].apply(self.extraer_modalidad)
        
        print("   Extrayendo nivel de experiencia...")
        self.df['nivel_experiencia'] = self.df['description'].apply(self.extraer_nivel_experiencia)
        
        print("   Extrayendo años de experiencia...")
        self.df['anos_experiencia'] = self.df['description'].apply(self.extraer_años_experiencia)
        
        # Contar cuántas ofertas tienen cada extracción
        print("\nRESULTADOS DE EXTRACCIÓN:")
        print(f"   - Ofertas con tecnologías: {self.df['tecnologias'].apply(len).gt(0).sum()}")
        print(f"   - Ofertas con salario mencionado: {self.df['salario_mencionado'].notna().sum()}")
        print(f"   - Ofertas con modalidad: {self.df['modalidad'].ne('No especificado').sum()}")
        print(f"   - Ofertas con nivel experiencia: {self.df['nivel_experiencia'].ne('No especificado').sum()}")
        print(f"   - Ofertas con años experiencia: {self.df['anos_experiencia'].notna().sum()}")
        
        print("\nEXTRACCIÓN COMPLETADA")
        return self.df
    
    def guardar_csv(self, nombre="datos/procesados/ofertas_con_regex.csv"):
        """
        Guarda el dataset con las nuevas columnas
        """
        if self.df.empty:
            print("No hay datos para guardar")
            return
        
        # Crear la carpeta si no existe
        os.makedirs(os.path.dirname(nombre), exist_ok=True)
        
        self.df.to_csv(nombre, index=False, encoding='utf-8-sig')
        print(f"Datos guardados en: {nombre}")
        print(f" Total de registros: {len(self.df)}")
        print(f" Nuevas columnas agregadas: tecnologias, salario_mencionado, modalidad, nivel_experiencia, anos_experiencia")
    
    def mostrar_ejemplos(self):
        """
        Muestra ejemplos de extracción para verificar que funciona
        """
        if self.df.empty:
            print("No hay datos para mostrar")
            return
        
        print("\nEJEMPLOS DE EXTRACCIÓN")
        print("=" * 60)
        
        # Tomar 3 ofertas con descripción larga
        ejemplos = self.df[self.df['description'].str.len() > 100].head(3)
        
        for idx, row in ejemplos.iterrows():
            print(f"\n {row['title']} - {row['companyName']}")
            print(f"Ubicación: {row['ubicacion']}")
            print(f"Modalidad: {row['modalidad']}")
            print(f"Tecnologías: {', '.join(row['tecnologias']) if row['tecnologias'] else 'No especificadas'}")
            print(f"Salario mencionado: {row['salario_mencionado'] or 'No especificado'}")
            print(f"Nivel: {row['nivel_experiencia']}")
            print(f" Experiencia: {row['anos_experiencia'] or 'No especificado'}")
            print("-" * 40)


    def ejecutar_extraccion(self):
        """
        Método principal que ejecuta todo el flujo de extracción 
        """
        print("INICIANDO EXTRACCIÓN CON REGEX")
        print("=" * 50)
        
        self.procesar_dataset()
        self.guardar_csv()
        self.mostrar_ejemplos()
        
        print("\nEXTRACCIÓN COMPLETADA EXITOSAMENTE")
        return self.df


# --- EJECUCIÓN ---
if __name__ == "__main__":
    extractor = ExtractorRegex("datos/procesados/ofertas_limpias.csv")
    df_enriquecido = extractor.ejecutar_extraccion()