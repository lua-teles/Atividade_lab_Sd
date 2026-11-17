import rpyc


def exibir_mapa(conn):
    """Busca o estado atual no servidor e exibe formatado no terminal."""
    # O RPyC retorna um 'netref' (referência remota); dict() traz os dados para a memória local
    mapa = dict(conn.root.listar_assentos())

    print("\n" + "=" * 35)
    print("       MAPA DE ASSENTOS")
    print("=" * 35)
    for assento, status in mapa.items():
        print(f"  [{assento:<3}] -> {status}")
    print("=" * 35 + "\n")


def iniciar_cliente():
    HOST = "localhost"
    PORTA = 18861

    try:
        conn = rpyc.connect(HOST, PORTA)
        print(f"Conectado ao servidor em {HOST}:{PORTA}!")
    except ConnectionRefusedError:
        print(
            "Não foi possível conectar ao servidor. Verifique se ele está em execução."
        )
        return

    nome_cliente = input("Digite seu nome para iniciar: ").strip()
    if not nome_cliente:
        nome_cliente = "Cliente Anônimo"

    try:
        while True:
            exibir_mapa(conn)

            print("Opções:")
            print("  [1] Reservar um assento")
            print("  [2] Atualizar mapa de assentos")
            print("  [0] Sair")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                assento = input(
                    "Digite o código do assento desejado (ex: A1): "
                ).strip()
                sucesso, mensagem = conn.root.reservar_assento(
                    nome_cliente, assento
                )
                print(f"\n>>> {mensagem}")
            elif opcao == "2":
                continue
            elif opcao == "0":
                print("Encerrando conexão. Até logo!")
                break
            else:
                print("\n>>> Opção inválida. Tente novamente.")
    except EOFError:
        pass
    finally:
        conn.close()


if __name__ == "__main__":
    iniciar_cliente()