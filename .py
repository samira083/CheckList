import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime
import os

# ------------------ VARIÁVEIS GLOBAIS ------------------
respostas = {}              # Guarda as respostas do usuário
indice_pergunta = 0         # Índice de controle do fluxo de perguntas
tarefas = []                # Lista de tarefas que compõem a rotina
animando = True             # Controle da animação do GIF
after_id = None             # ID para controle do after() da animação

# ------------------ JANELA 1: ANIMAÇÃO INICIAL ------------------
janela_1 = tk.Tk()
janela_1.title("CHECK CHECK")
ctk.set_appearance_mode("dark")  # Modo escuro do customtkinter
janela_1.config(bg="black")

# Caminho para o arquivo GIF
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Hello day.gif")

# Carrega os frames do GIF
gif = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

# Label onde o GIF será exibido
label = tk.Label(janela_1, bg="black")
label.pack()

# Função para exibir os frames do GIF em loop
def mostrar_frame():
    global current_frame, animando, after_id
    if animando and current_frame < len(frames):
        label.config(image=frames[current_frame])
        label.image = frames[current_frame]
        current_frame += 1
        after_id = janela_1.after(100, mostrar_frame)
    else:
        animando = False  # Para a animação

current_frame = 0
mostrar_frame()

# ------------------ JANELA 2: CHAT E CHECKLIST ------------------
def abrir_janela_2():
    global animando, after_id
    animando = False  # Para a animação do GIF
    if after_id:
        janela_1.after_cancel(after_id)  # Cancela o loop da animação
    janela_1.destroy()  # Fecha a janela da animação

    # Cria nova janela
    janela_2 = tk.Tk()
    janela_2.title("Assistente de Rotina")
    janela_2.geometry("900x500")
    ctk.set_appearance_mode("dark")
    janela_2.config(bg="black")

    # ------------------ FRAME DO CHAT (ESQUERDA) ------------------
    frame_chat = tk.Frame(janela_2, bg="black")
    frame_chat.pack(side="left", fill="both", expand=True)

    # ------------------ FRAME DA ROTINA (DIREITA) ------------------
    frame_rotina = tk.Frame(janela_2, bg="#1a1a1a", width=900)
    frame_rotina.pack(side="right", fill="y", pady=20)

    # Caixa de texto do chat
    caixa_chat = tk.Text(frame_chat, bg="black", fg="lime", font=("Consolas", 16))
    caixa_chat.pack(padx=10, pady=20, expand=True, fill="both")

    # Campo de entrada do usuário
    entrada_var = tk.StringVar()
    entrada_var.set("escreva aqui...")
    entrada = tk.Entry(frame_chat, textvariable=entrada_var, font=("Consolas", 20),
                    bg="black", fg="lime", insertbackground="lime",
                    highlightbackground="#39ff14", highlightcolor="#39ff14",
                    highlightthickness=2, relief="flat")
    entrada.pack(fill="x", padx=10, pady=5)

    # Placeholder interativo no campo de entrada
    def on_entry_click(event):
        if entrada_var.get() == "escreva aqui...":
            entrada_var.set("")
    def on_focus_out(event):
        if entrada_var.get() == "":
            entrada_var.set("escreva aqui...")
    entrada.bind("<FocusIn>", on_entry_click)
    entrada.bind("<FocusOut>", on_focus_out)

    # Título da checklist
    label_rotina = tk.Label(frame_rotina, text="Sua Rotina", bg="#1a1a1a",
                            fg="lime", font=("Arial", 15, "bold"))
    label_rotina.pack(pady=10)

    # Frame interno da checklist
    checklist_frame = tk.Frame(frame_rotina, bg="#1a1a1a")
    checklist_frame.pack(fill="both", expand=True, padx=150)

    # Atualiza a checklist com base na lista de tarefas
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

    # Função para exibir mensagens com delay
    def bot_fala(mensagem, delay=500):
        janela_2.after(delay, lambda: caixa_chat.insert(tk.END, mensagem))

    # Envia mensagem inicial com delays simulando "pensamento"
    bot_fala("> [BOT: CYBER-ROUTINE v1.0]\n", delay=300)
    bot_fala("> Olá, viajante digital.\n", delay=900)
    bot_fala("> Você está conectado ao núcleo de automação diária.\n", delay=1600)
    bot_fala("> Eu sou seu BOT de organização pessoal.\n", delay=2200)
    bot_fala("> Minha função:\n> → Coletar suas respostas.\n> → Criar uma ROTINA OTIMIZADA.\n> → Entregar tudo em um CHECKLIST interativo.\n", delay=3000)
    bot_fala("> ⚠ Ative o MODO TELA CHEIA para melhor experiência.\n", delay=4000)
    bot_fala("> [Digite qualque coisa e pressione no botão '➤' \n > abaixo para começar sua programação personalizada]\n", delay=4800)

    inicio_confirmado = False

    # Lógica de fluxo das perguntas e montagem da rotina
    def enviar():
        nonlocal inicio_confirmado
        global indice_pergunta

        msg = entrada.get().strip()
        if not msg:
            return

        if not inicio_confirmado:
            bot_fala("> BOT: Você trabalha hoje? (y/n)\n")
            entrada.delete(0, tk.END)
            inicio_confirmado = True
            return

        caixa_chat.insert(tk.END, f"> Você: {msg}\n")
        entrada.delete(0, tk.END)

        # Pergunta 1 - Trabalha hoje?
        if indice_pergunta == 0:
            if msg.lower() == "y":
                respostas["trabalha"] = True
                bot_fala("> BOT: Que horas você trabalha? (ex: 13:00)\n")
                indice_pergunta = 1
            else:
                respostas["trabalha"] = False
                bot_fala("> BOT: Sem trabalho hoje.\n> BOT: Que horas você costuma acordar? (ex: 4:30)\n")
                indice_pergunta = 2

        # Pergunta 2 - Horário de trabalho
        elif indice_pergunta == 1:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "trabalho"))
                atualizar_checklist()
                bot_fala("> BOT: Trabalho registrado.\n> BOT: Que horas você acorda? (ex: 4:30)\n")
                indice_pergunta = 2
            except ValueError:
                bot_fala("> BOT: Use o formato HH:MM.\n")

        # Pergunta 3 - Acordar
        elif indice_pergunta == 2:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "acordar"))
                atualizar_checklist()
                bot_fala("> BOT: Acordar registrado.\n> BOT: Que horas você toma café da manhã? (ex: 7:00)\n")
                indice_pergunta = 3
            except ValueError:
                bot_fala("> BOT: Horário inválido.\n")

        # Pergunta 4 - Café da manhã
        elif indice_pergunta == 3:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "café da manhã"))
                atualizar_checklist()
                bot_fala("> BOT: Café da manhã registrado!\n> BOT: Que horas será seu tempo para lazer ou redes sociais? (ex: 21:00)\n")
                indice_pergunta = 4
            except ValueError:
                bot_fala("> BOT: Tente no formato HH:MM.\n")

        # Pergunta 5 - Lazer
        elif indice_pergunta == 4:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "lazer"))
                atualizar_checklist()
                bot_fala("> BOT: Horário de lazer registrado!\n> BOT: Rotina finalizada ✅\n")
                indice_pergunta = 99
            except ValueError:
                bot_fala("> BOT: Tente no formato HH:MM.\n")

        # Caso todas as perguntas tenham sido feitas
        else:
            bot_fala("> BOT: Rotina finalizada ✅\n")

    # ------------------ BOTÃO DE ENVIAR MENSAGEM ------------------
    botao_enviar = tk.Canvas(frame_chat, width=50, height=50, bg="black", highlightthickness=0)
    botao_enviar.pack(pady=5)
    circulo = botao_enviar.create_oval(5, 5, 45, 45, outline="black", width=2, fill="#0f0f0f")
    texto = botao_enviar.create_text(25, 25, text="➤", fill="#39ff14", font=("Arial", 16, "bold"))
    botao_enviar.tag_bind(circulo, "<Button-1>", lambda e: enviar())
    botao_enviar.tag_bind(texto, "<Button-1>", lambda e: enviar())

    janela_2.mainloop()

# ------------------ BOTÃO "NEXT" NA TELA INICIAL ------------------
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

# ------------------ INÍCIO DA INTERFACE ------------------
janela_1.mainloop()
