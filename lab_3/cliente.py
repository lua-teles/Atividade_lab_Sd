import socket
import threading
import sys

HOST = "127.0.0.1"
PORTA = 55555

apelido = input("Escolha seu apelido no chat: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cliente.connect((HOST, PORTA))
except Exception as e:
    print(f"Não foi possível conectar ao servidor: {e}")
    sys.exit()

def receber_mensagens():
    """Thread dedicada para escutar dados do servidor sem travar a digitação."""
    while True:
        try:
            mensagem = cliente.recv(1024).decode("utf-8")
            if mensagem == "NICK":
                # Responde ao pedido do servidor enviando o apelido
                cliente.send(apelido.encode("utf-8"))
            elif mensagem:
                print(f"\r{mensagem}\nVocê: ", end="")
        except Exception:
            print("\n[ERRO] Conexão com o servidor foi perdida.")
            cliente.close()
            break

def enviar_mensagens():
    """Loop principal para capturar a entrada do usuário e enviar ao servidor."""
    while True:
        try:
            texto = input("Você: ")
            if texto.strip().lower() == "/sair":
                cliente.close()
                print("Você saiu do chat.")
                break
            
            mensagem_formatada = f"{apelido}: {texto}"
            cliente.send(mensagem_formatada.encode("utf-8"))
        except Exception:
            break

if __name__ == "__main__":
    # Inicia a thread responsável por escutar o servidor em segundo plano
    thread_receber = threading.Thread(target=receber_mensagens)
    thread_receber.daemon = True
    thread_receber.start()

    # Executa o loop de envio de mensagens na thread principal
    enviar_mensagens()