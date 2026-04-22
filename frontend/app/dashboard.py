# dashboard.py — Canvas principal do painel solar
# @author: Jhonatas de Oliveira
# @date: 21/04/2026
# @description: Este módulo define a classe SolarDashboard, que é responsável por desenhar o painel de controle do sistema de energia solar portátil. Ele utiliza o tkinter para criar uma interface gráfica com elementos animados e estilizados, como o status do sol, nível da bateria, status de saída, barra de tempo restante e um rodapé com data/hora, modo ativo e nível de bateria. O design é inspirado em um estilo neon futurista, usando cores vibrantes e efeitos de brilho para destacar as informações mais importantes. A classe também inclui uma função de animação que atualiza os elementos visuais a cada 80ms para criar uma experiência dinâmica e envolvente.
# @version: 1.0

import tkinter as tk
import math
from datetime import datetime
from theme import *
from draw  import neon_rect, neon_text, icon_calendar, icon_gear, icon_bars

# Classe principal do painel, desenha tudo e anima os elementos
class SolarDashboard(tk.Canvas):
    W, H = 800, 480

    def __init__(self, master, **kw):
        super().__init__(master, width=self.W, height=self.H,
                         bg=BG_DEEP, highlightthickness=0, bd=0)
        self._battery   = 78
        self._sun_angle = 0
        self._pulse     = 0
        self._draw_all()
        self._animate()

    # ── Animação ──────────────────────────────────────────────
    # Atualiza o ângulo do sol e o pulso para efeitos de animação, e redesenha tudo a cada 80ms
    def _animate(self):
        self._sun_angle = (self._sun_angle + 2) % 360
        self._pulse     = (self._pulse + 0.08) % (2 * math.pi)
        self._draw_all()
        self.after(80, self._animate)
    # ── Desenho ───────────────────────────────────────────────
    # Desenha o painel inteiro, chamando funções específicas para cada seção
    def _draw_all(self):
        self.delete("all")
        self._bg();         self._header()
        self._solar_card(); self._battery_card(); self._output_card()
        self._time_bar();   self._footer()

    # ── Fundo ─────────────────────────────────────────────────
    
    # Desenha o fundo com grid e bordas neon
    def _bg(self):
        W, H = self.W, self.H
        self.create_rectangle(0, 0, W, H, fill=BG_DEEP, outline="")
        for x in range(0, W, 40): self.create_line(x, 0, x, H, fill=MUTED, width=1)
        for y in range(0, H, 40): self.create_line(0, y, W, y, fill=MUTED, width=1)
        neon_rect(self, 4, 4, W-4, H-4, CYAN, radius=16, layers=3, width=2)
        s = 20
        # Cantos brilhantes
        for x, y, dx, dy in [(8,8,1,1),(W-8,8,-1,1),(8,H-8,1,-1),(W-8,H-8,-1,-1)]: 
            self.create_line(x, y, x+dx*s, y, fill=CYAN, width=2)
            self.create_line(x, y, x, y+dy*s, fill=CYAN, width=2)

    # ── Cabeçalho ─────────────────────────────────────────────
    # Desenha o título do painel com linhas e pontos neon
    def _header(self):
        cx = self.W // 2
        for xi in [30, cx-220, cx+220, self.W-30]:
            self.create_line(30, 50, cx-220, 50, fill=CYAN_DIM, width=1)
            self.create_oval(xi-3, 47, xi+3, 53, fill=CYAN, outline="")
        neon_text(self, cx, 38, "PAINEL DE ENERGIA SOLAR PORTÁTIL",
                  CYAN, ("Arial Black", 20, "bold"))
        self.create_text(cx, 52, text="PAINEL DE ENERGIA SOLAR PORTÁTIL",
                         fill=CYAN_DIM, font=("Arial Black", 8, "bold"), anchor="center")

    # ── Card Solar ────────────────────────────────────────────
    # Desenha o card de status solar, com um sol animado e um badge de status
    def _solar_card(self):
        x1, y1, x2, y2 = 25, 70, 255, 320
        cx = (x1+x2)//2
        self.create_rectangle(x1, y1, x2, y2, fill=BG_PANEL, outline="")
        neon_rect(self, x1, y1, x2, y2, YELLOW, radius=12, layers=3, width=2)
        self.create_text(cx, y1+22, text="SOLAR STATUS", fill=YELLOW, font=FONT_SMALL, anchor="center")
        self._sun(cx, (y1+y2)//2 - 20, 38)
        self._badge(x1, y2, cx, "ATIVO", GREEN, GREEN_DIM)

# Desenha o sol animado, com camadas de brilho e raios que giram
    def _sun(self, cx, cy, r):
        for i in range(5, 0, -1):
            sz = r * (0.5 + 0.5*(i/5))
            self.create_oval(cx-sz, cy-sz, cx+sz, cy+sz,
                             fill=YELLOW if i < 3 else "#ffaa00", outline="")
        for i in range(12):
            ang = math.radians(self._sun_angle + i * 30)
            r1, r2 = r+4, r+16+(4 if i%2==0 else 0)
            self.create_line(cx+r1*math.cos(ang), cy+r1*math.sin(ang),
                             cx+r2*math.cos(ang), cy+r2*math.sin(ang),
                             fill=YELLOW, width=3, capstyle="round")

    # ── Card Bateria ──────────────────────────────────────────
    # Desenha o card de status da bateria, com um medidor de nível e um badge de status
    def _battery_card(self):
        x1, y1, x2, y2 = 275, 70, 525, 320
        cx = (x1+x2)//2
        self.create_rectangle(x1, y1, x2, y2, fill=BG_PANEL, outline="")
        neon_rect(self, x1, y1, x2, y2, CYAN, radius=12, layers=3, width=2)
        self.create_text(cx, y1+22, text="BATERIA LEVEL", fill=CYAN, font=FONT_SMALL, anchor="center")
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

    # ── Card Output ───────────────────────────────────────────
        # Desenha o card de status de saída, com um ícone de plug animado e um badge de status
    def _output_card(self):
        x1, y1, x2, y2 = 545, 70, 775, 320
        cx = (x1+x2)//2
        self.create_rectangle(x1, y1, x2, y2, fill=BG_PANEL, outline="")
        neon_rect(self, x1, y1, x2, y2, ORANGE, radius=12, layers=3, width=2)
        self.create_text(cx, y1+22, text="OUTPUT STATUS", fill=ORANGE, font=FONT_SMALL, anchor="center")
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
        self.create_text(cx-70, cy, text="TEMPO RESTANTE", fill=WHITE, font=("Arial Black",12,"bold"), anchor="center")
        self.create_text(cx+50, cy, text="2h 30min",       fill=CYAN,  font=("Arial Black",18,"bold"), anchor="center")

    # ── Rodapé ────────────────────────────────────────────────
    # Desenha o rodapé com três seções: data/hora, modo ativo e nível de bateria, cada uma com um ícone e texto
    def _footer(self):
        now  = datetime.now()
        data = [
            (25,  388, 255, 460, icon_calendar, now.strftime("%d/%m/%Y"), now.strftime("%H:%M")),
            (275, 388, 525, 460, icon_gear,     "MODO",  "ATIVO"),
            (545, 388, 775, 460, icon_bars,     "NIVEL", f"{self._battery}%"),
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