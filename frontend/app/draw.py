# draw.py — Funções de desenho neon e ícones para o tema Cyberpunk Red
import math
from theme import *


# Função para desenhar um retângulo com efeito neon
def neon_rect(canvas, x1, y1, x2, y2, color, radius=10, layers=4, width=2): 
    for i in range(layers, 0, -1):
        off = i * 2
        _rrect(canvas, x1-off, y1-off, x2+off, y2+off, radius+off//2, color, width=1)
    _rrect(canvas, x1, y1, x2, y2, radius, color, width=width)
    
# Função auxiliar para desenhar um retângulo arredondado
def _rrect(canvas, x1, y1, x2, y2, r, color, width=2):
    r = min(r, (x2-x1)//2, (y2-y1)//2)
    for (ax,ay,bx,by), start in [
        ((x1,y1,x1+2*r,y1+2*r), 90), ((x2-2*r,y1,x2,y1+2*r), 0),
        ((x2-2*r,y2-2*r,x2,y2), 270), ((x1,y2-2*r,x1+2*r,y2), 180)
    ]:
        canvas.create_arc(ax,ay,bx,by, start=start, extent=90,
                          style="arc", outline=color, width=width)
    canvas.create_line(x1+r,y1, x2-r,y1, fill=color, width=width)
    canvas.create_line(x1+r,y2, x2-r,y2, fill=color, width=width)
    canvas.create_line(x1,y1+r, x1,y2-r, fill=color, width=width)
    canvas.create_line(x2,y1+r, x2,y2-r, fill=color, width=width)
# Função para desenhar texto com efeito neon
def neon_text(canvas, x, y, text, color, font, anchor="center"):
    canvas.create_text(x+3, y+3, text=text, fill=BG_DEEP, font=font, anchor=anchor)
    canvas.create_text(x, y, text=text, fill=color, font=font, anchor=anchor)
# Funções para desenhar ícones simples
def icon_calendar(canvas, cx, cy):
   
    w, h = 34, 30
    x1, y1 = cx-w//2, cy-h//2 + 3
    canvas.create_rectangle(x1, y1, x1+w, y1+h, fill="", outline=RED, width=3)
    canvas.create_line(x1, y1+8, x1+w, y1+8, fill=RED, width=3)
    canvas.create_line(cx-8, y1-6, cx-8, y1+3, fill=RED, width=3)
    canvas.create_line(cx+8, y1-6, cx+8, y1+3, fill=RED, width=3)
    for gx in [cx-8, cx, cx+8]:
        for gy in [y1+15, y1+23]:
            canvas.create_rectangle(gx-2, gy-2, gx+2, gy+2, fill=RED, outline="")

def icon_weather(canvas, cx, cy):
    canvas.create_oval(cx-10, cy-14, cx+14, cy+14, fill="", outline=RED, width=3)
    for i in range(8):
        angle = i * (math.pi / 4)
        x1 = cx + math.cos(angle) * 20
        y1 = cy + math.sin(angle) * 20
        x2 = cx + math.cos(angle) * 28
        y2 = cy + math.sin(angle) * 28
        canvas.create_line(x1, y1, x2, y2, fill=RED, width=3)


def icon_plug(canvas, cx, cy):
    pw, ph = 28, 22
    cy -= 3
    # Corpo
    pts = [cx-pw//2, cy-ph//2, cx+pw//2, cy-ph//2, cx+pw//2, cy+ph//2, cx+pw//4, cy+ph, cx-pw//4, cy+ph, cx-pw//2, cy+ph//2]
    canvas.create_polygon(pts, fill="", outline=RED, width=3)
    canvas.create_line(cx-pw//2, cy-ph//2+6, cx+pw//2, cy-ph//2+6, fill=RED, width=2)
    # Pinos
    canvas.create_line(cx-6, cy-ph//2, cx-6, cy-ph//2-12, fill=RED, width=3)
    canvas.create_line(cx+6, cy-ph//2, cx+6, cy-ph//2-12, fill=RED, width=3)
    # Fio
    canvas.create_line(cx, cy+ph, cx, cy+ph+16, fill=RED, width=3)

def icon_clock(canvas, cx, cy):
    canvas.create_oval(cx-10, cy-10, cx+10, cy+10, fill="", outline=RED, width=3)
    canvas.create_line(cx, cy, cx, cy-8, fill=RED, width=3)
    canvas.create_line(cx, cy, cx+10, cy+6, fill=RED, width=3)
    canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill=RED, outline="")
