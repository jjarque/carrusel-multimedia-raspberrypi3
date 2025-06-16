class AppSettings:
    """Configuraciones de la aplicación"""

    def __init__(self):
        # Configuraciones por defecto
        self.tiempo_imagen = 5  # segundos por imagen
        self.modo_pantalla_completa = False
        self.reproducir_videos = True
        self.reproducir_imagenes = True
        self.modo_aleatorio = False
        self.repetir_lista = True

        # Configuraciones de interfaz
        self.ancho_ventana = 1200
        self.alto_ventana = 800
        self.color_fondo = 'black'

        # Configuraciones de archivos
        self.extensiones_imagen = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
        self.extensiones_video = ('.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm')
