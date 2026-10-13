import socket


def iniciar_cliente():
  HOST = "127.0.0.1"
  PORTA = 8000
  cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    cliente.connect((HOST, PORTA))
    print("Conexão estabelecida com o servidor.")

    mensagem = "Olá, Mundo Distribuído"
    print(f"Enviando mensagem: {mensagem}")
    cliente.sendall(mensagem.encode("utf-8"))

    resposta = cliente.recv(1024).decode("utf-8")
    print(f"Resposta do servidor: {resposta}")
  except Exception as e:
    print(f"Erro ao conectar com o servidor: {e}")
  finally:
    cliente.close()
    print("Conexão encerrada.")


if __name__ == "__main__":
  iniciar_cliente()