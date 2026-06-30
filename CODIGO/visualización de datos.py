import os
import ast
import pandas as pd
import matplotlib.pyplot as plt

# ===============================
# CONFIGURACIÓN
# ===============================

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (10,6)
plt.rcParams["font.size"] = 11

RUTA_CSV = "datos/procesados/ofertas_con_regex.csv"
CARPETA_GRAFICOS = "graficos"

os.makedirs(CARPETA_GRAFICOS, exist_ok=True)

# ===============================
# CARGAR DATOS
# ===============================

df = pd.read_csv(RUTA_CSV, encoding="utf-8-sig")

print("Datos cargados correctamente")
print(f"Registros: {len(df)}")

# =============================================
# CONVERTIR LA COLUMNA TECNOLOGIAS A LISTA
# =============================================

def convertir_lista(valor):

    if pd.isna(valor):
        return []

    try:
        return ast.literal_eval(valor)
    except:
        return []

df["tecnologias"] = df["tecnologias"].apply(convertir_lista)

# =====================================================
# GRAFICO 1
# TOP EMPRESAS CON MEJOR SALARIO PROMEDIO
# =====================================================

salarios = (
    df[df["salario_promedio"].notna()]
    .groupby("companyName")["salario_promedio"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(11,6))
salarios.sort_values().plot(kind="barh")

plt.title("Top 10 empresas con mayor salario promedio")
plt.xlabel("Salario promedio")
plt.ylabel("Empresa")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CARPETA_GRAFICOS,
        "salarios_empresa.png"
    ),
    dpi=300
)

plt.close()

# =====================================================
# GRAFICO 2
# DISTRIBUCIÓN DE MODALIDADES
# =====================================================

modalidades = df["tipo_empleo_simple"].value_counts()

plt.figure(figsize=(8,8))

plt.pie(
    modalidades,
    labels=modalidades.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Distribución de modalidades de empleo")

plt.savefig(
    os.path.join(
        CARPETA_GRAFICOS,
        "modalidades.png"
    ),
    dpi=300
)

plt.close()

# =====================================================
# GRAFICO 3
# TECNOLOGÍAS MÁS DEMANDADAS
# =====================================================

lista_tecnologias = []

for tecnologias in df["tecnologias"]:
    lista_tecnologias.extend(tecnologias)

conteo = (
    pd.Series(lista_tecnologias)
    .value_counts()
    .head(15)
)

plt.figure(figsize=(12,6))

conteo.sort_values().plot(kind="barh")

plt.title("Tecnologías más demandadas")
plt.xlabel("Cantidad de ofertas")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CARPETA_GRAFICOS,
        "tecnologias.png"
    ),
    dpi=300
)

plt.close()

# =====================================================
# GRAFICO 4
# NIVEL DE EXPERIENCIA
# =====================================================

niveles = df["nivel_experiencia"].value_counts()

plt.figure(figsize=(9,5))

niveles.plot(kind="bar")

plt.title("Nivel de experiencia requerido")
plt.xlabel("Nivel")
plt.ylabel("Cantidad")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CARPETA_GRAFICOS,
        "niveles_experiencia.png"
    ),
    dpi=300
)

plt.close()

# =====================================================
# GRAFICO 5
# HEATMAP TECNOLOGÍA VS MODALIDAD
# =====================================================

datos = []

for _, fila in df.iterrows():

    modalidad = fila["tipo_empleo_simple"]

    for tecnologia in fila["tecnologias"]:

        datos.append(
            {
                "Tecnologia": tecnologia,
                "Modalidad": modalidad
            }
        )

heat = pd.DataFrame(datos)

if len(heat) > 0:

    tabla = pd.crosstab(
        heat["Tecnologia"],
        heat["Modalidad"]
    )

    tabla = tabla.loc[
        tabla.sum(axis=1)
        .sort_values(ascending=False)
        .head(15)
        .index
    ]

    plt.figure(figsize=(10,8))

    plt.imshow(
        tabla,
        aspect="auto"
    )

    plt.xticks(
        range(len(tabla.columns)),
        tabla.columns,
        rotation=45
    )

    plt.yticks(
        range(len(tabla.index)),
        tabla.index
    )

    plt.colorbar(label="Cantidad")

    plt.title("Heatmap Tecnologías vs Modalidad")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CARPETA_GRAFICOS,
            "heatmap_tecnologias_modalidad.png"
        ),
        dpi=300
    )

    plt.close()

print("\n=======================================")
print("GRÁFICOS GENERADOS CORRECTAMENTE")
print("=======================================")

print("✔ salarios_empresa.png")
print("✔ modalidades.png")
print("✔ tecnologias.png")
print("✔ niveles_experiencia.png")
print("✔ heatmap_tecnologias_modalidad.png")
