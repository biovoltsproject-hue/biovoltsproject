# main.py 
# @author: Jhonatas de Oliveira
# @author: Ronalthy Vasques
# @author: Edson Lima
# @author: Yurhi Prestes
# @author: Luiz Gabriel
# @date: 21/04/2026
# @description: Este é o ponto de entrada para a aplicação do painel de controle do sistema de energia solar portátil. 
# Ele define a classe App, que é uma janela principal do tkinter configurada com um tema escuro e um layout fixo.
# A classe App instancia o SolarDashboard, que é o canvas principal onde todos os elementos visuais do painel são desenhados.
# O aplicativo é iniciado chamando a função mainloop() da instância App, que mantém a janela aberta e responsiva para interações do usuário.
# @version: 1.0

import customtkinter as ctk
from theme     import BG_DEEP
from dashboard import SolarDashboard

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Painel de Energia Solar Portátil")
        self.configure(fg_color=BG_DEEP)
        
        # Ativa o modo de tela cheia (fullscreen)
        self.attributes("-fullscreen", True)
        
        # Permite fechar o aplicativo apertando a tecla ESC
        self.bind("<Escape>", lambda e: self.destroy())
        
        # pack(expand=True) garante que o painel fique centralizado
        # caso a tela seja maior que os 1024x600 originais do design.
        SolarDashboard(self).pack(expand=True)

if __name__ == "__main__":
    App().mainloop()