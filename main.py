#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Carrusel Multimedia - Aplicación para mostrar fotos y videos desde USB
Desarrollado para Raspberry Pi 3
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importación simplificada usando el __init__.py
from src import CarruselApp


def main():
    """Función principal de la aplicación"""
    try:
        # Crear ventana principal
        root = tk.Tk()

        # Configurar para cerrar con Escape
        root.bind('<Escape>', lambda e: root.quit())

        # Inicializar aplicación
        app = CarruselApp(root)

        # Iniciar bucle principal
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
