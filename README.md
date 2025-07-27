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
 
Link a la sustentación: https://drive.google.com/file/d/1WB1iNVauIkbX9pjOQYNUV8x234TpvY0p/view?usp=sharing

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
├── 📁 BateriaPruebas
│   └── Archivos .txt con pruebas genéricas para evaluar el modelo.
│       Estas pruebas fueron suministradas como parte de la batería estándar.
│
├── 📁 DatosProyecto
│   └── Archivos .dzn convertidos a partir de las pruebas .txt oficiales.
│       Se usan como entrada del modelo en MiniZinc para pruebas reales.
│
├── 📁 MisInstancias
│   └── Pruebas personalizadas en formato .dzn creadas por el equipo
│       para validar situaciones específicas del modelo.
│
├── 📁 ProyectoGUIFuentes
│   ├── main.py          → Código principal de la interfaz gráfica.
│   └── graficador.py    → Funciones complementarias para visualización y manejo de resultados.
│
├── 📄 Informe_Proyecto_II_ADA_II_2025_Grupo_11.pdf
│
│
├── 📄 Proyecto.mzn
│   → Archivo principal que contiene el modelo matemático implementado en MiniZinc.
│     Incluye parámetros, variables, restricciones y la función objetivo para minimizar el extremismo.
│
└── 📄 README.md
    → Este documento. Explica el propósito, funcionamiento y estructura del proyecto.
             
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



