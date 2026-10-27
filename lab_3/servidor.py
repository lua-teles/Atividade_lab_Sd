import socket
import threading

HOST = '127.0.0.1'
PORTA = 55555

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORTA))    
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.listen()

clientes = []
apelidos = []


def broadcast(mensagem, cliente_remetente):
    for cliente in clientes:
        if cliente != cliente_remetente:
            try:
                cliente.send(mensagem)
            except:
                remover_cliente(cliente)
                
def remover_cliente(cliente):
    if cliente in clientes:
        index = clientes.index(cliente)
        clientes.remove(cliente)
        apelido = apelidos[index]
        apelidos.remove(apelido)
        cliente.close()
        broadcast(f'{apelido} saiu do chat!'.encode('utf-8'), cliente)
        
def lidar_com_cliente(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024)
            if mensagem:
                broadcast(mensagem, cliente_remetente = cliente)
            else:
                remover_cliente(cliente)
                break
        except Exception:
            remover_cliente(cliente)
            break
        
def receber_conexoes():
    print("Servidor está ouvindo conexões...")
    while True:
        try:
            cliente, endereco = servidor.accept()
            print(f"Conexão estabelecida com {endereco}")
            
            cliente.send("APELIDO".encode('utf-8'))
            apelido = cliente.recv(1024).decode('utf-8')
            
            apelidos.append(apelido)
            clientes.append(cliente)
            
            print(f"Apelido do cliente é {apelido}")
            broadcast(f"{apelido} entrou no chat!".encode('utf-8'), cliente)
            cliente.send("Conectado ao servidor!".encode('utf-8'))
            
            thread = threading.Thread(target=lidar_com_cliente, args=(cliente,))
            thread.daaemon = True
            thread.start()
        except KeyboardInterrupt:
            print("Servidor encerrado pelo usuário.")
            servidor.close()
            break
        
if __name__ == "__main__":
    receber_conexoes()