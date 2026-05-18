#!/bin/bash
# install.sh — Instalação completa do BioVolts no Raspberry Pi
set -e

echo "================================================"
echo "  BioVolts — Instalador para Raspberry Pi"
echo "================================================"

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
APP_DIR="$PROJECT_DIR/frontend/app"
USER=$(whoami)
HOME_DIR=$(eval echo ~$USER)
AUTOSTART_DIR="$HOME_DIR/.config/autostart"
AUTOSTART_FILE="$AUTOSTART_DIR/biovolts.desktop"

echo ""
echo "[1/5] Atualizando o sistema..."
sudo apt update -y

echo ""
echo "[2/5] Instalando dependências do sistema..."
sudo apt install -y python3-pip python3-tk i2c-tools

echo ""
echo "[3/5] Habilitando I2C..."
sudo raspi-config nonint do_i2c 0
echo "      I2C habilitado."

echo ""
echo "[4/5] Instalando dependências Python..."
pip install customtkinter adafruit-circuitpython-ads1x15 adafruit-blinka pydantic --break-system-packages

echo ""
echo "[5/5] Criando autostart via .desktop (método correto para interface gráfica)..."

# Remove o serviço systemd antigo se existir
if [ -f /etc/systemd/system/biovolts.service ]; then
    sudo systemctl stop biovolts.service 2>/dev/null || true
    sudo systemctl disable biovolts.service 2>/dev/null || true
    sudo rm /etc/systemd/system/biovolts.service
    sudo systemctl daemon-reload
    echo "      Serviço systemd antigo removido."
fi

# Cria a pasta autostart se não existir
mkdir -p "$AUTOSTART_DIR"

# Cria o arquivo .desktop
cat > "$AUTOSTART_FILE" << DESKTOP
[Desktop Entry]
Type=Application
Name=BioVolts
Comment=Painel de Energia Solar
Exec=/usr/bin/python3 $APP_DIR/main.py
WorkingDirectory=$APP_DIR
X-GNOME-Autostart-enabled=true
DESKTOP

echo "      Arquivo criado em: $AUTOSTART_FILE"

echo ""
echo "================================================"
echo "  Instalação concluída!"
echo ""
echo "  Comandos úteis:"
echo "  Rodar agora:    python3 $APP_DIR/main.py"
echo "  Ver autostart:  cat $AUTOSTART_FILE"
echo "  Remover:        rm $AUTOSTART_FILE"
echo "================================================"
echo ""
echo "  Reinicie para ativar o autostart:"
echo "  sudo reboot"
echo "================================================"