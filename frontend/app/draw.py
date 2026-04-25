# draw.py — Funções de desenho neon e ícones para o tema Cyberpunk Red
import math
from theme import *

def neon_poly(canvas, points, color, layers=2, width=2):
    canvas.create_polygon(points, fill="", outline=RED_DIM, width=width+3)
    canvas.create_polygon(points, fill="", outline=color, width=width)

def draw_panel_bg(canvas, x1, y1, x2, y2, cut=25):
    points = [
        x1+cut, y1,
        x2-cut, y1,
        x2, y1+cut,
        x2, y2-cut,
        x2-cut, y2,
        x1+cut, y2,
        x1, y2-cut,
        x1, y1+cut
    ]
    canvas.create_polygon(points, fill=BG_PANEL, outline="")
    neon_poly(canvas, points, RED, layers=1, width=2)
    
    # Detalhes decorativos nos cantos (dots e cruzes)
    s = 8
    for px, py in [(x1+cut, y1-s), (x2-cut, y1-s), (x1+cut, y2+s), (x2-cut, y2+s)]:
        canvas.create_oval(px-2, py-2, px+2, py+2, fill=RED, outline="")
        
    # Crosshairs internos
    ch = 15
    canvas.create_line(x1+cut+5, y1+5, x1+cut+5+ch, y1+5, fill=RED_DIM, width=2)
    canvas.create_line(x1+5, y1+cut+5, x1+5, y1+cut+5+ch, fill=RED_DIM, width=2)
    
    canvas.create_line(x2-cut-5, y2-5, x2-cut-5-ch, y2-5, fill=RED_DIM, width=2)
    canvas.create_line(x2-5, y2-cut-5, x2-5, y2-cut-5-ch, fill=RED_DIM, width=2)

def neon_text(canvas, x, y, text, color, font, anchor="center"):
    canvas.create_text(x+3, y+3, text=text, fill=BG_DEEP, font=font, anchor=anchor)
    canvas.create_text(x, y, text=text, fill=color, font=font, anchor=anchor)

def icon_circle(canvas, cx, cy, r):
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="", outline=RED_DIM, width=3)
    canvas.create_oval(cx-r-5, cy-r-5, cx+r+5, cy+r+5, fill="", outline=RED_DARK, width=1)

def icon_calendar(canvas, cx, cy):
    icon_circle(canvas, cx, cy, 50)
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
    icon_circle(canvas, cx, cy, 50)
    canvas.create_oval(cx-14, cy-14, cx+14, cy+14, fill="", outline=RED, width=3)
    for i in range(8):
        angle = i * (math.pi / 4)
        x1 = cx + math.cos(angle) * 20
        y1 = cy + math.sin(angle) * 20
        x2 = cx + math.cos(angle) * 28
        y2 = cy + math.sin(angle) * 28
        canvas.create_line(x1, y1, x2, y2, fill=RED, width=3)


def icon_plug(canvas, cx, cy):
    icon_circle(canvas, cx, cy, 50)
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
    icon_circle(canvas, cx, cy, 35)
    canvas.create_oval(cx-24, cy-24, cx+24, cy+24, fill="", outline=RED, width=3)
    canvas.create_line(cx, cy, cx, cy-12, fill=RED, width=3)
    canvas.create_line(cx, cy, cx+10, cy+6, fill=RED, width=3)
    canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill=RED, outline="")

def draw_battery_icon(canvas, cx, cy, percentage):
    w, h = 90, 36
    x1, y1 = cx-w//2, cy-h//2
    canvas.create_rectangle(x1, y1, x1+w, y1+h, fill="", outline=RED, width=3)
    canvas.create_rectangle(x1+w, cy-8, x1+w+6, cy+8, fill=RED, outline="")
    bars = 5
    bar_w = (w - 8 - (bars-1)*3) / bars
    active_bars = int((percentage / 100) * bars)
    for i in range(bars):
        bx1 = x1 + 4 + i*(bar_w + 3)
        if i < active_bars:
            canvas.create_rectangle(bx1, y1+4, bx1+bar_w, y1+h-4, fill=WHITE, outline="")
        else:
            canvas.create_rectangle(bx1, y1+4, bx1+bar_w, y1+h-4, fill=RED_DARK, outline="")