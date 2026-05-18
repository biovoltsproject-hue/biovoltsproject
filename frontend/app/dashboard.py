# dashboard.py — Canvas principal do painel solar (800x480) com troca de temas
import tkinter as tk
import math
import random
import queue
from datetime import datetime
import theme as TH
from draw import *


def _t():
    """Retorna o tema atual como dict."""
    return TH.get()


class SolarDashboard(tk.Canvas):
    W, H = 800, 480

    def __init__(self, master, data_queue, **kw):
        super().__init__(master, width=self.W, height=self.H,
                         bg=TH.BG_DEEP, highlightthickness=0, bd=0)
        self.data_queue = data_queue

        self._battery      = 0.0
        self._status       = "AGUARDANDO SINAL..."
        self._time_to_full = 0
        self._raw_v        = 0.0
        self._raw_i        = 0.0

        self._angle    = 0
        self._pulse    = 0
        self._particles = [
            {"x": random.randint(0, self.W), "y": random.randint(0, self.H),
             "speed": random.uniform(1, 3), "len": random.randint(4, 15)}
            for _ in range(30)
        ]

        # Estado da animação de ondas
        self._ripples      = []
        self._detail_open  = False
        self._detail_alpha = 0

        # Animação de troca de tema
        self._theme_flash  = 0   # frames do flash ao trocar tema

        # Bind de clique
        self.bind("<Button-1>", self._on_click)

        self._draw_all()
        self._animate_visuals()
        self._poll_backend_data()

    # ── DADOS ──────────────────────────────────────────────────────────
    def _poll_backend_data(self):
        try:
            data = self.data_queue.get_nowait()
            self._battery      = data.get("battery",      self._battery)
            self._status       = data.get("status",       self._status)
            self._time_to_full = data.get("time_to_full", 0)
            self._raw_v        = data.get("raw_v",        self._raw_v)
            self._raw_i        = data.get("raw_i",        self._raw_i)
        except queue.Empty:
            pass
        self.after(200, self._poll_backend_data)

    # ── CLIQUE ─────────────────────────────────────────────────────────
    def _on_click(self, event):
        W, H  = self.W, self.H
        cx_main = W // 2
        cy_main = (60 + 440) // 2

        # Botão de tema — canto inferior direito (80x36)
        btn_x1, btn_y1 = W - 90, H - 44
        btn_x2, btn_y2 = W - 10, H - 10
        if btn_x1 <= event.x <= btn_x2 and btn_y1 <= event.y <= btn_y2:
            self._switch_theme()
            return

        # Fechar tela de detalhes
        if self._detail_open:
            self._detail_open  = False
            self._detail_alpha = 0
            return

        # Ondas no centro
        dist = math.hypot(event.x - cx_main, event.y - cy_main)
        if dist < 110:
            self._ripples = [
                {"r": 0, "max_r": 180, "speed": 6, "delay": i * 6}
                for i in range(4)
            ]
            self._animate_ripple()

    # ── TROCA DE TEMA ──────────────────────────────────────────────────
    def _switch_theme(self):
        TH.next_theme()
        TH._refresh_globals()
        self.configure(bg=TH.BG_DEEP)
        self._theme_flash = 8   # 8 frames de flash branco
        self._animate_theme_flash()

    def _animate_theme_flash(self):
        if self._theme_flash > 0:
            self._theme_flash -= 1
            self._draw_all()
            self.after(30, self._animate_theme_flash)
        else:
            self._draw_all()

    # ── ONDAS ──────────────────────────────────────────────────────────
    def _animate_ripple(self):
        all_done = True
        for rip in self._ripples:
            if rip["delay"] > 0:
                rip["delay"] -= 1
                all_done = False
            elif rip["r"] < rip["max_r"]:
                rip["r"] += rip["speed"]
                all_done = False
        self._draw_all()
        if not all_done:
            self.after(16, self._animate_ripple)
        else:
            self._ripples      = []
            self._detail_open  = True
            self._detail_alpha = 0
            self._animate_detail_open()

    def _animate_detail_open(self):
        if self._detail_alpha < 20:
            self._detail_alpha += 1
            self._draw_all()
            self.after(16, self._animate_detail_open)

    # ── LOOP VISUAL ────────────────────────────────────────────────────
    def _animate_visuals(self):
        self._angle = (self._angle + 2) % 360
        self._pulse = (self._pulse + 0.1) % (2 * math.pi)
        for p in self._particles:
            p["y"] += p["speed"]
            if p["y"] > self.H:
                p["y"] = -20
                p["x"] = random.randint(0, self.W)
        if not self._ripples:
            self._draw_all()
        self.after(60, self._animate_visuals)

    # ── DRAW PRINCIPAL ─────────────────────────────────────────────────
    def _draw_all(self):
        t = _t()
        self.delete("all")
        self._bg(t)
        self._header(t)
        self._left_card(t)
        self._center_card(t)
        self._right_card(t)
        self._bottom_bar(t)
        self._theme_button(t)

        if self._theme_flash > 0:
            # Flash branco ao trocar tema
            opacity_rect = self.create_rectangle(
                0, 0, self.W, self.H,
                fill=t["HIGHLIGHT"], outline=""
            )
            # Simula fade diminuindo a cada frame
            factor = self._theme_flash / 8
            # Não há transparência real no tkinter canvas,
            # então usamos o flash por frames como efeito
            if self._theme_flash < 4:
                self.delete(opacity_rect)

        if self._ripples:
            self._draw_ripples(t)
        if self._detail_open:
            self._draw_detail_screen(t)

    # ── BOTÃO DE TEMA ──────────────────────────────────────────────────
    def _theme_button(self, t):
        W, H = self.W, self.H
        x1, y1 = W - 90, H - 44
        x2, y2 = W - 10, H - 10

        # Fundo do botão
        self.create_rectangle(x1, y1, x2, y2,
                              fill=t["BG_PANEL"], outline=t["ACCENT"], width=1)

        # Cantos decorativos
        s = 5
        for (ax, ay) in [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]:
            dx = s if ax == x1 else -s
            dy = s if ay == y1 else -s
            self.create_line(ax, ay, ax+dx, ay, fill=t["ACCENT"], width=2)
            self.create_line(ax, ay, ax, ay+dy, fill=t["ACCENT"], width=2)

        # Ícone e nome do próximo tema
        idx  = TH.THEME_ORDER.index(TH._current)
        next_key  = TH.THEME_ORDER[(idx + 1) % len(TH.THEME_ORDER)]
        next_name = TH.THEMES[next_key]["name"].split()[0]  # só a 1ª palavra

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        self.create_text(cx, cy - 6, text="TEMA",
                         fill=t["CINZA"], font=("Consolas", 7), anchor="center")
        self.create_text(cx, cy + 7, text=next_name,
                         fill=t["ACCENT"], font=("Consolas", 8, "bold"), anchor="center")

    # ── ONDAS DE ENERGIA ───────────────────────────────────────────────
    def _draw_ripples(self, t):
        cx = self.W // 2
        cy = (60 + 440) // 2
        for rip in self._ripples:
            if rip["delay"] > 0 or rip["r"] == 0:
                continue
            r        = rip["r"]
            max_r    = rip["max_r"]
            progress = r / max_r
            width    = max(1, int(4 * (1 - progress)))
            self.create_oval(cx-r, cy-r, cx+r, cy+r,
                             outline=t["ACCENT"], width=width, fill="")
            r2 = max(0, r - 30)
            if r2 > 0:
                self.create_oval(cx-r2, cy-r2, cx+r2, cy+r2,
                                 outline=t["HIGHLIGHT"], width=1, fill="")
        first = self._ripples[0] if self._ripples else None
        if first and first["r"] < 40 and first["delay"] == 0:
            fr = first["r"]
            self.create_oval(cx-fr, cy-fr, cx+fr, cy+fr,
                             outline=t["ACCENT"], width=6, fill="")

    # ── TELA DE DETALHES ───────────────────────────────────────────────
    def _draw_detail_screen(self, t):
        W, H  = self.W, self.H
        alpha = min(self._detail_alpha / 20, 1.0)
        pad   = int(20 * alpha)
        x1, y1, x2, y2 = pad, pad, W-pad, H-pad

        self.create_rectangle(x1, y1, x2, y2,
                              fill=t["BG_PANEL"], outline=t["ACCENT"], width=2)
        sz = 16
        for (ax, ay) in [(x1, y1), (x2-sz, y1), (x1, y2-sz), (x2-sz, y2-sz)]:
            self.create_line(ax, ay, ax+sz, ay, fill=t["ACCENT"], width=3)
            self.create_line(ax, ay, ax, ay+sz, fill=t["ACCENT"], width=3)

        if alpha < 0.5:
            return

        cx      = W // 2
        title_y = y1 + 36
        neon_text(self, cx, title_y, "DADOS DO SISTEMA",
                  t["ACCENT"], ("Consolas", 14, "bold"))
        self.create_line(x1+40, title_y+18, x2-40, title_y+18,
                         fill=t["CINZAESCURO"], width=1)

        potencia = abs(self._raw_v * self._raw_i)
        dados = [
            ("TENSÃO",   f"{self._raw_v:.2f} V",               t["ACCENT"]),
            ("CORRENTE", f"{self._raw_i:.3f} A",               t["ACCENT"]),
            ("POTÊNCIA", f"{potencia:.2f} W",                  t["WARN"]),
            ("BATERIA",  f"{self._battery:.1f} %",             t["ACCENT"]),
            ("STATUS",   self._status,                         t["HIGHLIGHT"]),
            ("TEMPO",    f"{self._time_to_full} min"
                         if self._time_to_full > 0 else "---", t["HIGHLIGHT"]),
        ]

        cols   = 2
        rows   = math.ceil(len(dados) / cols)
        cell_w = (x2 - x1 - 80) // cols
        cell_h = (y2 - title_y - 80) // rows
        sx, sy = x1 + 40, title_y + 36

        for i, (label, valor, cor) in enumerate(dados):
            col = i % cols
            row = i // cols
            bx  = sx + col * cell_w
            by  = sy + row * cell_h
            self.create_rectangle(bx, by, bx+cell_w-16, by+cell_h-12,
                                  fill=t["BG_DEEP"], outline=t["CINZAESCURO"], width=1)
            self.create_text(bx+12, by+14, text=label,
                             fill=t["CINZA"], font=("Consolas", 8), anchor="w")
            fs = 8 if len(valor) > 16 else 13
            self.create_text(bx+12, by+cell_h-22, text=valor,
                             fill=cor, font=("Consolas", fs, "bold"), anchor="w")

        self.create_text(cx, y2-16, text="[ TOQUE PARA FECHAR ]",
                         fill=t["CINZA"], font=("Consolas", 8), anchor="center")

    # ── BACKGROUND ─────────────────────────────────────────────────────
    def _bg(self, t):
        W, H = self.W, self.H
        self.create_rectangle(0, 0, W, H, fill=t["BG_DEEP"], outline="")
        for p in self._particles:
            self.create_line(p["x"], p["y"], p["x"], p["y"]+p["len"],
                             fill=t["DARKCINZA"], width=1)
        self.create_line(W//2-60, 8,   W//2+60, 8,   fill=t["HIGHLIGHT"], width=4)
        self.create_line(W//2-20, 12,  W//2+20, 12,  fill=t["HIGHLIGHT"], width=2)
        self.create_line(W//2-60, H-8, W//2+60, H-8, fill=t["HIGHLIGHT"], width=4)
        self.create_line(W//2-20, H-12,W//2+20, H-12,fill=t["HIGHLIGHT"], width=2)
        for i in range(4):
            self.create_line(40+i*10, 22,  45+i*10, 12,  fill=t["CINZAESCURO"], width=2)
            self.create_line(W-80+i*10, 22,W-75+i*10, 12,fill=t["CINZAESCURO"], width=2)
            self.create_line(40+i*10, H-12,45+i*10, H-22,fill=t["CINZAESCURO"], width=2)
            self.create_line(W-80+i*10, H-12,W-75+i*10, H-22,fill=t["CINZAESCURO"],width=2)
        for r in range(4):
            for c in range(2):
                for ox, oy in [(12, 120), (12, 340), (W-26, 120), (W-26, 340)]:
                    self.create_oval(ox+c*7, oy+r*7, ox+c*7+3, oy+r*7+3,
                                     fill=t["CINZA"], outline="")

    # ── HEADER ─────────────────────────────────────────────────────────
    def _header(self, t):
        cx = self.W // 2
        self.create_line(40, 32, cx-160, 32, fill=t["CINZAESCURO"], width=1)
        self.create_line(cx+160, 32, self.W-40, 32, fill=t["CINZAESCURO"], width=1)
        self.create_oval(cx-165, 29, cx-155, 35, fill=t["CINZAESCURO"], outline="")
        self.create_oval(cx+155, 29, cx+165, 35, fill=t["CINZAESCURO"], outline="")
        self.create_text(cx-130, 30, text="[", fill=t["CINZAESCURO"],
                         font=("Montserrat", 18, "bold"), anchor="center")
        self.create_text(cx+130, 30, text="]", fill=t["CINZAESCURO"],
                         font=("Montserrat", 18, "bold"), anchor="center")
        neon_text(self, cx-30, 28, "Bio",   t["ACCENT"],      ("Montserrat", 20))
        neon_text(self, cx+28, 28, "Volts", t["ACCENT_DARK"], ("Montserrat", 20, "bold"))
        self.create_text(cx, 50, text="SUA ENERGIA SOLAR PORTÁTIL",
                         fill=t["HIGHLIGHT"], font=("Montserrat", 8), anchor="center")
        now = datetime.now()
        icon_clock(self, 28, 28)
        self.create_text(70, 28, text=now.strftime("%H:%M:%S"),
                         fill=t["HIGHLIGHT"], font=("Consolas", 8, "bold"), anchor="center")

    # ── CARDS ──────────────────────────────────────────────────────────
    def _left_card(self, t):
        x1, y1, x2, y2 = 10, 65, 210, 420
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        icon_weather(self, cx, cy-50)
        self.create_text(cx, cy+20, text="PLACA SOLAR",
                         fill=t["HIGHLIGHT"], font=("Consolas", 14, "bold"), anchor="center")
        self.create_line(cx-40, cy+35, cx+40, cy+35, fill=t["CINZAESCURO"], width=1)
        self.create_text(cx, cy+55, text="CARREGANDO",
                         fill=t["ACCENT"], font=("Consolas", 13, "bold"), anchor="center")
        self.create_text(cx, cy+80, text="PELO MODULO SOLAR",
                         fill=t["HIGHLIGHT"], font=("Consolas", 7), anchor="center")

    def _center_card(self, t):
        x1, y1, x2, y2 = 220, 60, 580, 440
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        r_outer, r_mid, r_inner, r_bar = 148, 134, 120, 104

        for i in range(16):
            self.create_arc(cx-r_outer, cy-r_outer, cx+r_outer, cy+r_outer,
                            start=self._angle+i*22.5, extent=10,
                            style="arc", outline=t["ACCENT"], width=3)

        self.create_oval(cx-r_mid, cy-r_mid, cx+r_mid, cy+r_mid,
                         fill="", outline=t["HIGHLIGHT"], width=1)

        for i in range(36):
            self.create_arc(cx-r_inner, cy-r_inner, cx+r_inner, cy+r_inner,
                            start=-self._angle*1.5+i*10, extent=4,
                            style="arc", outline=t["ACCENT_DARK"], width=5)

        self.create_oval(cx-r_bar, cy-r_bar, cx+r_bar, cy+r_bar,
                         fill="", outline=t["CINZA"], width=8)

        pw     = 8 + math.sin(self._pulse) * 2
        extent = (self._battery / 100.0) * 360
        self.create_arc(cx-r_bar, cy-r_bar, cx+r_bar, cy+r_bar,
                        start=90, extent=-extent,
                        style="arc", outline=t["ACCENT"], width=pw)

        self.create_text(cx-8, cy-25, text=f"{int(self._battery)}",
                         fill=t["HIGHLIGHT"], font=("Consolas", 58, "bold"), anchor="center")
        self.create_text(cx+48, cy-5, text="%",
                         fill=t["HIGHLIGHT"], font=("Consolas", 18, "bold"), anchor="center")
        self.create_text(cx, cy+32, text="BATERIA",
                         fill=t["HIGHLIGHT"], font=("Consolas", 18, "bold"), anchor="center")
        self.create_text(cx, cy+55, text="· toque para detalhes ·",
                         fill=t["CINZAESCURO"], font=("Consolas", 7), anchor="center")

    def _right_card(self, t):
        x1, y1, x2, y2 = 590, 65, 790, 420
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        icon_plug(self, cx, cy-50)
        self.create_text(cx, cy+20, text="DISPOSITIVO",
                         fill=t["HIGHLIGHT"], font=("Consolas", 14, "bold"), anchor="center")
        self.create_line(cx-40, cy+35, cx+40, cy+35, fill=t["CINZAESCURO"], width=1)
        self.create_text(cx, cy+55, text="CONECTADO",
                         fill=t["ACCENT"], font=("Consolas", 13, "bold"), anchor="center")
        self.create_text(cx, cy+80, text="CARREGANDO...",
                         fill=t["HIGHLIGHT"], font=("Consolas", 7), anchor="center")

    def _bottom_bar(self, t):
        W, H = self.W, self.H
        cx   = W // 2
        cy   = H - 28
        if self._time_to_full > 0:
            texto = f"{self._time_to_full} min para a carga total."
        elif self._status == "EM USO - DESCARREGANDO":
            texto = "Painel não está gerando energia suficiente."
        else:
            texto = "Bateria estabilizada."
        self.create_text(cx - 40, cy, text=texto,
                         fill=t["HIGHLIGHT"], font=("Consolas", 9, "bold"), anchor="center")
        self.create_line(30, cy, cx-150, cy, fill=t["CINZAESCURO"], width=1, dash=(4,3))
        self.create_line(cx+80, cy, W-100, cy, fill=t["CINZAESCURO"], width=1, dash=(4,3))
        self.create_oval(cx-155, cy-3, cx-145, cy+3, fill=t["CINZAESCURO"], outline="")
        self.create_oval(cx+75,  cy-3, cx+85,  cy+3, fill=t["CINZAESCURO"], outline="")