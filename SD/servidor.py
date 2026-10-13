import socket
import threading
from datetime import datetime


def lidar_cliente(conexao, endereco):
  print(f"Conexão estabelecida com {endereco}")
  try:
    dados = conexao.recv(1024).decode("utf-8")
    if dados:
      print(f"[RECEBIDO] {endereco}: {dados}")
      string_revertida = dados[::-1]
      horario_atual = datetime.now().strftime("%H:%M:%S")

      resposta = f"String invertida: {string_revertida} | Horário do servidor: {horario_atual}"
      conexao.send(resposta.encode("utf-8"))
  except Exception as e:
    print(f"Erro ao receber dados de {endereco}: {e}")
  finally:
    conexao.close()
    print(f"Conexão encerrada com {endereco}")


def iniciar_servidor():
  HOST = "127.0.0.1"
  PORTA = 8000
  servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  servidor.bind((HOST, PORTA))
  servidor.listen()
  print(f"Servidor ouvindo em {HOST}:{PORTA}")

  try:
    while True:
      conexao, endereco = servidor.accept()
      thread_cliente = threading.Thread(
          target=lidar_cliente, args=(conexao, endereco)
      )
      thread_cliente.start()
  except KeyboardInterrupt:
    print("\nServidor encerrado.")
  finally:
    servidor.close()


if __name__ == "__main__":
  iniciar_servidor()