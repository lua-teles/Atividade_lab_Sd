import socket
import time
import sys

HOST = '127.0.0.1'
PORT = 5000
INTERVALO_HEARTBEAT = 3  

def iniciar_worker():
    
    if len(sys.argv) > 1:
        worker_id = sys.argv[1]
    else:
        worker_id = input("Digite o ID do Worker (ex: Worker_1): ").strip()
        if not worker_id:
            worker_id = "Worker_1"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mensagem = f"PING:{worker_id}"

    print(f"[INICIADO] {worker_id} enviando Heartbeats a cada {INTERVALO_HEARTBEAT}s para {HOST}:{PORT}")
    print("Pressione CTRL+C para simular a queda/parada do nó.\n")

    try:
        while True:
            sock.sendto(mensagem.encode('utf-8'), (HOST, PORT))
            print(f"[{time.strftime('%H:%M:%S')}] Heartbeat 'PING' enviado.")
            time.sleep(INTERVALO_HEARTBEAT)
    except KeyboardInterrupt:
        print(f"\n[PARADO] Worker {worker_id} interrompido.")
    finally:
        sock.close()

if __name__ == "__main__":
    iniciar_worker()