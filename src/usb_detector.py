import os
import threading
from tkinter import messagebox


class USBDetector:
    def __init__(self, app):
        self.app = app
        self.extensiones_soportadas = (
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff',  # Imágenes
            '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'  # Videos
        )

    def detectar_dispositivos(self):
        """Detecta dispositivos USB montados"""
        # Ejecutar en hilo separado para no bloquear la interfaz
        hilo = threading.Thread(target=self._buscar_usb, daemon=True)
        hilo.start()

    def _buscar_usb(self):
        """Busca dispositivos USB en rutas típicas de montaje"""
        rutas_montaje = [
            '/media/pi/',
            '/media/',
            '/mnt/',
            '/run/media/',
        ]

        dispositivos_encontrados = []
        archivos_multimedia = []

        for ruta_base in rutas_montaje:
            if os.path.exists(ruta_base):
                try:
                    for item in os.listdir(ruta_base):
                        ruta_dispositivo = os.path.join(ruta_base, item)
                        if os.path.isdir(ruta_dispositivo) and os.access(ruta_dispositivo, os.R_OK):
                            dispositivos_encontrados.append(ruta_dispositivo)
                except PermissionError:
                    continue

        if not dispositivos_encontrados:
            self.app.root.after(0, lambda: messagebox.showwarning(
                "Sin USB",
                "No se detectaron dispositivos USB.\n\nAsegúrate de que:\n• El USB esté conectado\n• El USB esté montado correctamente"
            ))
            return

        # Buscar archivos multimedia en todos los dispositivos
        for dispositivo in dispositivos_encontrados:
            archivos_encontrados = self._buscar_archivos_multimedia(dispositivo)
            archivos_multimedia.extend(archivos_encontrados)

        # Actualizar interfaz en hilo principal
        self.app.root.after(0, self._actualizar_interfaz, dispositivos_encontrados, archivos_multimedia)

    def _buscar_archivos_multimedia(self, ruta_dispositivo):
        """Busca archivos multimedia en un dispositivo"""
        archivos_encontrados = []

        try:
            for root, dirs, files in os.walk(ruta_dispositivo):
                for archivo in files:
                    if archivo.lower().endswith(self.extensiones_soportadas):
                        ruta_completa = os.path.join(root, archivo)
                        archivos_encontrados.append(ruta_completa)
        except (PermissionError, OSError) as e:
            print(f"Error accediendo a {ruta_dispositivo}: {e}")

        return archivos_encontrados

    def _actualizar_interfaz(self, dispositivos, archivos):
        """Actualiza la interfaz con los archivos encontrados"""
        if not archivos:
            messagebox.showinfo(
                "Sin archivos multimedia",
                f"Se detectaron {len(dispositivos)} dispositivos USB, pero no contienen archivos multimedia soportados.\n\nFormatos soportados:\n• Imágenes: JPG, PNG, GIF, BMP\n• Videos: MP4, AVI, MOV, MKV"
            )
            return

        # Actualizar lista de archivos
        self.app.actualizar_lista_archivos(archivos)

        messagebox.showinfo(
            "USB Detectado",
            f"✅ Dispositivos USB encontrados: {len(dispositivos)}\n📁 Archivos multimedia: {len(archivos)}\n\n¡Ya puedes iniciar el carrusel!"
        )
