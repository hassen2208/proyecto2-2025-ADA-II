import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

def graficar_extremismo(valores_float):
    """Genera una imagen PIL de la gráfica de extremismo total"""
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.plot(range(1, len(valores_float) + 1), valores_float, marker="o", color="green")
    ax.set_title("Evolución del extremismo total")
    ax.set_xlabel("Solución")
    ax.set_ylabel("Extremismo")
    ax.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img = Image.open(buffer)
    plt.close(fig)
    return img
