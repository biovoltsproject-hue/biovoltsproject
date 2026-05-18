# main.py
# @author: Jhonatas de Oliveira, Ronalthy Vasques, Edson Lima, Yurhi Prestes, Luiz Gabriel
# @date: 21/04/2026
# @version: 1.1 — otimizado para tela 800x480

import sys
import os
import queue

import customtkinter as ctk

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)

from theme import BG_DEEP
from dashboard import SolarDashboard
from backend.models.sensor_backend import BioVoltsBackend

ctk.set_appearance_mode("dark")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BioVolts - Painel de Energia Solar Portátil")
        self.configure(fg_color=BG_DEEP)

        # Tela cheia sem barra do sistema operacional
       # self.attributes("-fullscreen", True)

        # Esconde o cursor (modo quiosque embarcado)
        self.config(cursor="none")

        self.data_queue = queue.Queue()

        self.backend = BioVoltsBackend(self.data_queue)
        self.backend.start()

        self.dashboard = SolarDashboard(self, self.data_queue)
        self.dashboard.pack(expand=True, fill="both")

        self.bind("<Escape>", lambda e: self._quit())
        self.protocol("WM_DELETE_WINDOW", self._quit)

    def _quit(self):
        self.backend.stop()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()