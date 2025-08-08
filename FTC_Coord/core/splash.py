# core/splash.py
from ttkbootstrap import *
from tkinter import Label
import time


class TelaSplash:
    def __init__(self, root, ao_carregar):
        self.root = root
        self.root.title("Iniciando NexuGest")
        self.root.geometry("400x200")
        Label(root, text="Carregando...", font=("Arial", 20)).pack(expand=True)

        def carregar():
            time.sleep(2.5)  # animação simulada
            ao_carregar()

        root.after(2500, ao_carregar)