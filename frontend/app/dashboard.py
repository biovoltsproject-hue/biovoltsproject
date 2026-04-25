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
<<<<<<< HEAD
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
=======
        for xi in [30, cx-220, cx+220, self.W-30]:
            self.create_line(30, 50, cx-220, 50, fill=CYAN_DIM, width=1)
            self.create_oval(xi-3, 47, xi+3, 53, fill=CYAN, outline="")
        neon_text(self, cx, 38, "MALETA SOLAR BIOVOLTS", #Mudança no nome do painel
                  CYAN, ("Arial Black", 20, "bold"))
        #Autor: Edson.
        # As duas linhas abaixo estão duplicando o texto do embaixo do título.
        #self.create_text(cx, 52, text="PAINEL DE ENERGIA SOLAR PORTÁTIL",
                         #fill=CYAN_DIM, font=("Arial Black", 8, "bold"), anchor="center")
>>>>>>> 82d820968552e07e2f28e8a23b7f1331f1a63ae4

    def _left_card(self):
        x1, y1, x2, y2 = 40, 120, 290, 480
        cx = (x1+x2)//2
<<<<<<< HEAD
        cy = (y1+y2)//2
        draw_panel_bg(self, x1, y1, x2, y2, cut=25)
        
        icon_weather(self, cx, cy - 50)
        self.create_text(cx, cy + 30, text="CLIMA", fill=RED, font=FONT_MED, anchor="center")
        
        self.create_text(cx, cy + 80, text="32°C", fill=WHITE, font=("Consolas", 32, "bold"), anchor="center")
        self.create_text(cx, cy + 115, text="ENSOLARADO", fill=RED_DIM, font=FONT_MICRO, anchor="center")
=======
        self.create_rectangle(x1, y1, x2, y2, fill=BG_PANEL, outline="")
        neon_rect(self, x1, y1, x2, y2, YELLOW, radius=12, layers=3, width=2)
        self.create_text(cx, y1+22, text="STATUS SOLAR", fill=YELLOW, font=FONT_SMALL, anchor="center") #mudança em SOLAR STATUS para STATUS SOLAR
        self._sun(cx, (y1+y2)//2 - 20, 38)
        self._badge(x1, y2, cx, "ATIVO", GREEN, GREEN_DIM)
>>>>>>> 82d820968552e07e2f28e8a23b7f1331f1a63ae4

        # Linha decorativa
        self.create_line(cx-50, cy+55, cx+50, cy+55, fill=RED_DIM, width=2)

    def _center_card(self):
        x1, y1, x2, y2 = 320, 120, 704, 480
        cx = (x1+x2)//2
<<<<<<< HEAD
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
=======
        self.create_rectangle(x1, y1, x2, y2, fill=BG_PANEL, outline="")
        neon_rect(self, x1, y1, x2, y2, CYAN, radius=12, layers=3, width=2)
        #mudança em BATERIA LEVEL para PORCENTAGEM DE BATERIA
        self.create_text(cx, y1+22, text="BATERIA", fill=CYAN, font=FONT_SMALL, anchor="center")
        neon_text(self, cx, (y1+y2)//2-30, f"{self._battery}%",
                  WHITE, ("Arial Black", 52, "bold"))
        self._battery_bar(cx, y2-45, 180, 32)
    # Desenha a barra de bateria, com preenchimento proporcional ao nível e um ícone de raio
    def _battery_bar(self, cx, cy, bw, bh):
        x1, y1 = cx-bw//2, cy-bh//2
        x2, y2 = cx+bw//2, cy+bh//2
        self.create_rectangle(x1, y1, x2, y2, fill="#001a0a", outline="")
        neon_rect(self, x1, y1, x2, y2, GREEN, radius=5, layers=2, width=2)
        self.create_rectangle(x2, cy-8, x2+10, cy+8, fill=GREEN_DIM, outline=GREEN, width=1)
        fw = int((bw-8) * self._battery / 100)
        self.create_rectangle(x1+4, y1+4, x1+4+fw, y2-4, fill=GREEN, outline="")
        self.create_rectangle(x1+4, y1+4, x1+4+fw, y1+10, fill="#aaffcc", outline="")
        bolt = [(cx+4,cy-10),(cx-2,cy-2),(cx+2,cy-2),(cx-4,cy+10),(cx+3,cy+1),(cx-1,cy+1)]
        self.create_polygon(bolt, fill=WHITE, outline="")
>>>>>>> 82d820968552e07e2f28e8a23b7f1331f1a63ae4

        # Informações Centrais
        self.create_text(cx, cy - 35, text=f"{int(self._battery)}%", fill=WHITE, font=FONT_LARGE, anchor="center")
        self.create_text(cx, cy + 40, text="BATERIA", fill=RED, font=FONT_MED, anchor="center")
        
        draw_battery_icon(self, cx, cy + 90, self._battery)

    def _right_card(self):
        x1, y1, x2, y2 = 734, 120, 984, 480
        cx = (x1+x2)//2
<<<<<<< HEAD
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
=======
        self.create_rectangle(x1, y1, x2, y2, fill=BG_PANEL, outline="")
        neon_rect(self, x1, y1, x2, y2, ORANGE, radius=12, layers=3, width=2)
        #Mudança em OUTPUT STATUS para STATUS DA SAÍDA
        self.create_text(cx, y1+22, text=" STATUS DA SAÍDA", fill=ORANGE, font=FONT_SMALL, anchor="center")
        self._plug(cx, (y1+y2)//2 - 18)
        self._badge(x1, y2, cx, "CONECTADO", ORANGE, ORANGE_DIM, font_size=13)

    # Desenha o ícone de plug animado, com círculos de pulso e linhas de energia que se estendem para fora do plug
    def _plug(self, cx, cy):
        pr = 38 + int(6*math.sin(self._pulse))
        for r in range(pr, pr-12, -4):
            self.create_oval(cx-r, cy-r, cx+r, cy+r, fill="", outline=ORANGE_DIM, width=1)
        pw, ph = 34, 44
        self.create_rectangle(cx-pw//2, cy-ph//2, cx+pw//2, cy-ph//2+22, fill=ORANGE_DIM, outline=ORANGE, width=2)
        for px in [cx-10, cx+10]:
            self.create_rectangle(px-4, cy-ph//2-14, px+4, cy-ph//2, fill=ORANGE, outline="")
        self.create_rectangle(cx-6, cy-ph//2+22, cx+6, cy+ph//2+8, fill=ORANGE_DIM, outline=ORANGE, width=2)
        for ang in [-45, 45, -135, 135]:
            a = math.radians(ang)
            self.create_line(cx+44*math.cos(a), cy+44*math.sin(a),
                             cx+58*math.cos(a), cy+58*math.sin(a),
                             fill=ORANGE, width=2, dash=(4,3))

    # ── Helper badge ──────────────────────────────────────────
    # Desenha um badge de status com fundo neon e texto centralizado, usado nos cards de solar e output
    def _badge(self, x1, y2, cx, text, color, dim, font_size=14):
        bx1, bx2 = x1+20, x1+210
        by1, by2 = y2-52, y2-22
        self.create_rectangle(bx1, by1, bx2, by2, fill=dim, outline="")
        neon_rect(self, bx1, by1, bx2, by2, color, radius=6, layers=2, width=2)
        self.create_text(cx, (by1+by2)//2, text=text,
                         fill=color, font=("Arial Black", font_size, "bold"), anchor="center")

    # ── Barra de tempo ────────────────────────────────────────
    # Desenha a barra de tempo restante, com linhas de divisão e um texto centralizado que mostra o tempo restante
    def _time_bar(self):
        W = self.W
        x1, y1, x2, y2 = 160, 334, W-160, 374
        cx, cy = (x1+x2)//2, (y1+y2)//2
        self.create_rectangle(x1, y1, x2, y2, fill=BG_PANEL, outline="")
        neon_rect(self, x1, y1, x2, y2, CYAN, radius=8, layers=2, width=2)
        for xi, x2_ in [(30, x1), (x2, W-30)]:
            self.create_line(xi, cy, x2_, cy, fill=CYAN_DIM, width=1, dash=(4,4))
            self.create_oval(xi-4, cy-4, xi+4, cy+4, fill=CYAN, outline="")
            #Autor Edson
            #Espaçamento de "Tempo Restante" e "2h 30min" aumentada,
            #Não estando mais tão próximas uma da outra.
        self.create_text(cx-100, cy, text="TEMPO RESTANTE:", fill=WHITE, font=("Arial Black",12,"bold"), anchor="center")
        self.create_text(cx+80, cy, text="2h 30min",       fill=CYAN,  font=("Arial Black",18,"bold"), anchor="center")

    # ── Rodapé ────────────────────────────────────────────────
    # Desenha o rodapé com três seções: data/hora, modo ativo e nível de bateria, cada uma com um ícone e texto
    def _footer(self):
        now  = datetime.now()
        data = [
            (25,  388, 255, 460, icon_calendar, now.strftime("%d/%m/%Y"), now.strftime("%H:%M")),
            (275, 388, 525, 460, icon_gear,     "MODO",  "ATIVO"),
            (545, 388, 775, 460, icon_bars,     "BATERIA", f"{self._battery}%"),
        ]
        # Para cada seção do rodapé, desenha um retângulo de fundo, um ícone, uma linha divisória e o texto correspondente
        for x1, y1, x2, y2, icon_fn, label, value in data:
            cx, cy = (x1+x2)//2, (y1+y2)//2
            ix = x1 + 38
            self.create_rectangle(x1, y1, x2, y2, fill=BG_PANEL, outline="")
            neon_rect(self, x1, y1, x2, y2, CYAN_DIM, radius=8, layers=1, width=1)
            icon_fn(self, ix, cy)
            self.create_line(ix+22, y1+12, ix+22, y2-12, fill=CYAN_DIM, width=1)
            self.create_text(cx+20, cy-12, text=label, fill=TEXT_DIM, font=("Arial Black",10,"bold"), anchor="center")
            self.create_text(cx+20, cy+12, text=value,  fill=CYAN,     font=("Arial Black",14,"bold"), anchor="center")
>>>>>>> 82d820968552e07e2f28e8a23b7f1331f1a63ae4
