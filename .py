import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence

# Criação da janela principal
janela_1 = tk.Tk()
janela_1.title("CHECK CHECK")
ctk.set_appearance_mode("dark")
janela_1.config(bg="black")

# Função para abrir a janela 2
def janela_2():
    nova_janela = tk.Toplevel(janela_1)
    nova_janela.title("Janela 2")
    nova_janela.geometry("400x400")
    nova_janela.configure(bg="white")

    label = tk.Label(nova_janela, text="Bem-vindo à Janela 2!", font=("Arial", 16), bg="white")
    label.pack(pady=20)

    # Fecha a janela principal
    janela_1.destroy()

# Carrega o GIF
gif_path = "C:\\Users\\samir\\Downloads\\Hello day.gif"  # Caminho do GIF
gif = Image.open(gif_path)

# Prepara os frames do GIF
frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]
animando = True
current_frame = 0

# Função para mostrar os frames
def mostrar_frame():
    global animando, current_frame
    if animando:
        label.config(image=frames[current_frame])
        label.image = frames[current_frame]
        current_frame = (current_frame + 1) % len(frames)
        if current_frame == 0:
            animando = False
        janela_1.after(100, mostrar_frame)

# Label para exibir o GIF
label = tk.Label(janela_1, bg="black")
label.pack()

# Botão "NEXT"
btn_show = ctk.CTkButton(
    master=janela_1,
    text="NEXT",
    font=("Arial", 26, "bold"),
    command=janela_2,
    text_color="black",
    fg_color="lime",
    corner_radius=20,
    width=350,
    height=50
)
btn_show.pack(pady=10)

# Inicia a animação
mostrar_frame()

# Inicia a interface
janela_1.mainloop()
