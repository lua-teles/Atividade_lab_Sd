import threading
import time
import rpyc
from rpyc.utils.server import ThreadedServer


class ReservaAssentosService(rpyc.Service):
    # Estado compartilhado na memória (atributo de classe)
    # Todos os clientes conectados enxergarão e modificarão este mesmo dicionário
    assentos = {f"A{i}": None for i in range(1, 11)}

    # Lock global para controle de concorrência (Exclusão Mútua)
    lock = threading.Lock()

    def on_connect(self, conn):
        print("[LOG] Novo cliente conectado.")

    def on_disconnect(self, conn):
        print("[LOG] Cliente desconectado.")

    def exposed_listar_assentos(self):
        """Retorna uma cópia formatada do status atual de cada assento."""
        with self.lock:
            status = {}
            for assento, cliente in self.assentos.items():
                if cliente is None:
                    status[assento] = "Livre"
                else:
                    status[assento] = f"Reservado ({cliente})"
            return status

    def exposed_reservar_assento(self, nome_cliente, assento):
        """Tenta reservar um assento de forma thread-safe."""
        assento = assento.strip().upper()

        # Início da seção crítica: apenas uma thread entra aqui por vez
        with self.lock:
            if assento not in self.assentos:
                return False, f"Erro: O assento '{assento}' não existe."

            # Simula um pequeno atraso de processamento para facilitar testes de concorrência
            time.sleep(0.5)

            if self.assentos[assento] is None:
                self.assentos[assento] = nome_cliente
                print(
                    f"[RESERVA] Assento {assento} reservado para {nome_cliente}."
                )
                return (
                    True,
                    f"Sucesso! Assento {assento} reservado para {nome_cliente}.",
                )
            else:
                ocupante = self.assentos[assento]
                print(
                    f"[CONFLITO] {nome_cliente} tentou reservar {assento}, mas já pertence a {ocupante}."
                )
                return (
                    False,
                    f"Aviso: Assento {assento} já ocupado por {ocupante}.",
                )


if __name__ == "__main__":
    PORTA = 18861
    print(f"Iniciando servidor de reservas na porta {PORTA}...")
    # ThreadedServer é essencial para atender múltiplos clientes simultaneamente
    servidor = ThreadedServer(
        ReservaAssentosService,
        port=PORTA,
        protocol_config={"allow_public_attrs": True},
    )
    servidor.start()