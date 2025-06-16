#!/bin/bash
# crear_ejecutable.sh - Script para crear ejecutable con PyInstaller
# Convierte la aplicación Python en un ejecutable independiente

echo "=========================================="
echo "  Creando Ejecutable"
echo "  Carrusel Multimedia"
echo "=========================================="
echo ""

# Función para mostrar errores
mostrar_error() {
    echo "❌ ERROR: $1"
    exit 1
}

# Función para mostrar éxito
mostrar_exito() {
    echo "✅ $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    mostrar_error "No se encontró main.py. Ejecuta este script desde la raíz del proyecto."
fi

# Verificar Python
echo "🐍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    mostrar_error "Python 3 no está instalado"
fi
mostrar_exito "Python 3 disponible"

# Instalar PyInstaller si no está disponible
echo ""
echo "📦 Verificando PyInstaller..."
if python3 -c "import PyInstaller" 2>/dev/null; then
    mostrar_exito "PyInstaller ya está instalado"
else
    echo "📥 Instalando PyInstaller..."
    pip3 install pyinstaller || mostrar_error "No se pudo instalar PyInstaller"
    mostrar_exito "PyInstaller instalado correctamente"
fi

# Limpiar compilaciones anteriores
echo ""
echo "🧹 Limpiando compilaciones anteriores..."
if [ -d "build" ]; then
    rm -rf build
    echo "   • Directorio 'build' eliminado"
fi

if [ -d "dist" ]; then
    rm -rf dist
    echo "   • Directorio 'dist' eliminado"
fi

if [ -f "*.spec" ]; then
    rm -f *.spec
    echo "   • Archivos .spec eliminados"
fi

mostrar_exito "Limpieza completada"

# Verificar dependencias antes de compilar
echo ""
echo "🔍 Verificando dependencias..."
python3 -c "
try:
    import tkinter
    import PIL
    import vlc
    print('✅ Todas las dependencias están disponibles')
except ImportError as e:
    print(f'❌ Falta dependencia: {e}')
    exit(1)
" || mostrar_error "Faltan dependencias necesarias. Ejecuta ./setup_raspberry.sh primero"

# Crear ejecutable
echo ""
echo "🔨 Creando ejecutable..."
echo "   (Esto puede tomar varios minutos en Raspberry Pi)"
echo ""

# Comando PyInstaller con opciones optimizadas
pyinstaller \
    --onefile \
    --windowed \
    --name "CarruselMultimedia" \
    --add-data "config:config" \
    --add-data "src:src" \
    --hidden-import "PIL._tkinter_finder" \
    --hidden-import "vlc" \
    --clean \
    main.py

# Verificar si la compilación fue exitosa
if [ $? -eq 0 ] && [ -f "dist/CarruselMultimedia" ]; then
    mostrar_exito "Ejecutable creado exitosamente"
else
    mostrar_error "Falló la creación del ejecutable"
fi

# Hacer el ejecutable... ejecutable
chmod +x dist/CarruselMultimedia
mostrar_exito "Permisos de ejecución configurados"

# Obtener información del ejecutable
echo ""
echo "📊 Información del ejecutable:"
echo "   • Ubicación: $(pwd)/dist/CarruselMultimedia"
echo "   • Tamaño: $(du -h dist/CarruselMultimedia | cut -f1)"
echo "   • Permisos: $(ls -la dist/CarruselMultimedia | cut -d' ' -f1)"

# Crear script de distribución
echo ""
echo "📦 Creando paquete de distribución..."
cat > dist/INSTRUCCIONES.txt << 'EOF'
CARRUSEL MULTIMEDIA - INSTRUCCIONES DE USO
==========================================

REQUISITOS:
- Raspberry Pi con Raspberry Pi OS
- Pantalla conectada por HDMI
- Puerto USB disponible

INSTALACIÓN:
1. Copiar el archivo "CarruselMultimedia" a cualquier carpeta
2. Abrir terminal en esa carpeta
3. Ejecutar: chmod +x CarruselMultimedia

USO:
1. Conectar USB con fotos y videos
2. Ejecutar: ./CarruselMultimedia
3. Presionar "Detectar USB"
4. Configurar tiempo por imagen
5. Presionar "Iniciar Carrusel"

FORMATOS SOPORTADOS:
- Imágenes: JPG, PNG, GIF, BMP, TIFF
- Videos: MP4, AVI, MOV, MKV, WMV

PROBLEMAS COMUNES:
- Si no detecta USB: verificar que esté montado en /media/
- Si no reproduce videos: instalar VLC (sudo apt install vlc)
- Para salir: presionar tecla Escape

CONTACTO:
- Repositorio: https://github.com/tu-usuario/carrusel-multimedia
EOF

mostrar_exito "Instrucciones de uso creadas"

# Crear script de instalación para el usuario final
cat > dist/instalar.sh << 'EOF'
#!/bin/bash
echo "Instalando Carrusel Multimedia..."

# Hacer ejecutable
chmod +x CarruselMultimedia

# Verificar VLC
if ! command -v vlc &> /dev/null; then
    echo "Instalando VLC..."
    sudo apt update
    sudo apt install vlc-bin vlc-plugin-base -y
fi

echo "✅ Instalación completada"
echo "Ejecutar con: ./CarruselMultimedia"
EOF

chmod +x dist/instalar.sh
mostrar_exito "Script de instalación creado"

# Finalización
echo ""
echo "=========================================="
echo "✅ EJECUTABLE CREADO EXITOSAMENTE"
echo "=========================================="
echo ""
echo "📁 Archivos generados:"
echo "   • dist/CarruselMultimedia (ejecutable principal)"
echo "   • dist/INSTRUCCIONES.txt (guía de uso)"
echo "   • dist/instalar.sh (script de instalación)"
echo ""
echo "📋 Para distribuir:"
echo "   • Copiar toda la carpeta 'dist/' al usuario final"
echo "   • El usuario debe ejecutar: ./instalar.sh"
echo "   • Luego ejecutar: ./CarruselMultimedia"
echo ""
echo "🧪 Para probar localmente:"
echo "   • cd dist"
echo "   • ./CarruselMultimedia"
echo ""
echo "🎉 ¡Ejecutable listo para distribución!"
