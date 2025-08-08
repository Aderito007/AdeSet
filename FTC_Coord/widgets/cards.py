# widgets/cards.py
from ttkbootstrap import *

def criar_card_indicador(master, valor, texto, icone="ℹ️"):
    frame = Frame(master, padding=10, relief="raised", borderwidth=1)
    frame.pack(side=LEFT, padx=6, ipadx=4)

    Label(frame, text=icone, font=("Arial", 20)).pack()
    Label(frame, text=valor, font=("Arial", 14, "bold")).pack()
    Label(frame, text=texto, font=("Arial", 10)).pack()


    