# draw.py — Funções de desenho neon e ícones
# 
# @date: 21/04/2026
# @description: Este módulo define funções para desenhar elementos neon e ícones em uma interface gráfica tkinter.
# @version: 1.0


import math
from theme import *


def neon_rect(canvas, x1, y1, x2, y2, color, radius=10, layers=4, width=2):
    for i in range(layers, 0, -1):
        off = i * 2
        _rrect(canvas, x1-off, y1-off, x2+off, y2+off, radius+off//2, color, width=1)
    _rrect(canvas, x1, y1, x2, y2, radius, color, width=width)

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

def neon_text(canvas, x, y, text, color, font, anchor="center"):
    for dx, dy in [(2,2),(-2,-2),(2,-2),(-2,2),(0,3),(0,-3),(3,0),(-3,0)]:
        canvas.create_text(x+dx, y+dy, text=text, fill=BG_DEEP, font=font, anchor=anchor)
    canvas.create_text(x, y, text=text, fill=color, font=font, anchor=anchor)

def icon_calendar(canvas, cx, cy):
    w, h = 28, 26
    x1, y1 = cx-w//2, cy-h//2
    canvas.create_rectangle(x1, y1, x1+w, y1+h, fill="", outline=CYAN, width=2)
    canvas.create_rectangle(x1, y1, x1+w, y1+8, fill=CYAN_DIM, outline=CYAN, width=1)
    for gx in [x1+7, x1+14, x1+21]:
        for gy in [y1+13, y1+19]:
            canvas.create_rectangle(gx-2, gy-2, gx+2, gy+2, fill=CYAN, outline="")

def icon_gear(canvas, cx, cy):
    r_out, r_in, teeth = 14, 9, 8
    for i in range(teeth):
        a1 = math.radians(i * 360/teeth)
        a2 = math.radians(i * 360/teeth + 15)
        canvas.create_line(cx+r_in*math.cos(a1), cy+r_in*math.sin(a1),
                           cx+r_out*math.cos(a1), cy+r_out*math.sin(a1),
                           fill=CYAN, width=3)
        canvas.create_line(cx+r_out*math.cos(a1), cy+r_out*math.sin(a1),
                           cx+r_out*math.cos(a2), cy+r_out*math.sin(a2),
                           fill=CYAN, width=3)
    canvas.create_oval(cx-r_in, cy-r_in, cx+r_in, cy+r_in, fill=BG_PANEL, outline=CYAN, width=2)
    canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill=CYAN, outline="")

def icon_bars(canvas, cx, cy):
    for ox, h in [(0,18),(8,12),(16,7),(24,3)]:
        bx, by = cx-12+ox, cy+10
        canvas.create_rectangle(bx, by-h, bx+5, by, fill=CYAN, outline="")