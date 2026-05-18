# dashboard.py — Canvas principal do painel solar
import tkinter as tk
import math
import random
import queue
from datetime import datetime
from theme import *
from draw import *


class SolarDashboard(tk.Canvas):
    W, H = 1024, 600

    def __init__(self, master, data_queue, **kw):
        super().__init__(master, width=self.W, height=self.H,
                         bg=BG_DEEP, highlightthickness=0, bd=0)
        self.data_queue = data_queue

        # Estado interno de dados (alimentado pelo backend)
        self._battery = 0.0
        self._status = "AGUARDANDO SINAL..."
        self._time_to_full = 0

        # Estado de animação puramente visual
        self._angle = 0
        self._pulse = 0
        self._grid_offset = 0
        self._scan_y = 0
        self._particles = [
            {
                "x": random.randint(0, self.W),
                "y": random.randint(0, self.H),
                "speed": random.uniform(1, 4),
                "len": random.randint(5, 20),
            }
            for _ in range(40)
        ]

        self._draw_all()
        self._animate_visuals()
        self._poll_backend_data()

    def _poll_backend_data(self):
        """Lê os dados do backend sem bloquear a interface."""
        try:
            data = self.data_queue.get_nowait()
            self._battery = data.get("battery", self._battery)
            self._status = data.get("status", self._status)
            self._time_to_full = data.get("time_to_full", 0)
        except queue.Empty:
            pass
        self.after(200, self._poll_backend_data)

    def _animate_visuals(self):
        """Cuida estritamente dos efeitos cosméticos (giros, luzes)."""
        self._angle = (self._angle + 2) % 360
        self._pulse = (self._pulse + 0.1) % (2 * math.pi)
        self._grid_offset = (self._grid_offset + 0.5) % 64
        self._scan_y = (self._scan_y + 3) % self.H

        for p in self._particles:
            p["y"] += p["speed"]
            if p["y"] > self.H:
                p["y"] = -20
                p["x"] = random.randint(0, self.W)

        self._draw_all()
        self.after(60, self._animate_visuals)

    def _draw_all(self):
        self.delete("all")
        self._bg()
        self._header()
        self._left_card()
        self._center_card()
        self._right_card()
        self._top_bar_clock()
        self._bottom_bar()

    def _bg(self):
        W, H = self.W, self.H
        self.create_rectangle(0, 0, W, H, fill=BG_DEEP, outline="")

        # Partículas de dados (Digital Rain)
        for p in self._particles:
            self.create_line(p["x"], p["y"], p["x"], p["y"] + p["len"],
                             fill=DARKCINZA, width=2)

        # Linhas de destaque no topo e embaixo
        self.create_line(W // 2 - 80, 12, W // 2 + 80, 12, fill=WHITE, width=5)
        self.create_line(W // 2 - 30, 17, W // 2 + 30, 17, fill=WHITE, width=2)
        self.create_line(W // 2 - 80, H - 12, W // 2 + 80, H - 12, fill=WHITE, width=5)
        self.create_line(W // 2 - 30, H - 17, W // 2 + 30, H - 17, fill=WHITE, width=2)

        # Barras diagonais nos cantos
        for i in range(6):
            self.create_line(60 + i * 12, 30, 66 + i * 12, 16, fill=CINZAESCURO, width=3)
            self.create_line(W - 130 + i * 12, 30, W - 124 + i * 12, 16, fill=CINZAESCURO, width=3)
            self.create_line(60 + i * 12, H - 16, 66 + i * 12, H - 30, fill=CINZAESCURO, width=3)
            self.create_line(W - 130 + i * 12, H - 16, W - 124 + i * 12, H - 30, fill=CINZAESCURO, width=3)

        # Grids de pontos nas laterais
        for r in range(5):
            for c in range(2):
                self.create_oval(25 + c * 8, 160 + r * 8, 28 + c * 8, 163 + r * 8, fill=CINZA, outline="")
                self.create_oval(25 + c * 8, 420 + r * 8, 28 + c * 8, 423 + r * 8, fill=CINZA, outline="")
                self.create_oval(W - 40 + c * 8, 160 + r * 8, W - 37 + c * 8, 163 + r * 8, fill=CINZA, outline="")
                self.create_oval(W - 40 + c * 8, 420 + r * 8, W - 37 + c * 8, 423 + r * 8, fill=CINZA, outline="")

    def _header(self):
        cx = self.W // 2
        self.create_line(60, 45, cx - 220, 45, fill=CINZAESCURO, width=2)
        self.create_line(cx + 220, 45, self.W - 60, 45, fill=CINZAESCURO, width=2)
        self.create_oval(cx - 220 - 5, 42, cx - 220 + 5, 48, fill=CINZAESCURO, outline="")
        self.create_oval(cx + 220 - 5, 42, cx + 220 + 5, 48, fill=CINZAESCURO, outline="")
        self.create_text(cx - 180, 40, text="[", fill=CINZAESCURO, font=FONT_TITLE, anchor="center")
        self.create_text(cx + 180, 40, text="]", fill=CINZAESCURO, font=FONT_TITLE, anchor="center")
        neon_text(self, cx - 50, 40, "Bio", GREEN, FONTEFINA)
        neon_text(self, cx + 30, 40, "Volts", VERDE_ESCURO, FONT_TITLE)
        self.create_text(cx, 70, text="SUA ENERGIA SOLAR PORTÁTIL",
                         fill=WHITE, font=FONT_SUBTITLE, anchor="center")

    def _left_card(self):
        x1, y1, x2, y2 = 40, 120, 290, 480
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        icon_weather(self, cx, cy - 50)
        self.create_text(cx, cy + 30, text="PLACA SOLAR", fill=WHITE, font=FONT_MED, anchor="center")
        self.create_text(cx, cy + 80, text="CARREGANDO", fill=GREEN, font=FONT_MED, anchor="center")
        self.create_text(cx, cy + 115, text="CARREGANDO PELO MODULO SOLAR",
                         fill=WHITE, font=FONT_MICRO, anchor="center")
        self.create_line(cx - 50, cy + 55, cx + 50, cy + 55, fill=CINZAESCURO, width=1)

    def _center_card(self):
        x1, y1, x2, y2 = 320, 120, 704, 480
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        r_outer = 175
        r_mid = 160
        r_inner = 145
        r_bar = 125

        # Aro tracejado externo giratório
        for i in range(16):
            start = self._angle + i * 22.5
            self.create_arc(cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer,
                            start=start, extent=10, style="arc", outline=GREEN, width=4)

        # Aro sólido brilhante intermediário
        self.create_oval(cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid,
                         fill="", outline=WHITE, width=2)

        # Ticks internos girando ao contrário
        for i in range(36):
            start = -self._angle * 1.5 + i * 10
            self.create_arc(cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner,
                            start=start, extent=4, style="arc", outline=VERDE_ESCURO, width=6)

        # Aro interno de fundo para a bateria
        self.create_oval(cx - r_bar, cy - r_bar, cx + r_bar, cy + r_bar,
                         fill="", outline=CINZA, width=10)

        # Aro preenchido da bateria (pulsando)
        pw = 10 + math.sin(self._pulse) * 2
        extent = (self._battery / 100.0) * 360
        self.create_arc(cx - r_bar, cy - r_bar, cx + r_bar, cy + r_bar,
                        start=90, extent=-extent, style="arc", outline=GREEN, width=pw)

        # Informações Centrais
        self.create_text(cx - 10, cy - 35, text=f"{int(self._battery)}",
                         fill=WHITE, font=FONT_LARGE, anchor="center")
        self.create_text(cx, cy + 40, text="BATERIA", fill=WHITE, font=FONT_MED, anchor="center")
        self.create_text(cx + 55, cy - 12, text="%", fill=WHITE, font=FONT_MED, anchor="center")

    def _right_card(self):
        x1, y1, x2, y2 = 734, 120, 984, 480
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        icon_plug(self, cx, cy - 50)
        self.create_text(cx, cy + 30, text="DISPOSITIVO", fill=WHITE, font=FONT_MED, anchor="center")
        self.create_text(cx, cy + 80, text="CONECTADO", fill=GREEN, font=FONT_MED, anchor="center")
        self.create_text(cx, cy + 115, text="CARREGANDO...", fill=WHITE, font=FONT_MICRO, anchor="center")
        self.create_line(cx - 50, cy + 55, cx + 50, cy + 55, fill=CINZAESCURO, width=1)

    def _top_bar_clock(self):
        x1, y1, x2, y2 = -470, -530, 774, 580
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        icon_clock(self, cx, cy)
        now = datetime.now()
        self.create_text(cx + 50, cy, text=now.strftime("%H:%M:%S"),
                         fill=WHITE, font=("Consolas", 10, "bold"), anchor="center")

    def _bottom_bar(self):
        x1, y1, x2, y2 = 100, 500, 774, 580
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # CORREÇÃO: removido o texto hardcoded "49 min para a carga total."
        # que sobrescrevia o texto dinâmico logo abaixo
        if self._time_to_full > 0:
            texto_tempo = f"{self._time_to_full} min para a carga total."
        elif self._status == "EM USO - DESCARREGANDO":
            texto_tempo = "Painel não está gerando energia suficiente."
        else:
            texto_tempo = "Bateria estabilizada."

        self.create_text(cx + 80, cy, text=texto_tempo,
                         fill=WHITE, font=("Consolas", 12, "bold"), anchor="center")

        self.create_line(x1 - 100, cy, cx - 50, cy, fill=CINZAESCURO, width=2, dash=(6, 4))
        self.create_line(cx + 600, cy, x2 - 120, cy, fill=CINZAESCURO, width=2, dash=(6, 4))
        self.create_oval(cx - 55, cy - 3, cx - 45, cy + 3, fill=CINZAESCURO, outline="")
        self.create_oval(cx + 205, cy - 3, cx + 215, cy + 3, fill=CINZAESCURO, outline="")