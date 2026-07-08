"""Re-exporta funcoes e constantes do modulo de mensagens (tgs_server.message).

Este modulo existe para manter compatibilidade com imports como
'from common.protocol import empacotar', usados por todos os componentes
(AS, TGS, Servico, Cliente).

As funcoes reais vivem em tgs_server.message — este arquivo apenas
re-exporta para que todos os modulos encontrem no mesmo caminho.
"""

from tgs_server.message import (
    # Constantes de tipo de mensagem
    MSG_AUTH_REQUEST,
    MSG_AUTH_REPLY,
    MSG_TGS_REQUEST,
    MSG_TGS_REPLY,
    MSG_SVC_REQUEST,
    MSG_SVC_REPLY,
    MSG_CHAT,
    MSG_ECHO,
    MSG_ERROR,
    # Funcoes de empacotamento
    empacotar,
    desempacotar,
    # Funcoes de ticket
    criar_ticket,
    extrair_ticket,
)

__all__ = [
    "MSG_AUTH_REQUEST",
    "MSG_AUTH_REPLY",
    "MSG_TGS_REQUEST",
    "MSG_TGS_REPLY",
    "MSG_SVC_REQUEST",
    "MSG_SVC_REPLY",
    "MSG_CHAT",
    "MSG_ECHO",
    "MSG_ERROR",
    "empacotar",
    "desempacotar",
    "criar_ticket",
    "extrair_ticket",
]
