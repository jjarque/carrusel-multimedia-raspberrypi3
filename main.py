#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src import CarruselApp

def main():
    try:
        root = tk.Tk()
        root.bind('<Escape>', lambda e: root.quit())
        app = CarruselApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
