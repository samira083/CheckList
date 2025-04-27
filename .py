import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence

# Criação da janela
janela = tk.Tk()
janela.title("Controle de GIF")
ctk.set_appearance_mode("dark")

# Configura o fundo da janela para preto
janela.config(bg="black")

# Carrega o GIF
gif_path = "C:\\Users\\samir\\Downloads\\Hello day.gif"  # Substitua pelo caminho do seu GIF
gif = Image.open(gif_path)

# Carrega todos os frames do GIF
frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

# Variável para controlar o estado da animação (True = animando, False = pausado)
animando = True
current_frame = 0

# Função para atualizar o frame do GIF
def mostrar_frame():
    global animando, current_frame  # Declara as variáveis como globais

    if animando:
        # Exibe o próximo frame
        label.config(image=frames[current_frame])
        label.image = frames[current_frame]

        # Passa para o próximo frame, reiniciando quando chegar ao final
        current_frame = (current_frame + 1) % len(frames)

        # Verifica se a animação deve ser pausada depois de um ciclo completo
        if current_frame == 0:
            animando = False  # Pausa a animação após o ciclo completo

        # Atualiza a cada 100 ms
        janela.after(100, mostrar_frame)

# Função para o botão (exemplo de exibir uma mensagem)
def exibir_mensagem():
    print("Botão clicado!")

# Criação do label para exibir o GIF
label = tk.Label(janela, bg="black")  # Definindo o fundo do label como preto também
label.pack()

# Criação do botão abaixo do GIF
btn_show = ctk.CTkButton(
    master=janela,
    text="NEXT",
    font=("Arial", 26, "bold"),
    command=exibir_mensagem,
    text_color="black",      # cor do texto
    fg_color="lime",          # cor do botão
    corner_radius=20,         # botão mais arredondado
    width=350,                # largura
    height=50                 # altura
)
btn_show.pack(pady=10)

# Começa a mostrar o primeiro frame
mostrar_frame()

# Inicia a janela
janela.mainloop()
