# dashboard.py — Canvas principal do painel solar (otimizado para 800x480)
import tkinter as tk
import math
import random
import queue
from datetime import datetime
from theme import *
from draw import *


class SolarDashboard(tk.Canvas):
    W, H = 800, 480

    def __init__(self, master, data_queue, **kw):
        super().__init__(master, width=self.W, height=self.H,
                         bg=BG_DEEP, highlightthickness=0, bd=0)
        self.data_queue = data_queue

        self._battery = 0.0
        self._status = "AGUARDANDO SINAL..."
        self._time_to_full = 0

        self._angle = 0
        self._pulse = 0
        self._grid_offset = 0
        self._particles = [
            {
                "x": random.randint(0, self.W),
                "y": random.randint(0, self.H),
                "speed": random.uniform(1, 3),
                "len": random.randint(4, 15),
            }
            for _ in range(30)
        ]

        self._draw_all()
        self._animate_visuals()
        self._poll_backend_data()

    def _poll_backend_data(self):
        try:
            data = self.data_queue.get_nowait()
            self._battery = data.get("battery", self._battery)
            self._status = data.get("status", self._status)
            self._time_to_full = data.get("time_to_full", 0)
        except queue.Empty:
            pass
        self.after(200, self._poll_backend_data)

    def _animate_visuals(self):
        self._angle = (self._angle + 2) % 360
        self._pulse = (self._pulse + 0.1) % (2 * math.pi)

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
        self._bottom_bar()

    def _bg(self):
        W, H = self.W, self.H
        self.create_rectangle(0, 0, W, H, fill=BG_DEEP, outline="")

        for p in self._particles:
            self.create_line(p["x"], p["y"], p["x"], p["y"] + p["len"],
                             fill=DARKCINZA, width=1)

        # Linhas de destaque topo e base
        self.create_line(W//2 - 60, 8,  W//2 + 60, 8,  fill=WHITE, width=4)
        self.create_line(W//2 - 20, 12, W//2 + 20, 12, fill=WHITE, width=2)
        self.create_line(W//2 - 60, H-8,  W//2 + 60, H-8,  fill=WHITE, width=4)
        self.create_line(W//2 - 20, H-12, W//2 + 20, H-12, fill=WHITE, width=2)

        # Barras diagonais nos cantos
        for i in range(4):
            self.create_line(40 + i*10, 22, 45 + i*10, 12, fill=CINZAESCURO, width=2)
            self.create_line(W-80 + i*10, 22, W-75 + i*10, 12, fill=CINZAESCURO, width=2)
            self.create_line(40 + i*10, H-12, 45 + i*10, H-22, fill=CINZAESCURO, width=2)
            self.create_line(W-80 + i*10, H-12, W-75 + i*10, H-22, fill=CINZAESCURO, width=2)

        # Pontos decorativos laterais
        for r in range(4):
            for c in range(2):
                self.create_oval(12+c*7, 120+r*7, 15+c*7, 123+r*7, fill=CINZA, outline="")
                self.create_oval(12+c*7, 340+r*7, 15+c*7, 343+r*7, fill=CINZA, outline="")
                self.create_oval(W-26+c*7, 120+r*7, W-23+c*7, 123+r*7, fill=CINZA, outline="")
                self.create_oval(W-26+c*7, 340+r*7, W-23+c*7, 343+r*7, fill=CINZA, outline="")

    def _header(self):
        cx = self.W // 2

        # Linhas decorativas
        self.create_line(40, 32, cx-160, 32, fill=CINZAESCURO, width=1)
        self.create_line(cx+160, 32, self.W-40, 32, fill=CINZAESCURO, width=1)
        self.create_oval(cx-165, 29, cx-155, 35, fill=CINZAESCURO, outline="")
        self.create_oval(cx+155, 29, cx+165, 35, fill=CINZAESCURO, outline="")

        self.create_text(cx-130, 30, text="[", fill=CINZAESCURO,
                         font=("Montserrat", 18, "bold"), anchor="center")
        self.create_text(cx+130, 30, text="]", fill=CINZAESCURO,
                         font=("Montserrat", 18, "bold"), anchor="center")

        # Título
        neon_text(self, cx-30, 28, "Bio", GREEN,   ("Montserrat", 20))
        neon_text(self, cx+28, 28, "Volts", VERDE_ESCURO, ("Montserrat", 20, "bold"))
        self.create_text(cx, 50, text="SUA ENERGIA SOLAR PORTÁTIL",
                         fill=WHITE, font=("Montserrat", 8), anchor="center")

        # Relógio
        now = datetime.now()
        icon_clock(self, 28, 28)
        self.create_text(70, 28, text=now.strftime("%H:%M:%S"),
                         fill=WHITE, font=("Consolas", 8, "bold"), anchor="center")

    def _left_card(self):
        x1, y1, x2, y2 = 10, 65, 210, 420
        cx = (x1+x2)//2
        cy = (y1+y2)//2

        icon_weather(self, cx, cy - 50)

        self.create_text(cx, cy+20, text="PLACA SOLAR",
                         fill=WHITE, font=("Consolas", 14, "bold"), anchor="center")
        self.create_line(cx-40, cy+35, cx+40, cy+35, fill=CINZAESCURO, width=1)
        self.create_text(cx, cy+55, text="CARREGANDO",
                         fill=GREEN, font=("Consolas", 13, "bold"), anchor="center")
        self.create_text(cx, cy+80, text="PELO MODULO SOLAR",
                         fill=WHITE, font=("Consolas", 7), anchor="center")

    def _center_card(self):
        x1, y1, x2, y2 = 220, 60, 580, 440
        cx = (x1+x2)//2
        cy = (y1+y2)//2

        r_outer = 148
        r_mid   = 134
        r_inner = 120
        r_bar   = 104

        # Aro tracejado giratório
        for i in range(16):
            start = self._angle + i * 22.5
            self.create_arc(cx-r_outer, cy-r_outer, cx+r_outer, cy+r_outer,
                            start=start, extent=10, style="arc", outline=GREEN, width=3)

        # Aro intermediário
        self.create_oval(cx-r_mid, cy-r_mid, cx+r_mid, cy+r_mid,
                         fill="", outline=WHITE, width=1)

        # Ticks internos
        for i in range(36):
            start = -self._angle * 1.5 + i * 10
            self.create_arc(cx-r_inner, cy-r_inner, cx+r_inner, cy+r_inner,
                            start=start, extent=4, style="arc", outline=VERDE_ESCURO, width=5)

        # Aro de fundo da bateria
        self.create_oval(cx-r_bar, cy-r_bar, cx+r_bar, cy+r_bar,
                         fill="", outline=CINZA, width=8)

        # Aro preenchido (bateria)
        pw = 8 + math.sin(self._pulse) * 2
        extent = (self._battery / 100.0) * 360
        self.create_arc(cx-r_bar, cy-r_bar, cx+r_bar, cy+r_bar,
                        start=90, extent=-extent, style="arc", outline=GREEN, width=pw)

        # Texto central
        self.create_text(cx-8, cy-25, text=f"{int(self._battery)}",
                         fill=WHITE, font=("Consolas", 58, "bold"), anchor="center")
        self.create_text(cx+48, cy-5, text="%",
                         fill=WHITE, font=("Consolas", 18, "bold"), anchor="center")
        self.create_text(cx, cy+32, text="BATERIA",
                         fill=WHITE, font=("Consolas", 18, "bold"), anchor="center")

    def _right_card(self):
        x1, y1, x2, y2 = 590, 65, 790, 420
        cx = (x1+x2)//2
        cy = (y1+y2)//2

        icon_plug(self, cx, cy - 50)

        self.create_text(cx, cy+20, text="DISPOSITIVO",
                         fill=WHITE, font=("Consolas", 14, "bold"), anchor="center")
        self.create_line(cx-40, cy+35, cx+40, cy+35, fill=CINZAESCURO, width=1)
        self.create_text(cx, cy+55, text="CONECTADO",
                         fill=GREEN, font=("Consolas", 13, "bold"), anchor="center")
        self.create_text(cx, cy+80, text="CARREGANDO...",
                         fill=WHITE, font=("Consolas", 7), anchor="center")

    def _bottom_bar(self):
        W, H = self.W, self.H
        cx = W // 2
        cy = H - 28

        if self._time_to_full > 0:
            texto = f"{self._time_to_full} min para a carga total."
        elif self._status == "EM USO - DESCARREGANDO":
            texto = "Painel não está gerando energia suficiente."
        else:
            texto = "Bateria estabilizada."

        self.create_text(cx, cy, text=texto,
                         fill=WHITE, font=("Consolas", 9, "bold"), anchor="center")

        self.create_line(30, cy, cx-120, cy, fill=CINZAESCURO, width=1, dash=(4, 3))
        self.create_line(cx+120, cy, W-30, cy, fill=CINZAESCURO, width=1, dash=(4, 3))
        self.create_oval(cx-125, cy-3, cx-115, cy+3, fill=CINZAESCURO, outline="")
        self.create_oval(cx+115, cy-3, cx+125, cy+3, fill=CINZAESCURO, outline="")