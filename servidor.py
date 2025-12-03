import socket
import threading

HOST = "127.0.0.1"
PORT = 9001

def handle_client(conn, addr):
    print(f"[SERVIDOR] Conectado a {addr}")

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            conn.sendall(data)  # eco direto
    except:
        pass

    conn.close()
    print(f"[SERVIDOR] Conexão encerrada {addr}")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    print(f"[SERVIDOR] Escutando em {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
