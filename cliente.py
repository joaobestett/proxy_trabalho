import socket
import time
from statistics import mean

HOST = "127.0.0.1"
PORT = 9000

NUM_PACOTES = 30
TAM_PACOTE = 4096

def main():
    print("\n[CLIENTE] Iniciando cliente TCP...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f"[CLIENTE] Conectado ao proxy {HOST}:{PORT}\n")

    rtts = []

    for i in range(NUM_PACOTES):
        msg = b"x" * TAM_PACOTE

        inicio = time.time()
        s.sendall(msg)
        data = s.recv(TAM_PACOTE)
        fim = time.time()

        rtt = (fim - inicio) * 1000  # em ms
        rtts.append(rtt)

        throughput = (TAM_PACOTE / (rtt / 1000 + 0.000001))  # bytes/s

        print(f"Pacote {i+1}: RTT = {rtt:.2f} ms | Throughput = {throughput:.2f} bytes/s")

        time.sleep(1)

    print("\n===== RESUMO DO TESTE =====")
    if rtts:
        print(f"RTT médio:  {mean(rtts):.2f} ms")
        print(f"RTT máximo: {max(rtts):.2f} ms")
        print(f"RTT mínimo: {min(rtts):.2f} ms")
    else:
        print("Nenhum RTT calculado.")
    print("===========================\n")

    s.close()

if __name__ == "__main__":
    main()
