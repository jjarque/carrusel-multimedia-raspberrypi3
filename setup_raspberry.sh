#!/bin/bash
# setup_raspberry.sh - Script de configuración para Raspberry Pi
# Configura automáticamente el entorno para ejecutar la aplicación de carrusel

echo "=========================================="
echo "  Configurando Carrusel Multimedia"
echo "  para Raspberry Pi"
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

# Verificar si estamos en Raspberry Pi
echo "🔍 Verificando sistema..."
if [[ $(uname -m) == arm* ]] || [[ $(uname -m) == aarch64 ]]; then
    mostrar_exito "Sistema ARM detectado (Raspberry Pi)"
else
    echo "⚠️  ADVERTENCIA: No se detectó Raspberry Pi, continuando..."
fi

# Actualizar sistema
echo ""
echo "📦 Actualizando sistema..."
sudo apt update || mostrar_error "No se pudo actualizar la lista de paquetes"

# Instalar Python 3.11 si no está disponible
echo ""
echo "🐍 Verificando Python 3.11..."
if command -v python3.11 &> /dev/null; then
    mostrar_exito "Python 3.11 ya está instalado"
else
    echo "📥 Instalando Python 3.11..."
    sudo apt install python3.11 python3.11-venv python3.11-dev python3.11-tk -y || mostrar_error "No se pudo instalar Python 3.11"
    mostrar_exito "Python 3.11 instalado correctamente"
fi

# Instalar pip para Python 3.11
echo ""
echo "📦 Verificando pip..."
if command -v pip3 &> /dev/null; then
    mostrar_exito "pip ya está disponible"
else
    echo "📥 Instalando pip..."
    sudo apt install python3-pip -y || mostrar_error "No se pudo instalar pip"
    mostrar_exito "pip instalado correctamente"
fi

# Instalar dependencias del sistema para tkinter
echo ""
echo "🖼️  Instalando dependencias gráficas..."
sudo apt install python3-tk python3-pil python3-pil.imagetk -y || mostrar_error "No se pudieron instalar las dependencias gráficas"
mostrar_exito "Dependencias gráficas instaladas"

# Instalar VLC para reproducción de videos
echo ""
echo "🎥 Instalando VLC Media Player..."
sudo apt install vlc-bin vlc-plugin-base -y || mostrar_error "No se pudo instalar VLC"
mostrar_exito "VLC instalado correctamente"

# Instalar dependencias Python
echo ""
echo "🔧 Instalando dependencias Python..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt || mostrar_error "No se pudieron instalar las dependencias Python"
    mostrar_exito "Dependencias Python instaladas desde requirements.txt"
else
    echo "📥 Instalando dependencias manualmente..."
    pip3 install pillow python-vlc || mostrar_error "No se pudieron instalar las dependencias Python"
    mostrar_exito "Dependencias Python instaladas manualmente"
fi

# Verificar instalación
echo ""
echo "🔍 Verificando instalación..."

# Verificar Python
if python3 -c "import tkinter, PIL, vlc" 2>/dev/null; then
    mostrar_exito "Todas las bibliotecas Python están disponibles"
else
    mostrar_error "Faltan algunas bibliotecas Python"
fi

# Verificar VLC
if command -v vlc &> /dev/null; then
    mostrar_exito "VLC está disponible"
else
    echo "⚠️  ADVERTENCIA: VLC no se encontró en PATH"
fi

# Crear script de ejecución rápida
echo ""
echo "🚀 Creando script de ejecución rápida..."
cat > ejecutar_carrusel.sh << 'EOF'
#!/bin/bash
# Script de ejecución rápida para el carrusel
cd "$(dirname "$0")"
python3 main.py
EOF

chmod +x ejecutar_carrusel.sh
mostrar_exito "Script de ejecución creado: ./ejecutar_carrusel.sh"

# Finalización
echo ""
echo "=========================================="
echo "✅ CONFIGURACIÓN COMPLETADA"
echo "=========================================="
echo ""
echo "📋 Para ejecutar la aplicación:"
echo "   • Opción 1: python3 main.py"
echo "   • Opción 2: ./ejecutar_carrusel.sh"
echo ""
echo "📋 Para crear ejecutable:"
echo "   • ./crear_ejecutable.sh"
echo ""
echo "🔧 Requisitos cumplidos:"
echo "   ✅ Python 3.11+"
echo "   ✅ Bibliotecas gráficas (tkinter, PIL)"
echo "   ✅ VLC Media Player"
echo "   ✅ Dependencias Python (pillow, python-vlc)"
echo ""
echo "🎉 ¡Listo para usar!"
