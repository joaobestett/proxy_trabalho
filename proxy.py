import socket
import threading
import time
import csv
import os

HOST_PROXY = "127.0.0.1"
PORT_PROXY = 9000

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9001

os.makedirs("logs", exist_ok=True)

def log_metrics(metrics):
    file_exists = os.path.isfile("logs/metrics.csv")

    with open("logs/metrics.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "rtt", "jitter", "throughput", "goodput", "retransmissions", "cwnd"])
        writer.writerow(metrics)

def proxy_handler(client_conn, client_addr):
    print(f"[PROXY] Cliente conectado: {client_addr}")

    server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conn.connect((SERVER_HOST, SERVER_PORT))

    last_rtt = None
    retransmissions = 0
    cwnd = 1
    ssthresh = 8

    def forward(src, dst, direction):
        nonlocal last_rtt, retransmissions, cwnd, ssthresh

        while True:
            try:
                start = time.time()
                data = src.recv(4096)
                if not data:
                    break

                # -------- RTT ----------
                send_time = time.time()
                dst.sendall(data)
                ack_time = time.time()
                rtt = (ack_time - send_time) * 1000

                if last_rtt is None:
                    jitter = 0
                else:
                    jitter = abs(rtt - last_rtt)

                last_rtt = rtt

                # ------- Retransmissões (simulação) -------
                if jitter > rtt * 1.5:
                    retransmissions += 1

                # ------- Goodput / Throughput -------
                payload = len(data)
                throughput = payload / (rtt / 1000 + 0.00001)
                goodput = payload  

                # -------- TCP Congestion Control Estimado -------
                if rtt < 80:
                    cwnd += 1
                else:
                    ssthresh = cwnd // 2
                    cwnd = ssthresh

                # --------- TCP pacing ---------
                pacing_rate = max(10000, cwnd * 1200)  
                time.sleep(payload / pacing_rate)

                # --------- Delayed ACK adaptativo ---------
                delay = min(max(rtt * 0.25 / 1000, 0.005), 0.02)
                time.sleep(delay)

                # --------- Log ---------
                log_metrics([
                    time.time(), round(rtt, 3), round(jitter, 3),
                    round(throughput, 3), goodput, retransmissions, cwnd
                ])

                print(f"[RTT={rtt:.2f}ms] [CWND={cwnd}] [GOODPUT={goodput}] [RET={retransmissions}]")

            except:
                break

    threading.Thread(target=forward, args=(client_conn, server_conn, "c→s")).start()
    threading.Thread(target=forward, args=(server_conn, client_conn, "s→c")).start()

def main():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind((HOST_PROXY, PORT_PROXY))
    proxy.listen(5)

    print(f"[PROXY] Escutando em {HOST_PROXY}:{PORT_PROXY}")

    while True:
        conn, addr = proxy.accept()
        threading.Thread(target=proxy_handler, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
