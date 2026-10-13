import rpyc

HOST = "127.0.0.1"
PORTA = 18861

if __name__ == "__main__":
    #Conecta ao servidor RPyC
    conexao = rpyc.connect(HOST, PORTA)

    # Solicita o horário chamando o método exposto
    horario_atual = conexao.root.get_horario()
    
    print(f"Horário recebido do servidor: {horario_atual}")

    # Encerra a conexão
    conexao.close()
    print("Conexão encerrada pelo cliente.")