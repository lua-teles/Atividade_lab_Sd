import socket
import time
import threading

HOST = '127.0.0.1'
PORT = 5000
TIMEOUT_LIMIT = 8.0  

workers_status = {}
lock = threading.Lock()

def monitor_check_loop():
    """Thread que roda em background verificando o status dos workers."""
    while True:
        time.sleep(1)  
        agora = time.time()
        
        with lock:
            
            for worker_id, ultimo_heartbeat in list(workers_status.items()):
                tempo_decorrido = agora - ultimo_heartbeat
                
                if tempo_decorrido > TIMEOUT_LIMIT:
                    print(f"\n[ALERTA] O Nó {worker_id} está OFFLINE! (Sem sinal há {tempo_decorrido:.1f}s)")
                   
                    del workers_status[worker_id]


def iniciar_servidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    
    print(f"[INICIADO] Servidor Monitor rodando em {HOST}:{PORT}")
    print(f"[CONFIG] Tempo limite para timeout: {TIMEOUT_LIMIT}s\n")

    thread_checker = threading.Thread(target=monitor_check_loop, daemon=True)
    thread_checker.start()

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            mensagem = data.decode('utf-8').strip()
            
            if mensagem.startswith("PING:"):
                worker_id = mensagem.split(":", 1)[1]
                agora = time.time()
                
                with lock:
                    
                    if worker_id not in workers_status:
                        print(f"[CONECTADO] Nó {worker_id} registrado/restabelecido com sucesso.")
                    
                    workers_status[worker_id] = agora
                
                print(f"[HEARTBEAT] Recebido de {worker_id} às {time.strftime('%H:%M:%S')}")
                
        except KeyboardInterrupt:
            print("\n[ENCERRANDO] Servidor finalizado.")
            break
        except Exception as e:
            print(f"[ERRO] {e}")

    sock.close()

if __name__ == "__main__":
    iniciar_servidor()