import matplotlib.pyplot as plt

class VisualizadorGraficos:

    def __init__(self, df):
        self.df = df

    def grafico_tipos_empleo(self):
        tipos = self.df["tipo_empleo_simple"].value_counts()

        ax = tipos.plot(
            kind="bar",
            figsize=(8, 5)
        )

        plt.title("Distribución de los tipos de empleo")
        plt.xlabel("Tipo de empleo")
        plt.ylabel("Cantidad de ofertas")
        plt.xticks(rotation=0)

        # Mostrar el valor encima de cada barra
        for barra in ax.patches:
            ax.annotate(
                str(int(barra.get_height())),
                (barra.get_x() + barra.get_width()/2,
                 barra.get_height()),
                ha="center",
                va="bottom"
            )

        plt.show()


