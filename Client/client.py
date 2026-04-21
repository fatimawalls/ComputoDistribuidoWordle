import socket
import json
import threading
import tkinter as tk
from tkinter import messagebox

# ==================================================
# CONFIG
# ==================================================
PORT = 5000
sock = None
file = None
wins = 0
puede_escribir = False

# ==================================================
# SOCKET
# ==================================================
def enviar_json(sock, data):
    msg = json.dumps(data, separators=(',', ':')) + "\n"
    print("📤 CLIENT -> SERVER:", msg.strip())
    sock.sendall(msg.encode())

def recibir_json(file):
    while True:
        line = file.readline()

        if not line:
            raise Exception("Servidor desconectado")

        print("📥 SERVER -> CLIENT RAW:", line.strip())

        try:
            return json.loads(line)
        except:
            print("❌ JSON inválido")

# ==================================================
# INTERFAZ
# ==================================================
root = tk.Tk()
root.title("WORDLE ONLINE")
root.geometry("520x800")
root.config(bg="#121213")
root.resizable(False, False)

titulo = tk.Label(
    root,
    text="WORDLE",
    font=("Arial", 30, "bold"),
    fg="white",
    bg="#121213"
)
titulo.pack(pady=15)

# ==================================================
# LOGIN
# ==================================================
frame_login = tk.Frame(root, bg="#121213")
frame_login.pack(pady=20)

tk.Label(frame_login, text="IP Servidor", fg="white", bg="#121213").pack()
entry_ip = tk.Entry(frame_login, width=25, font=("Arial", 12))
entry_ip.insert(0, "127.0.0.1")
entry_ip.pack(pady=5)

tk.Label(frame_login, text="Usuario", fg="white", bg="#121213").pack()
entry_user = tk.Entry(frame_login, width=25, font=("Arial", 12))
entry_user.pack(pady=5)

tk.Label(frame_login, text="Password", fg="white", bg="#121213").pack()
entry_pass = tk.Entry(frame_login, width=25, show="*", font=("Arial", 12))
entry_pass.pack(pady=5)

estado = tk.Label(
    root,
    text="Heidi Meiners Muñoz \n Valeria Pérez Maciel \n Fátima Wall Fernández \n \n Profesor: Juan Carlos López Pimentel \n Materia: Computo Distribuido \n 6to Semestre ISGC",
    fg="white",
    bg="#121213",
    font=("Arial", 14, "bold")
)
estado.pack()

# ==================================================
# GAME
# ==================================================
frame_game = tk.Frame(root, bg="#121213")

grid_frame = tk.Frame(frame_game, bg="#121213")
grid_frame.pack(pady=20)

celdas = []

for fila in range(6):
    fila_temp = []
    for col in range(5):
        lbl = tk.Label(
            grid_frame,
            text="",
            width=4,
            height=2,
            font=("Arial", 22, "bold"),
            bg="#3a3a3c",
            fg="white",
            relief="solid",
            bd=2
        )
        lbl.grid(row=fila, column=col, padx=5, pady=5)
        fila_temp.append(lbl)
    celdas.append(fila_temp)

info = tk.Label(
    frame_game,
    text="Escribe una palabra de 5 letras y presiona ENTER",
    fg="white",
    bg="#121213",
    font=("Arial", 12)
)
info.pack(pady=10)

mensaje_final = tk.Label(
    frame_game,
    text="",
    fg="white",
    bg="#121213",
    font=("Arial", 22, "bold")
)
mensaje_final.pack(pady=10)

fila_actual = 0
palabra_actual = ""
palabra_lista = tk.StringVar()

# ==================================================
# TABLERO
# ==================================================
def limpiar_tablero():
    global fila_actual, palabra_actual

    fila_actual = 0
    palabra_actual = ""

    for fila in celdas:
        for celda in fila:
            celda.config(text="", bg="#3a3a3c", fg="white")

def refrescar_fila():
    global fila_actual, palabra_actual

    if fila_actual >= 6:
        return

    for i in range(5):
        letra = ""

        if i < len(palabra_actual):
            letra = palabra_actual[i].upper()

        celdas[fila_actual][i].config(
            text=letra,
            bg="#3a3a3c",
            fg="white"
        )

def pintar_resultado(palabra, resultado):
    global fila_actual

    for i in range(5):
        letra = palabra[i].upper()

        color = "#3a3a3c"

        if resultado[i] == "C":
            color = "#6aaa64"
        elif resultado[i] == "P":
            color = "#c9b458"
        elif resultado[i]== "A":
            color = "#7b7b7b"

        celdas[fila_actual][i].config(
            text=letra,
            bg=color,
            fg="white"
        )

    fila_actual += 1

# ==================================================
# REINICIAR
# ==================================================
def reiniciar():
    global puede_escribir

    limpiar_tablero()
    mensaje_final.config(text="")
    btn_reiniciar.pack_forget()
    puede_escribir = False

    enviar_json(sock, {
        "type": "play_again",
        "value": "SI"
    })

btn_reiniciar = tk.Button(
    frame_game,
    text="REINICIAR PARTIDA",
    width=18,
    bg="#538d4e",
    fg="white",
    font=("Arial", 12, "bold"),
    command=reiniciar
)

# ==================================================
# INPUT
# ==================================================
def escribir(event):
    global palabra_actual

    if not frame_game.winfo_ismapped():
        return

    if not puede_escribir:
        return

    tecla = event.keysym

    if len(tecla) == 1 and tecla.isalpha():
        if len(palabra_actual) < 5:
            palabra_actual += tecla.lower()
            refrescar_fila()

    elif tecla == "BackSpace":
        palabra_actual = palabra_actual[:-1]
        refrescar_fila()

    elif tecla == "Return":
        if len(palabra_actual) == 5:
            palabra_lista.set(palabra_actual)
            palabra_actual = ""

root.bind("<Key>", escribir)

# ==================================================
# JUEGO
# ==================================================
def hilo_juego():
    global wins, puede_escribir, palabra_actual

    while True:
        msg = recibir_json(file)

        if msg["type"] == "start":
            limpiar_tablero()
            mensaje_final.config(text="")
            puede_escribir = True

        elif msg["type"] == "play_again":
            continue

        while puede_escribir:

            while palabra_lista.get() == "":
                root.update()
                root.after(50)

            palabra = palabra_lista.get()
            palabra_lista.set("")

            enviar_json(sock, {
                "type": "guess",
                "word": palabra
            })

            resp = recibir_json(file)

            if resp["type"] == "error":
                palabra_actual = palabra
                refrescar_fila()
                continue

            if resp["type"] == "result":
                pintar_resultado(palabra, resp["data"])

                if resp["status"] == "win":
                    wins += 1
                    estado.config(text=f"Wins: {wins}")
                    puede_escribir = False

                    mensaje_final.config(
                        text="🎉 GANASTE",
                        fg="#6aaa64"
                    )

                    btn_reiniciar.pack(pady=10)

                elif resp["status"] == "lose":
                    puede_escribir = False

                    mensaje_final.config(
                        text="😢 PERDISTE",
                        fg="#ff4d4d"
                    )

                    btn_reiniciar.pack(pady=10)

# ==================================================
# LOGIN / REGISTER
# ==================================================
def autenticar(tipo):
    global sock, file, wins

    try:
        HOST = entry_ip.get()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        file = sock.makefile()

        enviar_json(sock, {
            "type": tipo,
            "user": entry_user.get(),
            "pass": entry_pass.get()
        })

        resp = recibir_json(file)

        if resp["type"] == "auth" and resp["status"] == "ok":

            wins = resp["wins"]
            estado.config(text=f"Wins: {wins}")
        
            frame_login.pack_forget()
            frame_game.pack()
        
            threading.Thread(
                target=hilo_juego,
                daemon=True
            ).start()
        
        else:
            messagebox.showerror("Error", "Datos incorrectos")
    except:
        messagebox.showerror("Error", "No se pudo conectar")

# ==================================================
# BOTONES LOGIN
# ==================================================
tk.Button(
    frame_login,
    text="LOGIN",
    width=20,
    bg="green",
    fg="white",
    command=lambda: autenticar("login")
).pack(pady=5)

tk.Button(
    frame_login,
    text="REGISTER",
    width=20,
    bg="blue",
    fg="white",
    command=lambda: autenticar("register")
).pack(pady=5)

# ==================================================
# START
# ==================================================
root.mainloop()
