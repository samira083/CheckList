import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime

# Dicionários e variáveis para controle das respostas e perguntas
respostas = {}
indice_pergunta = 0
tarefas = []

# ------------------ JANELA 1 (Animação Inicial com GIF) ------------------
janela_1 = tk.Tk()
janela_1.title("CHECK CHECK")
ctk.set_appearance_mode("dark")
janela_1.config(bg="black")

# Carrega e converte os frames do GIF
gif_path = "C:\\Users\\samir\\Downloads\\Hello day.gif"
gif = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

label = tk.Label(janela_1, bg="black")
label.pack()

current_frame = 0
animando = True
after_id = None

# Função para exibir os frames do GIF
def mostrar_frame():
    global current_frame, after_id
    if not animando or not label.winfo_exists():
        return
    label.config(image=frames[current_frame])
    label.image = frames[current_frame]
    current_frame = (current_frame + 1) % len(frames)
    after_id = janela_1.after(100, mostrar_frame)

# ------------------ JANELA 2 (Chat e Checklist) ------------------
def abrir_janela_2():
    global animando, after_id
    animando = False
    if after_id:
        janela_1.after_cancel(after_id)

    janela_1.destroy()  # Fecha a janela do GIF

    janela_2 = tk.Tk()
    janela_2.title("Assistente de Rotina")
    janela_2.geometry("900x500")
    ctk.set_appearance_mode("dark")
    janela_2.config(bg="black")

    frame_chat = tk.Frame(janela_2, bg="black")
    frame_chat.pack(side="left", fill="both", expand=True)

    frame_rotina = tk.Frame(janela_2, bg="#1a1a1a", width=900)
    frame_rotina.pack(side="right", fill="y", pady=20)

    caixa_chat = tk.Text(frame_chat, bg="black", fg="lime", font=("Consolas", 16))
    caixa_chat.pack(padx=10, pady=20, expand=True, fill="both")

    entrada_var = tk.StringVar()
    entrada_var.set("escreva aqui...")

    entrada = tk.Entry(frame_chat, textvariable=entrada_var, font=("Consolas", 20),
                    bg="black", fg="lime", insertbackground="lime",
                    highlightbackground="#39ff14", highlightcolor="#39ff14",
                    highlightthickness=2, relief="flat")
    entrada.pack(fill="x", padx=10, pady=5)

    def on_entry_click(event):
        if entrada_var.get() == "escreva aqui...":
            entrada_var.set("")

    def on_focus_out(event):
        if entrada_var.get() == "":
            entrada_var.set("escreva aqui...")

    entrada.bind("<FocusIn>", on_entry_click)
    entrada.bind("<FocusOut>", on_focus_out)

    label_rotina = tk.Label(frame_rotina, text="Sua Rotina", bg="#1a1a1a", fg="lime", font=("Arial", 15, "bold"))
    label_rotina.pack(pady=10)

    checklist_frame = tk.Frame(frame_rotina, bg="#1a1a1a")
    checklist_frame.pack(fill="both", expand=True, padx=150)

    def atualizar_checklist():
        for widget in checklist_frame.winfo_children():
            widget.destroy()
        tarefas.sort()
        for hora, descricao in tarefas:
            var = tk.IntVar()
            chk = tk.Checkbutton(checklist_frame, text=f"{hora} {descricao}",
                                variable=var, onvalue=1, offvalue=0,
                                bg="#1a1a1a", fg="white", selectcolor="black", anchor="w")
            chk.pack(fill="x", pady=5, anchor="w")

    mensagem_inicial = (
        "> [BOT: CYBER-ROUTINE v1.0]\n"
        "> Olá, viajante digital.\n"
        ">\n"
        "> Você está conectado ao núcleo de automação diária.\n"
        "> Eu sou seu BOT de organização pessoal.\n"
        ">\n"
        "> Minha função:\n"
        "> → Coletar suas respostas.\n"
        "> → Criar uma ROTINA OTIMIZADA.\n"
        "> → Entregar tudo em um CHECKLIST interativo.\n"
        ">\n"
        "> ⚠ Para visualização completa do sistema: ⚠\n"
        "> → Ative o **MODO TELA CHEIA** imediatamente.\n"
        "> → Preste atenção, ao lado do bate-papo irá aparecer sua CHECK-LIST personalizada\n"
        ">\n"
        "> Preparando ambiente de perguntas…\n"
        "> Iniciando sincronização com sua mente cibernética...\n"
        ">\n"
        "> [Pressione no botão '➤' a baixo para começar sua programação personalizada]\n"
    )
    caixa_chat.insert(tk.END, mensagem_inicial)

    inicio_confirmado = False

    def enviar():
        nonlocal inicio_confirmado
        global indice_pergunta

        msg = entrada.get().strip()
        if not msg:
            return

        if not inicio_confirmado:
            caixa_chat.insert(tk.END, "> BOT: Você trabalha hoje? (y/n)\n")
            entrada.delete(0, tk.END)
            inicio_confirmado = True
            return

        caixa_chat.insert(tk.END, f"> Você: {msg}\n")
        entrada.delete(0, tk.END)

        if indice_pergunta == 0:
            if msg.lower() == "y":
                respostas["trabalha"] = True
                caixa_chat.insert(tk.END, "> BOT: Que horas você trabalha? (ex: 13:00)\n")
                indice_pergunta = 1
            else:
                respostas["trabalha"] = False
                caixa_chat.insert(tk.END, "> BOT: Sem trabalho hoje.\n > BOT: Que horas você costuma acordar? (ex: 4:30)\n")
                indice_pergunta = 2

        elif indice_pergunta == 1:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "trabalho"))
                atualizar_checklist()
                caixa_chat.insert(tk.END, "> BOT: Trabalho registrado.\n> BOT: Que horas você acorda? (ex: 4:30)\n")
                indice_pergunta = 2
            except ValueError:
                caixa_chat.insert(tk.END, "> BOT: Use o formato HH:MM.\n")

        elif indice_pergunta == 2:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "acordar"))
                atualizar_checklist()
                caixa_chat.insert(tk.END, "> BOT: Acordar registrado. (suba o bate-papo) \n> BOT: Que horas você toma café da manhã? (ex: 7:00)\n")
                indice_pergunta = 3
            except ValueError:
                caixa_chat.insert(tk.END, "> BOT: Horário inválido.\n")

        elif indice_pergunta == 3:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "café da manhã"))
                atualizar_checklist()
                caixa_chat.insert(tk.END, "> BOT: Café da manhã registrado!\n> BOT: Que horas será seu tempo para lazer ou redes sociais? (ex: 21:00)\n")
                indice_pergunta = 99
            except ValueError:
                caixa_chat.insert(tk.END, "> BOT: Tente no formato HH:MM.\n")

        elif indice_pergunta == 4:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "lazer"))
                atualizar_checklist()
                caixa_chat.insert(tk.END, "> BOT: Horário de lazer registrado!\nRotina finalizada ✅\n")
                indice_pergunta = 99
            except ValueError:
                caixa_chat.insert(tk.END, "> BOT: Tente no formato HH:MM.\n")

        else:
            caixa_chat.insert(tk.END, "> BOT: Rotina finalizada ✅\n")

    botao_enviar = tk.Canvas(frame_chat, width=50, height=50, bg="black", highlightthickness=0)
    botao_enviar.pack(pady=5)
    circulo = botao_enviar.create_oval(5, 5, 45, 45, outline="black", width=2, fill="#0f0f0f")
    texto = botao_enviar.create_text(25, 25, text="➤", fill="#39ff14", font=("Arial", 16, "bold"))
    botao_enviar.tag_bind(circulo, "<Button-1>", lambda e: enviar())
    botao_enviar.tag_bind(texto, "<Button-1>", lambda e: enviar())

    janela_2.mainloop()

# ------------------ BOTÃO NEXT NA TELA INICIAL ------------------
btn_show = ctk.CTkButton(
    master=janela_1,
    text="NEXT",
    font=("Arial", 26, "bold"),
    command=abrir_janela_2,
    text_color="black",
    fg_color="lime",
    corner_radius=20,
    width=350,
    height=50
)
btn_show.pack(pady=10)

# Inicia a animação do GIF
mostrar_frame()
# Função para exibir os frames do GIF uma vez
def mostrar_frame():
    global current_frame, animando, after_id
    if animando and current_frame < len(frames):
        label.config(image=frames[current_frame])
        label.image = frames[current_frame]
        current_frame += 1
        after_id = janela_1.after(100, mostrar_frame)
    else:
        animando = False  # Para a animação
janela_1.mainloop()
