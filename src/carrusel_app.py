import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading
import time
from media_player import MediaPlayer
from usb_detector import USBDetector
from config.settings import AppSettings


class CarruselApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carrusel Multimedia v1.0")
        self.root.geometry("1200x800")

        # Variables de control
        self.archivos_multimedia = []
        self.indice_actual = 0
        self.reproduciendo = False
        self.hilo_carrusel = None

        # Configuraciones
        self.settings = AppSettings()

        # Componentes
        self.media_player = MediaPlayer(self)
        self.usb_detector = USBDetector(self)

        # Crear interfaz
        self.crear_interfaz()

        # Detectar USB al inicio
        self.detectar_usb()

    def crear_interfaz(self):
        """Crea la interfaz gráfica principal"""
        # Frame superior para controles
        self.frame_control = tk.Frame(self.root, height=250, bg='lightgray', relief='raised', bd=2)
        self.frame_control.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.frame_control.pack_propagate(False)

        # Frame inferior para visualización
        self.frame_visualizacion = tk.Frame(self.root, bg='black', relief='sunken', bd=2)
        self.frame_visualizacion.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Crear controles
        self.crear_controles()

        # Área de visualización
        self.label_multimedia = tk.Label(
            self.frame_visualizacion,
            bg='black',
            text="Conecta un USB con fotos y videos\nLuego presiona 'Detectar USB'",
            fg='white',
            font=('Arial', 16)
        )
        self.label_multimedia.pack(expand=True, fill=tk.BOTH)

    def crear_controles(self):
        """Crea los controles de la aplicación"""
        # Frame para botones principales
        frame_botones = tk.Frame(self.frame_control, bg='lightgray')
        frame_botones.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Botones de control
        self.btn_detectar = tk.Button(
            frame_botones,
            text="🔍 Detectar USB",
            command=self.detectar_usb,
            bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
            width=15, height=2
        )
        self.btn_detectar.pack(side=tk.LEFT, padx=5)

        self.btn_iniciar = tk.Button(
            frame_botones,
            text="▶️ Iniciar Carrusel",
            command=self.iniciar_carrusel,
            bg='#2196F3', fg='white', font=('Arial', 12, 'bold'),
            width=15, height=2
        )
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)

        self.btn_pausar = tk.Button(
            frame_botones,
            text="⏸️ Pausar",
            command=self.pausar_carrusel,
            bg='#FF9800', fg='white', font=('Arial', 12, 'bold'),
            width=15, height=2
        )
        self.btn_pausar.pack(side=tk.LEFT, padx=5)

        self.btn_limpiar = tk.Button(
            frame_botones,
            text="🗑️ Limpiar Lista",
            command=self.limpiar_lista,
            bg='#F44336', fg='white', font=('Arial', 12, 'bold'),
            width=15, height=2
        )
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)

        # Frame para configuraciones
        frame_config = tk.Frame(self.frame_control, bg='lightgray')
        frame_config.pack(side=tk.TOP, fill=tk.X, pady=5)

        tk.Label(frame_config, text="Tiempo por imagen (segundos):", bg='lightgray', font=('Arial', 10)).pack(
            side=tk.LEFT, padx=5)

        self.tiempo_var = tk.StringVar(value=str(self.settings.tiempo_imagen))
        self.spin_tiempo = tk.Spinbox(
            frame_config,
            from_=1, to=30,
            textvariable=self.tiempo_var,
            width=5, font=('Arial', 10)
        )
        self.spin_tiempo.pack(side=tk.LEFT, padx=5)

        # Lista de archivos
        frame_lista = tk.Frame(self.frame_control, bg='lightgray')
        frame_lista.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=5)

        tk.Label(frame_lista, text="Archivos detectados:", bg='lightgray', font=('Arial', 11, 'bold')).pack(anchor=tk.W,
                                                                                                            padx=5)

        # Listbox con scrollbar
        frame_listbox = tk.Frame(frame_lista, bg='lightgray')
        frame_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.listbox = tk.Listbox(frame_listbox, height=6, font=('Arial', 9))
        scrollbar = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Contador de archivos
        self.label_contador = tk.Label(frame_lista, text="Archivos: 0", bg='lightgray', font=('Arial', 10))
        self.label_contador.pack(anchor=tk.W, padx=5)

    def detectar_usb(self):
        """Detecta dispositivos USB y carga archivos multimedia"""
        self.usb_detector.detectar_dispositivos()

    def iniciar_carrusel(self):
        """Inicia la reproducción del carrusel"""
        if not self.archivos_multimedia:
            messagebox.showwarning("Sin archivos",
                                   "No hay archivos multimedia para reproducir.\nConecta un USB y presiona 'Detectar USB'.")
            return

        if self.reproduciendo:
            messagebox.showinfo("Ya reproduciendo", "El carrusel ya está en ejecución.")
            return

        self.reproduciendo = True
        self.settings.tiempo_imagen = int(self.tiempo_var.get())

        # Iniciar en hilo separado
        self.hilo_carrusel = threading.Thread(target=self._bucle_carrusel, daemon=True)
        self.hilo_carrusel.start()

        messagebox.showinfo("Carrusel iniciado", f"Reproduciendo {len(self.archivos_multimedia)} archivos.")

    def pausar_carrusel(self):
        """Pausa o reanuda la reproducción"""
        self.reproduciendo = not self.reproduciendo
        texto = "⏸️ Pausar" if self.reproduciendo else "▶️ Reanudar"
        self.btn_pausar.config(text=texto)

    def limpiar_lista(self):
        """Limpia la lista de archivos multimedia"""
        self.reproduciendo = False
        self.archivos_multimedia.clear()
        self.listbox.delete(0, tk.END)
        self.indice_actual = 0
        self.actualizar_contador()
        self.label_multimedia.config(
            text="Lista limpiada\nConecta un USB y presiona 'Detectar USB'",
            image=""
        )
        self.media_player.detener_video()

    def _bucle_carrusel(self):
        """Bucle principal del carrusel (ejecuta en hilo separado)"""
        while self.reproduciendo and self.archivos_multimedia:
            if self.indice_actual >= len(self.archivos_multimedia):
                self.indice_actual = 0

            archivo_actual = self.archivos_multimedia[self.indice_actual]

            # Programar actualización en hilo principal
            self.root.after(0, self.media_player.mostrar_archivo, archivo_actual)

            # Esperar tiempo configurado
            tiempo_espera = self.settings.tiempo_imagen if self.media_player.es_imagen(archivo_actual) else 0

            contador = 0
            while contador < tiempo_espera and self.reproduciendo:
                time.sleep(1)
                contador += 1

            self.indice_actual += 1

    def actualizar_lista_archivos(self, archivos):
        """Actualiza la lista de archivos multimedia"""
        self.archivos_multimedia = archivos
        self.listbox.delete(0, tk.END)

        for archivo in archivos:
            nombre = os.path.basename(archivo)
            self.listbox.insert(tk.END, nombre)

        self.actualizar_contador()

    def actualizar_contador(self):
        """Actualiza el contador de archivos"""
        total = len(self.archivos_multimedia)
        self.label_contador.config(text=f"Archivos: {total}")
