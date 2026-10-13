import rpyc
from rpyc.utils.server import ThreadedServer
from datetime import datetime

# Define o serviço que o servidor irá disponibilizar
class HorarioService(rpyc.Service):
    def exposed_get_horario(self):
        """Método exposto ao cliente para retornar o horário atual."""
        return datetime.now().strftime("%H:%M:%S")

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORTA = 18861  # Porta padrão do RPyC

    print(f"Servidor RPyC rodando em {HOST}:{PORTA}...")
    servidor = ThreadedServer(HorarioService, hostname=HOST, port=PORTA)
    
    try:
        servidor.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")