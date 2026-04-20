import socket
import json

HOST = input("IP del servidor: ")
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
file = sock.makefile()

# ---------- DEBUG SEND ----------
def enviar_json(sock, data):
    msg = json.dumps(data, separators=(',', ':')) + "\n"
    print("📤 CLIENT -> SERVER:", msg.strip())
    sock.sendall(msg.encode())

# ---------- DEBUG RECEIVE ----------
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

# ---------- LOGIN / REGISTER ----------
while True:
    print("\n1. Login")
    print("2. Register")
    op = input("> ")

    user = input("Usuario: ")
    pwd = input("Password: ")

    tipo = "login" if op == "1" else "register"

    enviar_json(sock, {
        "type": tipo,
        "user": user,
        "pass": pwd
    })

    resp = recibir_json(file)

    if resp["type"] == "auth" and resp["status"] == "ok":
        print("Autenticado ✅")
        print("Wins:", resp["wins"])
        break
    else:
        print("Error ❌")

# ---------- PARTIDAS ----------
while True:
    msg = recibir_json(file)

    if msg["type"] == "start":
        print("\n🎮 Nueva partida")

    while True:
        palabra = input("Palabra: ")

        enviar_json(sock, {
            "type": "guess",
            "word": palabra
        })

        resp = recibir_json(file)

        if resp["type"] == "error":
            print("Error:", resp["message"])
            continue

        if resp["type"] == "result":
            print("Resultado:", resp["data"])

            if resp["status"] == "win":
                print("Ganaste 🎉")
                break
            elif resp["status"] == "lose":
                print("Perdiste 😢")
                break

    msg = recibir_json(file)

    if msg["type"] == "play_again":
        again = input("¿Otra? (SI/NO): ")

        enviar_json(sock, {
            "type": "play_again",
            "value": again
        })

        if again != "SI":
            break

sock.close()