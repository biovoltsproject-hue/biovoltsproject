# biovoltsproject

BioVolts project, a interface ideal para seu sistema solar.

# ☀️ Painel de Energia Solar Portátil

Interface gráfica futurista para monitoramento de energia solar, desenvolvida em Python com CustomTkinter.

---

## 📋 Pré-requisitos

- Python **3.9** ou superior
- pip (gerenciador de pacotes do Python)

---

## 📦 Dependências

| Pacote          | Versão mínima       | Uso no projeto               |
| --------------- | ------------------- | ---------------------------- |
| `customtkinter` | 5.2.0               | Janela principal e tema dark |
| `tkinter`       | (incluso no Python) | Canvas, desenho e animações  |

### Instalação

```bash
pip install customtkinter
```

> **Nota:** `tkinter` já vem incluído no Python padrão. Caso não esteja disponível (algumas distros Linux), instale com:

---

## 🗂️ Estrutura do Projeto

```
frontend/
├── main.py        # Ponto de entrada — inicializa a janela
├── dashboard.py   # Canvas principal com toda a lógica visual
├── draw.py        # Funções reutilizáveis de desenho neon e ícones
└── theme.py       # Cores e fontes do painel
```

---

## 🚀 Como Executar

1. Clone ou baixe os arquivos na mesma pasta
2. Instale as dependências:

```bash
pip install customtkinter
```

3. Execute:

```bash
python main.py
```

---

## 🖥️ Compatibilidade

| Sistema Operacional            | Suporte                     |
| ------------------------------ | --------------------------- |
| Windows 10/11                  | ✅                          |
| Linux (Ubuntu, Debian, Fedora) | ✅                          |
| macOS 11+                      | ✅                          |
| Raspberry Pi OS                | ✅ (otimizado para 800×480) |

---

## ⚙️ Modo Kiosk (Raspberry Pi)

Para rodar em tela cheia sem barra de título no Raspberry Pi, descomente a linha no `dashboard.py`:

```python
# self.overrideredirect(True)  ← remova o # para ativar
```

---

## 📄 Licença

MIT — livre para uso e modificação.
