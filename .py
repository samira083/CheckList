import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import os

# Abertura da janela
janela_1 = tk.Tk()  
janela_1.title("Check List")  # Nome da janela

# Para a janela crescer proporcionalmente
janela_1.columnconfigure(0, weight=1)
janela_1.rowconfigure(0, weight=1)

# Caminho da fonte .ttf
caminho_fonte = os.path.join(os.getcwd(), "04B_30_.TTF")

# REGISTRA a fonte no tkinter
tkFont.Font(family="MinhaFonte", size=20, weight="bold")
janela_1.tk.call('font', 'create', 'MinhaFonte', '-family', '04B_30_', '-size', '20', '-weight', 'bold')

# Cria o título
titulo__Check = tk.Label(janela_1, text="CHECK LIST", font="MinhaFonte")
# Define onde a coluna e a linha irão ficar
titulo__Check.grid(column=0, row=0, sticky="nsew")

# Exibe a janela
janela_1.mainloop()
