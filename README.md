# 📊 Reducción de la Polarización en una Población

## 👥 Integrantes

- Alejandro Rodriguez Marulanda – 202042954  
  alejandro.marulanda@correounivalle.edu.co
- Hassen David Ortiz Alvarez – 202177273  
  hassen.ortiz@correounivalle.edu.co
- Heidy Mina Garcia – 201931720  
  heidy.mina@correounivalle.edu.co
- Wilson Andrés Mosquera Zapata – 202182116  
  mosquera.wilson@correounivalle.edu.co  

## 📚 Materia

Analisis y Diseños de Algoritmos II  
Universidad del Valle – 2025-I

## 📌 Descripción del Proyecto

Este proyecto implementa un modelo matemático de optimización para reducir la **polarización de opiniones** en una población.  
Se utilizó el lenguaje de modelado **MiniZinc** y se creó una interfaz gráfica (GUI) con **Python + CustomTkinter** que permite:

- Cargar archivos de entrada `.txt` con los parámetros del problema.
- Visualizar los parámetros de entrada y los resultados de la minimización.
- Ejecutar el modelo MiniZinc directamente desde la GUI.
- Mostrar múltiples soluciones y destacar la de menor extremismo.

## 📁 Estructura del Proyecto


```
📦 Proyecto/
├── 📄 main.py                  # Interfaz gráfica de usuario (GUI)
├── 📄 Proyecto.mzn             # Modelo de optimización en MiniZinc
├── 📂 BateriaPruebas/          # Archivos de entrada de prueba (.txt)
│   ├── Prueba1.txt
│   ├── Prueba2.txt
│   └── ...
├── 📂 DatosProyecto/           # Archivos .dzn generados desde los .txt
│   ├── Prueba1.dzn
│   ├── Prueba2.dzn
│   └── ...
└── 📄 README.md               
``` 


## ✅ Requisitos

- Python 3.10 o superior
- MiniZinc instalado y agregado al PATH: [https://www.minizinc.org/software.html](https://www.minizinc.org/software.html)
- Paquetes de Python: pip install customtkinter pillow

  
##  Ejecución de la aplicación

1. Asegúrate de tener MiniZinc instalado y accesible desde la terminal o consola.
2. Clona este repositorio o descarga los archivos del proyecto.
3. Ejecuta la aplicación desde el terminal:  python main.py
4. Desde la interfaz:
-Selecciona una entrada desde el menú desplegable.
-Haz clic en "Minimizar" para ejecutar el modelo.
-Visualiza los parámetros y resultados en sus respectivas secciones.:



