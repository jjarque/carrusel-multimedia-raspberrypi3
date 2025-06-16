# Carrusel Multimedia

Aplicación para mostrar fotos y videos desde dispositivos USB en Raspberry Pi.

## Características

- Detección automática de dispositivos USB
- Soporte para imágenes (JPG, PNG, GIF, BMP, TIFF)
- Soporte para videos (MP4, AVI, MOV, MKV, WMV)
- Interfaz gráfica intuitiva
- Tiempo configurable por imagen
- Reproducción en bucle automático

## Instalación

1. Clonar repositorio:

`git clone https://github.com/jjarque/carrusel-multimedia-raspberrypi3.git
cd carrusel-multimedia`

2. Ejecutar script de configuración:

``chmod +x setup_raspberry.sh
./setup_raspberry.sh``

3. Ejecutar aplicación:

`python3 main.py`


## Crear Ejecutable

`chmod +x crear_ejecutable.sh
./crear_ejecutable.sh`


## Uso

1. Conectar USB con fotos y videos
2. Abrir la aplicación
3. Presionar "Detectar USB"
4. Configurar tiempo por imagen
5. Presionar "Iniciar Carrusel"

## Requisitos

- Raspberry Pi con Raspberry Pi OS
- Python 3.11 o superior
- VLC media player