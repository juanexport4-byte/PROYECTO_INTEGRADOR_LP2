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

    def limpiar_datos(self):
        """
        Realiza la limpieza completa del dataset
        """
        if self.df.empty:
            print("No hay datos para limpiar")
            return self.df
        
        print("\nINICIANDO LIMPIEZA DE DATOS")
        print("=" * 40)
        
        # 1. Eliminar duplicados
        registros_antes = len(self.df)
        self.df = self.df.drop_duplicates(subset=['title', 'companyName'])
        print(f"   → Duplicados eliminados: {registros_antes - len(self.df)}")
        
        # 2. Manejar valores nulos
        self.df['description'] = self.df['description'].fillna('')
        self.df['minSalary'] = self.df['minSalary'].fillna(0)
        self.df['maxSalary'] = self.df['maxSalary'].fillna(0)
        self.df['currency'] = self.df['currency'].fillna('No especificado')
        self.df['employmentType'] = self.df['employmentType'].fillna('No especificado')
        
        # 3. Limpiar descripciones (eliminar HTML)
        self.df['description'] = self.df['description'].str.replace(r'<[^<>]*>', '', regex=True)
        self.df['description'] = self.df['description'].str.replace(r'\s+', ' ', regex=True)
        self.df['description'] = self.df['description'].str.strip()
        
        # 4. Convertir fechas
        self.df['pubDate'] = pd.to_datetime(self.df['pubDate'], unit='ms')
        
        # 5. Extraer ubicaciones
        if 'locationRestrictions' in self.df.columns:
            self.df['ubicacion'] = self.df['locationRestrictions'].apply(
                lambda x: ', '.join(x) if isinstance(x, list) and x else 'Global'
            )
        else:
            self.df['ubicacion'] = 'Global'
        
        # 6. Extraer seniority
        if 'seniority' in self.df.columns:
            self.df['seniority'] = self.df['seniority'].apply(
                lambda x: ', '.join(x) if isinstance(x, list) and x else 'No especificado'
            )
        else:
            self.df['seniority'] = 'No especificado'
        
        # 7. Crear rango salarial formateado
        self.df['rango_salarial'] = self.df.apply(
            lambda row: f"{row['minSalary']} - {row['maxSalary']} {row['currency']}" 
            if row['minSalary'] > 0 and row['maxSalary'] > 0 else 'No especificado',
            axis=1
        )
        
        # 8. Crear salario promedio
        self.df['salario_promedio'] = self.df.apply(
            lambda row: (row['minSalary'] + row['maxSalary']) / 2
            if row['minSalary'] > 0 and row['maxSalary'] > 0 else None,
            axis=1
        )
        
        # 9. Tipo de empleo simplificado
        self.df['tipo_empleo_simple'] = self.df['employmentType'].apply(
            lambda x: 'Full Time' if 'full' in x.lower() else 
                     'Part Time' if 'part' in x.lower() else 
                     'Contract' if 'contract' in x.lower() else 
                     'Freelance' if 'freelance' in x.lower() else 'Otro'
        )
        
        print(f"   → Datos limpios: {len(self.df)} registros")
        print("LIMPIEZA COMPLETADA")
        return self.df

    def guardar_csv(self, nombre="datos/procesados/ofertas_limpias.csv"):
        """
        Guarda el DataFrame limpio en un archivo CSV
        """
        if self.df.empty:
            print("No hay datos para guardar")
            return
        
        # Crear la carpeta si no existe
        os.makedirs(os.path.dirname(nombre), exist_ok=True)
        
        self.df.to_csv(nombre, index=False, encoding='utf-8-sig')
        print(f"Datos guardados en: {nombre}")
        print(f" Total de registros: {len(self.df)}")

    def mostrar_resumen(self):
        """
        Muestra un resumen estadístico del dataset
        """
        if self.df.empty:
            print("No hay datos para mostrar")
            return
        
        print("\n" + "=" * 50)
        print("RESUMEN DEL DATASET")
        print("=" * 50)
        
        print(f"📌 Total de ofertas: {len(self.df)}")
        print(f"📌 Columnas: {len(self.df.columns)}")
        
        print("\nTipos de empleo:")
        print(self.df['tipo_empleo_simple'].value_counts())
        
        print("\nTop 5 empresas con más ofertas:")
        print(self.df['companyName'].value_counts().head())
        
        salarios_validos = self.df[self.df['salario_promedio'].notna()]
        if not salarios_validos.empty:
            print(f"\n Salarios promedio:")
            print(f"   Mínimo: ${salarios_validos['salario_promedio'].min():,.0f}")
            print(f"   Promedio: ${salarios_validos['salario_promedio'].mean():,.0f}")
            print(f"   Máximo: ${salarios_validos['salario_promedio'].max():,.0f}")

    def ejecutar_procesamiento(self):
        """
        Método principal que ejecuta todo el flujo de procesamiento
        """
        print("INICIANDO PROCESAMIENTO DE DATOS")
        print("=" * 50)
        
        self.limpiar_datos()
        self.guardar_csv()
        self.mostrar_resumen()
        
        print("\nPROCESAMIENTO COMPLETADO EXITOSAMENTE")
        return self.df


if __name__ == "__main__":
    procesador = ProcesadorDatos("datos/crudos/ofertas_hiringcafe.json")
    df_limpio = procesador.ejecutar_procesamiento()
