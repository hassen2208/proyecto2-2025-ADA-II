import customtkinter as ctk
import os
import subprocess
from tkinter import filedialog
from PIL import Image, ImageTk
import time
import re
from graficador import graficar_extremismo

# Inicializar la app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("1400x600")
root.title("Reducción de Polarización - Grupo 11")

entradas_disponibles = []
entrada_seleccionada = None
contenido_dzn = ""

def ruta_relativa(desde_gui, destino):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", destino))

def cargar_archivo(prueba):
    global contenido_dzn
    try:
        carpeta_pruebas = ruta_relativa(__file__, "BateriaPruebas")
        ruta_prueba = os.path.join(carpeta_pruebas, prueba)
        resultado_area.insert(ctk.END, f"Buscando archivo en: {ruta_prueba}\n")

        with open(ruta_prueba, "r") as archivo:
            datos_entrada = [line.strip() for line in archivo.readlines()]
            contenido_dzn = txt_to_dzn(datos_entrada, prueba.replace('.txt', '.dzn'))
            resultado_area.insert(ctk.END, f"Archivo '{prueba}' transformado y guardado en DatosProyecto/\n")
            tabla = dibujar_tabla(datos_entrada)
            parametros_area.delete("0.0", "end")
            parametros_area.insert(ctk.END, f"\n{tabla}\n")
    except Exception as e:
        resultado_area.insert(ctk.END, f"Error al cargar entrada: {str(e)}\n")

def txt_to_dzn(datos, nombre_dzn):
    try:
        n, m, p, v, ce = datos[0:5]
        matriz_c = ",\n".join(datos[5:5 + int(m)])
        ct = datos[5 + int(m)].replace(";", "")
        maxM = datos[6 + int(m)].replace(";", "")

        contenido = (
            f"n = {n};\n"
            f"m = {m};\n"
            f"p = [{p}];\n"
            f"v = [{v}];\n"
            f"c = array2d(1..{m}, 1..{m}, [\n{matriz_c}\n]);\n"
            f"ce = [{ce}];\n"
            f"ct = {ct};\n"
            f"maxM = {maxM};\n"
        )

        carpeta_salida = ruta_relativa(__file__, "DatosProyecto")
        os.makedirs(carpeta_salida, exist_ok=True)
        ruta_salida = os.path.join(carpeta_salida, nombre_dzn)
        with open(ruta_salida, "w") as archivo:
            archivo.write(contenido)
        return contenido
    except Exception as e:
        resultado_area.insert(ctk.END, f"Error en la transformación: {str(e)}\n")
        return ""

def dibujar_tabla(datos):
    n, m, p, v, ce = datos[0:5]
    matriz_costos = datos[5:5+int(m)]
    max_movimientos = datos[-1]

    tabla = "+" + "-"*130 + "+\n"
    tabla += f"|{'':<62} Parámetros de entrada {'':<68}|\n"
    tabla += "+" + "-"*130 + "+\n"
    tabla += f" Total personas:              {n:<23} \n"
    tabla += f" Cantidad de opiniones: {m:<23} \n"
    tabla += f" Cantidad de Personas por opinion: [{p}]\n"
    tabla += f" Valor por opinion:  [{v}] \n"
    tabla += f" Costo extra:            [{ce}] \n"
    matriz_str = f'\n{" ":<34} '.join(matriz_costos)
    tabla += f" Matriz de costos:  [{matriz_str}] \n"
    tabla += f" Cantidad maxima de movimientos: {max_movimientos} \n"
    tabla += " -" + "-"*130 + "- \n"
    return tabla

def ejecutar_minimizacion():
    global contenido_dzn
    try:
        resultado_area.delete("0.0", "end")  # Limpiar resultados anteriores
        label_imagen.configure(image=None)
        label_imagen.image = None

        modelo_path = ruta_relativa(__file__, "Proyecto.mzn")
        archivo_dzn_path = os.path.join(ruta_relativa(__file__, "DatosProyecto"), entrada_seleccionada.replace('.txt', '.dzn'))
        comando = f'minizinc --solver gecode --all-solutions "{modelo_path}" "{archivo_dzn_path}"'

        start = time.time()
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        end = time.time()

        if resultado.returncode == 0:
            solucion = resultado.stdout.replace("Ã³", "ó").replace("----------", "-"*132).replace("==========", "="*75)
            valores = re.findall(r"Extremismo total: ([0-9.,]+)", solucion)
            mensaje = ""
            if valores:
                valores_float = [float(v.replace(",", ".")) for v in valores]
                minimo = min(valores_float)
                mensaje = f"\n✅ Valor mínimo de extremismo total encontrado: {minimo:.3f}\n"

                # Graficar
                img = graficar_extremismo(valores_float)
                img = img.resize((500, 200))
                img_tk = ImageTk.PhotoImage(img)
                label_imagen.configure(image=img_tk)
                label_imagen.image = img_tk

                frame_entrada_y_resultado.grid_columnconfigure(0, weight=1)  # Parámetros
                frame_entrada_y_resultado.grid_columnconfigure(1, weight=4)  # Resultados + gráfica

            else:
                mensaje = "\n⚠️ No se encontró ningún valor de extremismo total.\n"

                frame_entrada_y_resultado.grid_columnconfigure(0, weight=1)
                frame_entrada_y_resultado.grid_columnconfigure(1, weight=2)

            titulo = "+" + "-"*130 + "+\n"
            titulo += f'|{" ":<40} Resultado de la minimización para "{entrada_seleccionada}" {" ":<43}|\n'
            titulo += "+" + "-"*130 + "+\n"
            resultado_area.insert(ctk.END, f"{titulo}\n{solucion}{mensaje}  Tiempo de ejecución: {end - start:.3f} s\n")
        else:
            resultado_area.insert(ctk.END, f"❌ Error en la minimización: {resultado.stderr}\n")
    except Exception as e:
        resultado_area.insert(ctk.END, f"⚠️ Error al ejecutar MiniZinc: {str(e)}\n")

def obtener_entradas():
    global entradas_disponibles
    carpeta_pruebas = ruta_relativa(__file__, "BateriaPruebas")
    try:
        entradas_disponibles = [f for f in os.listdir(carpeta_pruebas) if f.endswith('.txt')]
        entradas_disponibles.sort(key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else float('inf'))
    except FileNotFoundError:
        entradas_disponibles = ["Carpeta 'BateriaPruebas' no encontrada"]

def actualizar_entradas_menu():
    obtener_entradas()
    opciones_pruebas.configure(values=entradas_disponibles)

def seleccionar_entrada(entrada):
    global entrada_seleccionada
    entrada_seleccionada = entrada
    resultado_area.insert(ctk.END, f"Entrada seleccionada: {entrada}\n")
    cargar_archivo(entrada)
    btn_ejecutar_minimizacion.configure(state="normal")

def limpiar():
    resultado_area.delete("0.0", "end")
    parametros_area.delete("0.0", "end")
    opciones_pruebas.set("Seleccionar entrada")
    btn_ejecutar_minimizacion.configure(state="disabled")
    label_imagen.configure(image=None)
    label_imagen.image = None

# --- Interfaz gráfica ---
barra_superior = ctk.CTkFrame(root, height=105, corner_radius=0, fg_color="#5B9BD5")
barra_superior.grid(row=0, column=0, columnspan=3, sticky="ew")
titulo_label = ctk.CTkLabel(barra_superior, text="MINIMIZACIÓN DE LA POLARIZACIÓN", font=("Roboto", 20), text_color="black")
titulo_label.place(relx=0.5, rely=0.5, anchor="center")

frame_entrada_y_resultado = ctk.CTkFrame(root, fg_color="#F2F2F2")
frame_entrada_y_resultado.grid(row=1, column=0, columnspan=3, rowspan=2, sticky="nsew", padx=10, pady=10)
frame_entrada_y_resultado.grid_columnconfigure(0, weight=1)  # Parámetros
frame_entrada_y_resultado.grid_columnconfigure(1, weight=2)  # Resultados + gráfica
frame_entrada_y_resultado.grid_rowconfigure(0, weight=1)

frame_parametros = ctk.CTkFrame(frame_entrada_y_resultado, fg_color="#F2F2F2")
frame_parametros.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
frame_parametros.grid_columnconfigure(0, weight=1)
frame_parametros.grid_rowconfigure(1, weight=1)
ctk.CTkLabel(frame_parametros, text="Parámetros de entrada", font=("Roboto", 20), text_color="black").grid(row=0, column=0, pady=10)
parametros_area = ctk.CTkTextbox(frame_parametros, font=("Roboto", 12), text_color="white")
parametros_area.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

frame_resultado = ctk.CTkFrame(frame_entrada_y_resultado, fg_color="#A8D5BA")
frame_resultado.grid_propagate(False)
frame_resultado.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
frame_resultado.grid_columnconfigure(0, weight=4)
frame_resultado.grid_columnconfigure(1, weight=3)
frame_resultado.grid_rowconfigure(1, weight=1)
ctk.CTkLabel(frame_resultado, text="Resultado de la ejecución", font=("Roboto", 20), text_color="black").grid(row=0, column=0, columnspan=2, pady=10)

resultado_area = ctk.CTkTextbox(frame_resultado, font=("Roboto", 12), text_color="white", wrap="word")
resultado_area.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

label_imagen = ctk.CTkLabel(frame_resultado, text="")
label_imagen.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")


frame_contenido = ctk.CTkFrame(root, fg_color="#F2F2F2")
frame_contenido.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
frame_contenido.grid_columnconfigure(0, weight=1)
ctk.CTkLabel(frame_contenido, text="Seleccione una entrada a minimizar", font=("Roboto", 20), text_color="black").grid(row=0, column=0, pady=5)

frame_menus_botones = ctk.CTkFrame(frame_contenido, fg_color="#F2F2F2")
frame_menus_botones.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
frame_menus_botones.grid_columnconfigure((0, 1, 2, 3), weight=1)

opciones_pruebas = ctk.CTkOptionMenu(frame_menus_botones, values=["Seleccionar entrada"], command=seleccionar_entrada)
opciones_pruebas.grid(row=0, column=0, padx=10, sticky="ew")

btn_ejecutar_minimizacion = ctk.CTkButton(frame_menus_botones, text="Minimizar", state="disabled", command=ejecutar_minimizacion)
btn_ejecutar_minimizacion.grid(row=0, column=2, padx=10, sticky="ew")

btn_limpiar = ctk.CTkButton(frame_menus_botones, text="Limpiar", command=limpiar)
btn_limpiar.grid(row=0, column=3, padx=10, sticky="ew")

root.grid_columnconfigure((0, 1, 2), weight=1)
root.grid_rowconfigure((1, 2), weight=1)
root.grid_rowconfigure(3, weight=0)

actualizar_entradas_menu()
root.mainloop()
