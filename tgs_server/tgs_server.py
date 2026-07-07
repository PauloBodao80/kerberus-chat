import socket
import threading
from message import (
    desempacotar,
    empacotar,
    MSG_TGS_REQUEST,
    MSG_ERROR,
)

class TGSServer:
    def __init__(self, host, porta, chave_as, chave_servico):       
        self.host = host
        self.porta = porta
        self.chave_as = chave_as
        self.chave_servico = chave_servico

    def iniciar(self):    
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        servidor.bind((self.host, self.porta))
        servidor.listen()

        print(f"TGS escutando em {self.host}:{self.porta}")

        while True:
            con, addr = servidor.accept()

            thread = threading.Thread(
                target=self.atender_cliente,
                args=(con, addr),
                daemon=True,
            )
            thread.start()

    def atender_cliente(self, con, addr):
        try:
            dados = con.recv(4096)

            if not dados:
                return

            tipo, payload = desempacotar(dados)

            if tipo != MSG_TGS_REQUEST:
                con.sendall(
                    empacotar(MSG_ERROR, b"Tipo de mensagem invalido")
                )
                return

            if len(payload) < 2:
                con.sendall(
                    empacotar(MSG_ERROR, b"Payload invalido")
                )
                return

            tam_tgt = int.from_bytes(payload[:2], "big")

            if len(payload) < 2 + tam_tgt:
                con.sendall(
                    empacotar(MSG_ERROR, b"TGT incompleto")
                )
                return

            tgt_cif = payload[2:2 + tam_tgt]
            nome_servico = payload[2 + tam_tgt:].decode("utf-8")

            if not nome_servico:
                con.sendall(
                    empacotar(MSG_ERROR, b"Servico invalido")
                )
                return

            print(f"[TGS] Cliente {addr}")
            print(f"[TGS] Serviço solicitado: {nome_servico}")
            print(f"[TGS] TGT recebido ({len(tgt_cif)} bytes)")

        except Exception as e:
            print(f"Erro ao atender {addr}: {e}")
            con.sendall(
                empacotar(MSG_ERROR, b"Erro interno")
            )

        finally:
            con.close()

if __name__ == "__main__":
    servidor = TGSServer(
        "127.0.0.1",
        5451,
        chave_as="chave_as",
        chave_servico="chave_servico",
    )
    servidor.iniciar()