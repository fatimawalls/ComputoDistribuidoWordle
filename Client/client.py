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
# VENTANAS EMERGENTES (INFO E INSTRUCCIONES)
# ==================================================
def abrir_informacion():
    ventana_info = tk.Toplevel(root)
    ventana_info.title("Información del Proyecto")
    ventana_info.geometry("400x300")
    ventana_info.config(bg="#121213")
    
    texto = (
        "PROYECTO WORDLE ONLINE\n\n"
        "Desarrollado por:\n"
        "- Heidi Meiners Muñoz\n"
        "- Valeria Pérez Maciel\n"
        "- Fátima Wall Fernández\n\n"
        "Profesor: Juan Carlos López Pimentel\n"
        "Materia: Cómputo Distribuido\n"
        "6to Semestre ISGC"
    )
    
    tk.Label(ventana_info, text=texto, fg="white", bg="#121213", 
             font=("Arial", 12), justify="center", pady=20).pack()
    
    tk.Button(ventana_info, text="Cerrar", command=ventana_info.destroy, bg="#3a3a3c", fg="white").pack(pady=10)

def abrir_instrucciones():
    ventana_inst = tk.Toplevel(root)
    ventana_inst.title("Cómo Jugar")
    ventana_inst.geometry("450x350")
    ventana_inst.config(bg="#121213")
    
    instrucciones = (
        "INSTRUCCIONES\n\n"
        "1. Adivina la palabra oculta en 6 intentos.\n"
        "2. Cada intento debe ser una palabra de 5 letras.\n"
        "3. Presiona ENTER para enviar.\n\n"
        "COLORES:\n"
        "VERDE: La letra está en la posición correcta.\n"
        "AMARILLO: La letra está en la palabra pero en otra posición.\n"
        "GRIS: La letra no forma parte de la palabra."
    )
    
    tk.Label(ventana_inst, text=instrucciones, fg="white", bg="#121213", 
             font=("Arial", 11), justify="left", padx=20, pady=20).pack()
    
    tk.Button(ventana_inst, text="Entendido", command=ventana_inst.destroy, bg="#6aaa64", fg="white").pack(pady=10)

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

estado = tk.Label(
    frame_game, 
    text="Wins: 0", 
    fg="white", 
    bg="#121213", 
    font=("Arial", 14)
)
estado.pack(pady=5)

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
).pack(pady=10)

tk.Button(
    frame_login,
    text="REGISTER",
    width=20,
    bg="blue",
    fg="white",
    command=lambda: autenticar("register")
).pack(pady=10)

tk.Button(
    frame_login,
    text="INSTRUCCIONES",
    width=20,
    bg="#3a3a3c",
    fg="white",
    command=abrir_instrucciones
).pack(pady=(30, 10))

tk.Button(
    frame_login,
    text="INFORMACIÓN",
    width=20,
    bg="#3a3a3c",
    fg="white",
    command=abrir_informacion
).pack(pady=10)

# ==================================================
# START
# ==================================================
root.mainloop()
