import tkinter as tk
from PIL import Image, ImageTk
import vlc
import os


class MediaPlayer:
    def __init__(self, app):
        self.app = app
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.imagen_actual = None

        # Extensiones soportadas
        self.extensiones_imagen = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
        self.extensiones_video = ('.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm')

    def es_imagen(self, archivo):
        """Verifica si el archivo es una imagen"""
        return archivo.lower().endswith(self.extensiones_imagen)

    def es_video(self, archivo):
        """Verifica si el archivo es un video"""
        return archivo.lower().endswith(self.extensiones_video)

    def mostrar_archivo(self, ruta_archivo):
        """Muestra un archivo (imagen o video)"""
        try:
            if self.es_imagen(ruta_archivo):
                self.mostrar_imagen(ruta_archivo)
            elif self.es_video(ruta_archivo):
                self.reproducir_video(ruta_archivo)
            else:
                print(f"Formato no soportado: {ruta_archivo}")
        except Exception as e:
            print(f"Error mostrando archivo {ruta_archivo}: {e}")

    def mostrar_imagen(self, ruta_imagen):
        """Muestra una imagen en el área de visualización"""
        try:
            # Detener video si está reproduciéndose
            self.detener_video()

            # Cargar imagen
            imagen = Image.open(ruta_imagen)

            # Obtener dimensiones del área de visualización
            self.app.frame_visualizacion.update()
            ancho_frame = self.app.frame_visualizacion.winfo_width()
            alto_frame = self.app.frame_visualizacion.winfo_height()

            if ancho_frame > 1 and alto_frame > 1:
                # Redimensionar manteniendo proporción
                imagen = self.redimensionar_imagen(imagen, ancho_frame, alto_frame)

            # Convertir para tkinter
            self.imagen_actual = ImageTk.PhotoImage(imagen)

            # Mostrar imagen
            self.app.label_multimedia.config(
                image=self.imagen_actual,
                text="",
                compound=tk.CENTER
            )

        except Exception as e:
            print(f"Error cargando imagen {ruta_imagen}: {e}")
            self.app.label_multimedia.config(
                text=f"Error cargando imagen:\n{os.path.basename(ruta_imagen)}",
                image="",
                fg='red'
            )

    def redimensionar_imagen(self, imagen, ancho_max, alto_max):
        """Redimensiona imagen manteniendo proporción"""
        ancho_orig, alto_orig = imagen.size

        # Calcular ratio para mantener proporción
        ratio = min(ancho_max / ancho_orig, alto_max / alto_orig)

        nuevo_ancho = int(ancho_orig * ratio)
        nuevo_alto = int(alto_orig * ratio)

        return imagen.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)

    def reproducir_video(self, ruta_video):
        """Reproduce un video usando VLC"""
        try:
            # Limpiar imagen anterior
            self.app.label_multimedia.config(image="", text="Reproduciendo video...")

            # Crear media y reproducir
            media = self.instance.media_new(ruta_video)
            self.player.set_media(media)

            # Configurar ventana de video
            if hasattr(self.app.label_multimedia, 'winfo_id'):
                self.player.set_xwindow(self.app.label_multimedia.winfo_id())

            self.player.play()

            # Esperar a que termine el video
            self.app.root.after(1000, self.verificar_estado_video)

        except Exception as e:
            print(f"Error reproduciendo video {ruta_video}: {e}")
            self.app.label_multimedia.config(
                text=f"Error reproduciendo video:\n{os.path.basename(ruta_video)}",
                fg='red'
            )

    def verificar_estado_video(self):
        """Verifica si el video ha terminado"""
        if self.player.get_state() == vlc.State.Ended:
            return  # Video terminado, continuar con siguiente archivo
        elif self.app.reproduciendo:
            # Seguir verificando
            self.app.root.after(1000, self.verificar_estado_video)

    def detener_video(self):
        """Detiene la reproducción de video"""
        if self.player:
            self.player.stop()
