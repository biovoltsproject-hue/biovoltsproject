# main.py 
# @author: Jhonatas de Oliveira
# @author: Ronalthy Vasques
# @author: Edson Lima
# @author: Yurhi Prestes
# @author: Luiz Gabriel
# @date: 21/04/2026
# @description: Ponto de entrada da aplicação do painel de controle do sistema de energia solar portátil.
# @version: 1.0

import sys
import os
import queue

import customtkinter as ctk

# Adiciona a raiz do projeto ao path (duas pastas acima de frontend/app/)
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
        self.attributes("-fullscreen", False)

        # 1. Cria a fila de comunicação thread-safe
        self.data_queue = queue.Queue()

        # 2. Inicializa e inicia o Backend em background
        self.backend = BioVoltsBackend(self.data_queue)
        self.backend.start()

        # 3. Inicializa o Dashboard passando a fila
        self.dashboard = SolarDashboard(self, self.data_queue)
        self.dashboard.pack(expand=True)

        # Eventos de encerramento seguro
        self.bind("<Escape>", lambda e: self._quit())
        self.protocol("WM_DELETE_WINDOW", self._quit)

    def _quit(self):
        self.backend.stop()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()