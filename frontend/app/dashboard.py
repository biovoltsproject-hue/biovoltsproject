# dashboard.py — Canvas principal do painel solar
import tkinter as tk
import math
import random
from datetime import datetime
from theme import *
from draw import neon_poly, draw_panel_bg, neon_text, icon_weather, icon_plug, icon_clock, draw_battery_icon

class SolarDashboard(tk.Canvas):
    W, H = 1024, 600

    def __init__(self, master, **kw):
        super().__init__(master, width=self.W, height=self.H,
                         bg=BG_DEEP, highlightthickness=0, bd=0)
        self._battery   = 78.0
        self._battery_dir = 0.05
        self._angle     = 0
        self._pulse     = 0
        self._grid_offset = 0
        self._scan_y    = 0
        self._particles = [{"x": random.randint(0, self.W), "y": random.randint(0, self.H), "speed": random.uniform(1, 4), "len": random.randint(5, 20)} for _ in range(40)]
        self._draw_all()
        self._animate()

    def _animate(self):
        self._angle = (self._angle + 2) % 360
        self._pulse = (self._pulse + 0.1) % (2 * math.pi)
        self._grid_offset = (self._grid_offset + 0.5) % 64
        self._scan_y = (self._scan_y + 3) % self.H
        
        # Animação da bateria
        self._battery += self._battery_dir
        if self._battery >= 100:
            self._battery = 100
            self._battery_dir = -0.05
        elif self._battery <= 0:
            self._battery = 0
            self._battery_dir = 0.05

        for p in self._particles:
            p["y"] += p["speed"]
            if p["y"] > self.H:
                p["y"] = -20
                p["x"] = random.randint(0, self.W)
        self._draw_all()
        self.after(60, self._animate)

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
        
        # Borda principal com detalhes sci-fi
        cut = 30
        points = [
            cut, 12,
            W-cut, 12,
            W-12, cut,
            W-12, H-cut,
            W-cut, H-12,
            cut, H-12,
            12, H-cut,
            12, cut
        ]
        neon_poly(self, points, RED, layers=2, width=2)
        
        # Grade sutil (em movimento)
        go = int(self._grid_offset)
        for x in range(0, W + 64, 64): self.create_line(x - go, 0, x - go, H, fill=MUTED, width=1)
        for y in range(0, H + 64, 64): self.create_line(0, y - go, W, y - go, fill=MUTED, width=1)
        
        # Partículas de dados (Digital Rain)
        for p in self._particles:
            self.create_line(p["x"], p["y"], p["x"], p["y"] + p["len"], fill=RED_DARK, width=2)
            
        # Linha de Scanner / Radar
        self.create_line(0, self._scan_y, W, self._scan_y, fill=RED_DIM, width=2)
        self.create_line(0, self._scan_y - 3, W, self._scan_y - 3, fill=RED_DARK, width=1)

        # 1. Linhas de destaque brilhantes no topo e embaixo da borda principal
        self.create_line(W//2 - 80, 12, W//2 + 80, 12, fill=RED, width=5)
        self.create_line(W//2 - 30, 17, W//2 + 30, 17, fill=RED_DIM, width=2)
        
        self.create_line(W//2 - 80, H-12, W//2 + 80, H-12, fill=RED, width=5)
        self.create_line(W//2 - 30, H-17, W//2 + 30, H-17, fill=RED_DIM, width=2)
        
        # 2. Barras diagonais (///) nos cantos do painel
        for i in range(6):
            # Topo esquerdo
            self.create_line(60 + i*12, 30, 66 + i*12, 16, fill=RED_DIM, width=3)
            # Topo direito
            self.create_line(W - 130 + i*12, 30, W - 124 + i*12, 16, fill=RED_DIM, width=3)
            # Baixo esquerdo
            self.create_line(60 + i*12, H-16, 66 + i*12, H-30, fill=RED_DIM, width=3)
            # Baixo direito
            self.create_line(W - 130 + i*12, H-16, W - 124 + i*12, H-30, fill=RED_DIM, width=3)
            
        # 3. Pequenos grids de pontos (matrizes sci-fi) nas laterais
        for r in range(5):
            for c in range(2):
                # Esquerda superior e inferior
                self.create_oval(25 + c*8, 160 + r*8, 28 + c*8, 163 + r*8, fill=RED_DIM, outline="")
                self.create_oval(25 + c*8, 420 + r*8, 28 + c*8, 423 + r*8, fill=RED_DIM, outline="")
                # Direita superior e inferior
                self.create_oval(W - 40 + c*8, 160 + r*8, W - 37 + c*8, 163 + r*8, fill=RED_DIM, outline="")
                self.create_oval(W - 40 + c*8, 420 + r*8, W - 37 + c*8, 423 + r*8, fill=RED_DIM, outline="")

    def _header(self):
        cx = self.W // 2
        # Linhas decorativas do topo
        self.create_line(60, 45, cx-220, 45, fill=RED_DIM, width=2)
        self.create_line(cx+220, 45, self.W-60, 45, fill=RED_DIM, width=2)
        
        self.create_oval(cx-220-5, 42, cx-220+5, 48, fill=RED, outline="")
        self.create_oval(cx+220-5, 42, cx+220+5, 48, fill=RED, outline="")
        
        # Colchetes decorativos [ ] ao redor do título
        self.create_text(cx-180, 40, text="[", fill=RED, font=FONT_TITLE, anchor="center")
        self.create_text(cx+180, 40, text="]", fill=RED, font=FONT_TITLE, anchor="center")
            
        neon_text(self, cx, 40, "PAINEL SOLAR", WHITE, FONT_TITLE)
        self.create_text(cx, 80, text="SISTEMA DE ENERGIA PORTÁTIL", fill=RED, font=FONT_SUBTITLE, anchor="center")
        
        # Micro textos decorativos
        self.create_text(60, 25, text="SYS.ON // V1.0", fill=RED_DARK, font=FONT_MICRO, anchor="w")
        self.create_text(self.W-60, 25, text="PWR.RDY", fill=RED_DARK, font=FONT_MICRO, anchor="e")

    def _left_card(self):
        x1, y1, x2, y2 = 40, 120, 290, 480
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        draw_panel_bg(self, x1, y1, x2, y2, cut=25)
        
        icon_weather(self, cx, cy - 50)
        self.create_text(cx, cy + 30, text="CLIMA", fill=RED, font=FONT_MED, anchor="center")
        
        self.create_text(cx, cy + 80, text="32°C", fill=WHITE, font=("Consolas", 32, "bold"), anchor="center")
        self.create_text(cx, cy + 115, text="ENSOLARADO", fill=RED_DIM, font=FONT_MICRO, anchor="center")

        # Linha decorativa
        self.create_line(cx-50, cy+55, cx+50, cy+55, fill=RED_DIM, width=2)

    def _center_card(self):
        x1, y1, x2, y2 = 320, 120, 704, 480
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        draw_panel_bg(self, x1, y1, x2, y2, cut=30)
        
        r_outer = 175
        r_mid   = 160
        r_inner = 145
        r_bar   = 125
        
        # 1. Aro tracejado externo giratório
        for i in range(16):
            start = self._angle + i * 22.5
            self.create_arc(cx-r_outer, cy-r_outer, cx+r_outer, cy+r_outer, 
                            start=start, extent=10, style="arc", outline=RED, width=4)
        
        # 2. Aro sólido brilhante intermediário
        self.create_oval(cx-r_mid, cy-r_mid, cx+r_mid, cy+r_mid, fill="", outline=RED_DIM, width=2)
        
        # 3. Pequenos ticks internos girando ao contrário
        for i in range(36):
            start = -self._angle * 1.5 + i * 10
            self.create_arc(cx-r_inner, cy-r_inner, cx+r_inner, cy+r_inner, 
                            start=start, extent=4, style="arc", outline=RED_DARK, width=6)
                            
        # 4. Aro interno de fundo para a bateria
        self.create_oval(cx-r_bar, cy-r_bar, cx+r_bar, cy+r_bar, fill="", outline=RED_DIM, width=10)
        
        # 5. Aro preenchido da bateria (pulsando)
        pw = 10 + math.sin(self._pulse)*2
        extent = (self._battery / 100.0) * 360
        self.create_arc(cx-r_bar, cy-r_bar, cx+r_bar, cy+r_bar, 
                        start=90, extent=-extent, style="arc", outline=RED, width=pw)

        # Informações Centrais
        self.create_text(cx, cy - 35, text=f"{int(self._battery)}%", fill=WHITE, font=FONT_LARGE, anchor="center")
        self.create_text(cx, cy + 40, text="BATERIA", fill=RED, font=FONT_MED, anchor="center")
        
        draw_battery_icon(self, cx, cy + 90, self._battery)

    def _right_card(self):
        x1, y1, x2, y2 = 734, 120, 984, 480
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        draw_panel_bg(self, x1, y1, x2, y2, cut=25)
        
        icon_plug(self, cx, cy - 50)
        self.create_text(cx, cy + 30, text="STATUS", fill=RED, font=FONT_MED, anchor="center")
        self.create_text(cx, cy + 80, text="CONECTADO", fill=WHITE, font=FONT_MED, anchor="center")
        
        self.create_line(cx-50, cy+55, cx+50, cy+55, fill=RED_DIM, width=2)

    def _bottom_bar(self):
        x1, y1, x2, y2 = 250, 500, 774, 580
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        draw_panel_bg(self, x1, y1, x2, y2, cut=20)
        
        icon_cx = cx - 160
        icon_clock(self, icon_cx, cy)
        
        self.create_text(cx - 50, cy, text="HORA", fill=RED, font=FONT_MED, anchor="center")
        
        now = datetime.now()
        self.create_text(cx + 80, cy, text=now.strftime("%H:%M:%S"), fill=WHITE, font=("Consolas", 28, "bold"), anchor="center")
        
        self.create_line(x1+40, cy, icon_cx-50, cy, fill=RED_DIM, width=2, dash=(6,4))
        self.create_line(cx+210, cy, x2-40, cy, fill=RED_DIM, width=2, dash=(6,4))
        
        self.create_oval(icon_cx-55, cy-3, icon_cx-45, cy+3, fill=RED, outline="")
        self.create_oval(cx+205, cy-3, cx+215, cy+3, fill=RED, outline="")