#!/bin/bash
# install.sh — Instalação completa do BioVolts no Raspberry Pi
# Execute com: bash install.sh

set -e  # Para em caso de erro

echo "================================================"
echo "  BioVolts — Instalador para Raspberry Pi"
echo "================================================"

# Diretório onde o projeto está (mesmo diretório do script)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$PROJECT_DIR/frontend/app"
SERVICE_FILE="/etc/systemd/system/biovolts.service"
USER=$(whoami)

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
echo "[5/5] Criando serviço systemd para autostart..."

sudo bash -c "cat > $SERVICE_FILE << SERVICE
[Unit]
Description=BioVolts - Painel de Energia Solar
After=graphical.target

[Service]
Type=simple
User=$USER
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/$USER/.Xauthority
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python3 $APP_DIR/main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=graphical.target
SERVICE"

sudo systemctl daemon-reload
sudo systemctl enable biovolts.service

echo ""
echo "================================================"
echo "  Instalação concluída!"
echo ""
echo "  Comandos úteis:"
echo "  Iniciar agora:   sudo systemctl start biovolts"
echo "  Ver status:      sudo systemctl status biovolts"
echo "  Ver logs:        journalctl -u biovolts -f"
echo "  Parar:           sudo systemctl stop biovolts"
echo "  Desativar:       sudo systemctl disable biovolts"
echo "================================================"
echo ""
echo "  Reinicie o Raspberry Pi para ativar o autostart:"
echo "  sudo reboot"
echo "================================================"
