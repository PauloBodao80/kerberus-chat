import socket
import threading

try:
    # Importação relativa quando executado como módulo do pacote as_server
    from .config import AS_HOST, AS_PORT, USER_DB_PATH
    from .user_db import UserDB
except ImportError:
    # Importação direta quando executado como script (python as_server.py)
    from config import AS_HOST, AS_PORT, USER_DB_PATH
    from user_db import UserDB


class ASServer:
    """Servidor de Autenticação (AS) para o projeto kerberos-chat.

    Responsável por receber conexões de clientes e, em uma implementação
    completa, emitir tickets iniciais (TGT). Esta versão implementa o
    esqueleto de rede: inicialização, loop de aceitação de conexões e
    atendimento básico de cada cliente em uma thread dedicada.

    Integra a issue #1 (configurações centralizadas) e a issue #9 (UserDB).
    """

    def __init__(self, host: str = AS_HOST, porta: int = AS_PORT,
                 user_db: UserDB | None = None, chave_mestra: bytes | None = None):
        self.host = host
        self.porta = porta
        self.user_db = user_db
        self.chave_mestra = chave_mestra if chave_mestra is not None else b""
        self._socket: socket.socket | None = None
        self._rodando = False

    def iniciar(self) -> None:
        """Inicia o servidor TCP e aceita conexões em loop.

        Cada conexão aceita é tratada em uma nova thread, permitindo
        atendimento concorrente de múltiplos clientes.
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._socket.bind((self.host, self.porta))
        self._socket.listen(5)
        self._rodando = True

        print(f"[AS] Servidor de Autenticação ouvindo em {self.host}:{self.porta}")

        try:
            while self._rodando:
                con, addr = self._socket.accept()
                thread = threading.Thread(
                    target=self.atender_cliente,
                    args=(con, addr),
                    daemon=True
                )
                thread.start()
        except KeyboardInterrupt:
            print("\n[AS] Encerrando servidor via interrupção do teclado.")
        finally:
            self._rodando = False
            if self._socket is not None:
                self._socket.close()
                self._socket = None

    def atender_cliente(self, con: socket.socket, addr) -> None:
        """Atende um cliente conectado.

        Neste esqueleto, apenas registra a conexão e fecha o socket do
        cliente de forma segura, garantindo o encerramento da thread.
        """
        try:
            print(f"[AS] Conexão recebida de {addr}")
        finally:
            try:
                con.close()
            except OSError:
                pass


if __name__ == "__main__":
    # Instancia o UserDB usando o caminho definido na configuração (issue #1)
    banco_usuarios = UserDB(USER_DB_PATH)

    # Cria o servidor utilizando host e port das configurações (issue #1)
    # e o UserDB da issue #9
    servidor = ASServer(
        host=AS_HOST,
        porta=AS_PORT,
        user_db=banco_usuarios,
        chave_mestra=b""
    )
    servidor.iniciar()