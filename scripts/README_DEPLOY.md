# BioVolts — Deploy no Raspberry Pi

## Pré-requisitos

- Raspberry Pi 4 com Raspberry Pi OS (Desktop)
- Projeto clonado em `/home/biovolts/BIOVOLTS/`
- Usuário logado: `biovolts`

---

## Estrutura esperada no Pi

```
/home/biovolts/BIOVOLTS/
├── frontend/
│   └── app/
│       ├── main.py
│       ├── dashboard.py
│       ├── draw.py
│       ├── theme.py
│       └── sensor_backend.py  ← temporário (mock)
├── backend/
│   ├── models/
│   │   ├── sensor_backend.py  ← versão real (hardware)
│   │   ├── models.py
│   │   └── Fonte.py
│   └── requirements.txt
├── scripts/
│   └── install.sh
└── README_DEPLOY.md
```

---

## Instalação

Copie o projeto para o Pi (via pendrive, git clone ou scp) e rode:

```bash
cd /home/biovolts/BIOVOLTS/scripts
bash install.sh
```

O script faz automaticamente:
- Atualiza o sistema
- Instala dependências Python e do sistema
- Habilita o I2C
- Cria e ativa o serviço systemd de autostart

Depois reinicie:
```bash
sudo reboot
```

---

## Verificar se está funcionando

```bash
# Ver status do serviço
sudo systemctl status biovolts

# Acompanhar logs em tempo real
journalctl -u biovolts -f
```

---

## Comandos úteis

| Ação | Comando |
|---|---|
| Iniciar manualmente | `sudo systemctl start biovolts` |
| Parar | `sudo systemctl stop biovolts` |
| Reiniciar | `sudo systemctl restart biovolts` |
| Ver logs | `journalctl -u biovolts -f` |
| Desativar autostart | `sudo systemctl disable biovolts` |

---

## Quando o hardware ADS1115 estiver funcionando

Substitua o `sensor_backend.py` da pasta `frontend/app/` pelo da pasta `backend/models/` e reinicie o serviço:

```bash
cp backend/models/sensor_backend.py frontend/app/sensor_backend.py
sudo systemctl restart biovolts
```

Verifique se o ADS1115 está detectado no I2C:
```bash
i2cdetect -y 1
# Deve aparecer "48" na tabela
```

---

## Modo Kiosk (tela cheia sem barra de título)

Edite `frontend/app/main.py` e mude:
```python
self.attributes("-fullscreen", False)
```
para:
```python
self.attributes("-fullscreen", True)
```

---

## Calibração dos sensores

Edite as constantes no topo do `sensor_backend.py` (versão real):

```python
FATOR_TENSAO      = 5.0    # Módulo 0-24V genérico (R1=30k, R2=7.5k)
SENSIBILIDADE_ACS712 = 0.100  # 20A → 0.100 | 5A → 0.185 | 30A → 0.066
OFFSET_ACS712     = 2.5    # Ajuste se a corrente em repouso não for zero
TENSAO_MIN_V      = 10.5   # 0% da bateria
TENSAO_MAX_V      = 12.7   # 100% da bateria
CAPACIDADE_AH     = 7.0    # Capacidade da sua bateria em Ah
```
