# theme.py — Cores, fontes e temas do painel

# Fontes (compartilhadas entre todos os temas)
FONT_LARGE    = ("Consolas", 72, "bold")
FONT_TITLE    = ("Montserrat", 32, "bold")
FONT_SUBTITLE = ("Montserrat", 12)
FONT_MED      = ("Consolas", 24, "bold")
FONT_SMALL    = ("Consolas", 14, "bold")
FONT_MICRO    = ("Consolas", 10)
FONTEFINA     = ("Montserrat", 32)

# ─────────────────────────────────────────────
# DEFINIÇÃO DOS TEMAS
# ─────────────────────────────────────────────
THEMES = {
    "cyberpunk": {
        "name":         "CYBERPUNK RED",
        "icon":         "⬡",
        "BG_DEEP":      "#000000",
        "BG_PANEL":     "#050000",
        "ACCENT":       "#2BFF00",
        "ACCENT_DARK":  "#006002",
        "ACCENT2":      "#FF7700",
        "HIGHLIGHT":    "#FFFFFF",
        "DANGER":       "#FF0000",
        "WARN":         "#FFFF00",
        "CINZA":        "#616161",
        "DARKCINZA":    "#101010",
        "CINZAESCURO":  "#2D2D2D",
        "CINZAESCURO1": "#111111",
    },
    "neon_blue": {
        "name":         "AZUL NEON",
        "icon":         "⬡",
        "BG_DEEP":      "#000510",
        "BG_PANEL":     "#000820",
        "ACCENT":       "#00CFFF",
        "ACCENT_DARK":  "#004F6E",
        "ACCENT2":      "#7B2FFF",
        "HIGHLIGHT":    "#FFFFFF",
        "DANGER":       "#FF4466",
        "WARN":         "#FFD700",
        "CINZA":        "#4A5A6A",
        "DARKCINZA":    "#080F18",
        "CINZAESCURO":  "#1A2A3A",
        "CINZAESCURO1": "#0D1520",
    },
    "solar_green": {
        "name":         "VERDE SOLAR",
        "icon":         "⬡",
        "BG_DEEP":      "#020A02",
        "BG_PANEL":     "#030D03",
        "ACCENT":       "#AAFF00",
        "ACCENT_DARK":  "#3A6600",
        "ACCENT2":      "#FFB800",
        "HIGHLIGHT":    "#E8FFE8",
        "DANGER":       "#FF5500",
        "WARN":         "#FFEE00",
        "CINZA":        "#4A6040",
        "DARKCINZA":    "#0A1008",
        "CINZAESCURO":  "#1E2E1A",
        "CINZAESCURO1": "#0F180C",
    },
}

THEME_ORDER = ["cyberpunk", "neon_blue", "solar_green"]

# Tema ativo (começa com cyberpunk)
_current = "cyberpunk"


def get():
    """Retorna o dicionário do tema atual."""
    return THEMES[_current]


def next_theme():
    """Avança para o próximo tema e retorna o nome dele."""
    global _current
    idx = THEME_ORDER.index(_current)
    _current = THEME_ORDER[(idx + 1) % len(THEME_ORDER)]
    return _current


def current_name():
    return THEMES[_current]["name"]


# ─────────────────────────────────────────────
# Atalhos globais para compatibilidade com
# código legado que importa as cores diretamente
# (draw.py, dashboard.py, etc.)
# ─────────────────────────────────────────────
def _refresh_globals():
    t = get()
    globals().update({
        "BG_DEEP":      t["BG_DEEP"],
        "BG_PANEL":     t["BG_PANEL"],
        "GREEN":        t["ACCENT"],
        "VERDE_ESCURO": t["ACCENT_DARK"],
        "LARANJA":      t["ACCENT2"],
        "RED":          t["DANGER"],
        "YELOW":        t["WARN"],
        "RED_DIM":      t["DANGER"],
        "RED_DARK":     t["BG_PANEL"],
        "WHITE":        t["HIGHLIGHT"],
        "CINZA":        t["CINZA"],
        "DARKCINZA":    t["DARKCINZA"],
        "CINZAESCURO":  t["CINZAESCURO"],
        "CINZAESCURO1": t["CINZAESCURO1"],
        "MUTED":        t["BG_PANEL"],
        "TEXT_DIM":     t["CINZAESCURO"],
    })

_refresh_globals()