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
after_id = None             # ID do método after() da animação para possível cancelamento

# ------------------ JANELA 1: ANIMAÇÃO INICIAL ------------------
janela_1 = tk.Tk()
janela_1.title("CHECK CHECK")
ctk.set_appearance_mode("dark")  # Define o modo escuro do CustomTkinter
janela_1.config(bg="black")      # Fundo preto para estilo cyber

# Caminho absoluto do GIF animado
gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Hello day.gif")
gif = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]  # Carrega todos os frames do GIF

# Label para exibir o GIF
label = tk.Label(janela_1, bg="black")
label.pack()

# Função que exibe os frames do GIF em loop
def mostrar_frame():
    global current_frame, animando, after_id
    if animando and current_frame < len(frames):
        label.config(image=frames[current_frame])
        label.image = frames[current_frame]
        current_frame += 1
        after_id = janela_1.after(100, mostrar_frame)
    else:
        animando = False

current_frame = 0
mostrar_frame()

# ------------------ JANELA 2: INTERFACE DO ASSISTENTE ------------------
def abrir_janela_2():
    global animando, after_id
    animando = False
    if after_id:
        janela_1.after_cancel(after_id)
    janela_1.destroy()  # Fecha a janela inicial com o GIF

    # Criação da nova janela principal
    janela_2 = tk.Tk()
    janela_2.title("Assistente de Rotina")
    janela_2.geometry("900x500")
    ctk.set_appearance_mode("dark")
    janela_2.config(bg="black")

    # ------------------ FRAME ESQUERDO: CHAT ------------------
    frame_chat = tk.Frame(janela_2, bg="black")
    frame_chat.pack(side="left", fill="both", expand=True)

    # ------------------ FRAME DIREITO COM BORDA VERDE FLUORESCENTE ------------------

    # Frame externo simulando borda verde
    borda_rotina = tk.Frame(janela_2, bg="#39ff14", padx=2, pady=2)
    borda_rotina.pack(side="right", fill="y", pady=20, padx=10)

    # Frame interno (conteúdo da rotina)
    frame_rotina = tk.Frame(borda_rotina, bg="#1a1a1a", width=300)
    frame_rotina.pack(fill="both", expand=True)


    # Caixa de saída do chat (apenas leitura)
    caixa_chat = tk.Text(frame_chat, bg="black", fg="lime", font=("Consolas", 16),
                        state="disabled", wrap="word", relief="flat")
    caixa_chat.pack(padx=10, pady=20, expand=True, fill="both")

    # Variável de entrada do usuário
    entrada_var = tk.StringVar()
    entrada_var.set("escreva aqui...")

    # Frame para agrupar entrada e botão ➤
    entrada_frame = tk.Frame(frame_chat, bg="black")
    entrada_frame.pack(fill="x", padx=10, pady=5)

    # Campo de entrada de texto
    entrada = tk.Entry(entrada_frame, textvariable=entrada_var, font=("Consolas", 20),
                    bg="black", fg="lime", insertbackground="lime",
                    highlightbackground="#39ff14", highlightcolor="#39ff14",
                    highlightthickness=2, relief="flat")
    entrada.pack(side="left", fill="x", expand=True)

    # Comportamento do placeholder
    def on_entry_click(event):
        if entrada_var.get() == "escreva aqui...":
            entrada_var.set("")
    def on_focus_out(event):
        if entrada_var.get() == "":
            entrada_var.set("escreva aqui...")

    entrada.bind("<FocusIn>", on_entry_click)
    entrada.bind("<FocusOut>", on_focus_out)

    # Botão circular com símbolo ➤ ao lado da entrada
    botao_enviar = tk.Canvas(entrada_frame, width=50, height=50, bg="black", highlightthickness=0)
    botao_enviar.pack(side="left", padx=(10, 0))
    circulo = botao_enviar.create_oval(5, 5, 45, 45, outline="black", width=2, fill="#0f0f0f")
    texto = botao_enviar.create_text(25, 25, text="➤", fill="#39ff14", font=("Arial", 16, "bold"))
    botao_enviar.tag_bind(circulo, "<Button-1>", lambda e: enviar())
    botao_enviar.tag_bind(texto, "<Button-1>", lambda e: enviar())

    # Título da seção de rotina
    label_rotina = tk.Label(frame_rotina, text="Sua Rotina", bg="#1a1a1a",
                            fg="lime", font=("Arial", 15, "bold"))
    label_rotina.pack(pady=10)

    # Frame onde os itens da checklist serão exibidos
    checklist_frame = tk.Frame(frame_rotina, bg="#1a1a1a")
    checklist_frame.pack(fill="both", expand=True, padx=20)

    # Atualiza os checkboxes com base nas tarefas
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

    # Insere mensagens simulando "fala" com delay
    def bot_fala(mensagem, delay=500):
        janela_2.after(delay, lambda: (caixa_chat.config(state="normal"),
                                    caixa_chat.insert(tk.END, mensagem),
                                    caixa_chat.see(tk.END),
                                    caixa_chat.config(state="disabled")))

    # Introdução inicial do bot com delays variados
    bot_fala("> [BOT: CYBER-ROUTINE v1.0]\n", delay=300)
    bot_fala(">\n", delay=350)
    bot_fala(">\n", delay=370)
    bot_fala("> Olá, viajante digital.\n", delay=900)
    bot_fala("> Você está conectado ao núcleo de automação diária.\n", delay=1600)
    bot_fala("> Eu sou seu BOT de organização pessoal.\n", delay=2200)
    bot_fala(">\n", delay=2250)
    bot_fala("> Minha função:\n", delay=2300)
    bot_fala("> → Coletar suas respostas.\n", delay=2400)
    bot_fala("> → Criar uma ROTINA OTIMIZADA.\n", delay=2500)
    bot_fala("> → Entregar tudo em um CHECKLIST interativo.\n", delay=3000)
    bot_fala(">\n", delay=3100)
    bot_fala("> ⚠ Ative o MODO TELA CHEIA para melhor experiência. ⚠\n", delay=4000)
    bot_fala(">\n", delay=4100)
    bot_fala("> [Digite algo e pressione o botão '➤']\n", delay=4800)
    bot_fala(">\n", delay=4900)
    bot_fala(">\n", delay=4950)

    inicio_confirmado = False

    # ------------------ LÓGICA DE FLUXO DO BOT ------------------
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

        caixa_chat.config(state="normal")
        caixa_chat.insert(tk.END, f"> Você: {msg}\n")
        caixa_chat.config(state="disabled")
        caixa_chat.see(tk.END)
        entrada.delete(0, tk.END)

        # Etapa 1 - trabalha?
        if indice_pergunta == 0:
            if msg.lower() == "y":
                respostas["trabalha"] = True
                bot_fala("> BOT: Que horas você trabalha? (ex: 13:00)\n")
                indice_pergunta = 1
            else:
                respostas["trabalha"] = False
                bot_fala("> BOT: Sem trabalho hoje.\n> BOT: Que horas você costuma acordar? (ex: 4:30)\n")
                indice_pergunta = 2

        # Etapa 2 - horário de trabalho
        elif indice_pergunta == 1:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "trabalho"))
                atualizar_checklist()
                bot_fala("> BOT: Trabalho registrado.\n> BOT: Que horas você acorda? (ex: 4:30)\n")
                indice_pergunta = 2
            except ValueError:
                bot_fala("> BOT: Use o formato HH:MM.\n")

        # Etapa 3 - acordar
        elif indice_pergunta == 2:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "acordar"))
                atualizar_checklist()
                bot_fala("> BOT: Acordar registrado.\n> BOT: Que horas você toma café da manhã? (ex: 7:00)\n")
                indice_pergunta = 3
            except ValueError:
                bot_fala("> BOT: Horário inválido.\n")

        # Etapa 4 - café da manhã
        elif indice_pergunta == 3:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "café da manhã"))
                atualizar_checklist()
                bot_fala("> BOT: Café da manhã registrado!\n> BOT: Que horas será seu tempo para lazer ou redes sociais? (ex: 21:00)\n")
                indice_pergunta = 4
            except ValueError:
                bot_fala("> BOT: Tente no formato HH:MM.\n")

        # Etapa 5 - lazer
        elif indice_pergunta == 4:
            try:
                horario = datetime.strptime(msg, "%H:%M").strftime("%H:%M")
                tarefas.append((horario, "lazer"))
                atualizar_checklist()
                bot_fala("> BOT: Horário de lazer registrado!\n> BOT: Rotina finalizada ✅\n")
                indice_pergunta = 99
            except ValueError:
                bot_fala("> BOT: Tente no formato HH:MM.\n")

        # Final
        else:
            bot_fala("> BOT: Rotina já foi criada.\n")

    # Encerra a interface
    janela_2.mainloop()

# ------------------ BOTÃO "NEXT" NA JANELA INICIAL ------------------
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

# ------------------ INICIALIZA A INTERFACE ------------------
janela_1.mainloop()
