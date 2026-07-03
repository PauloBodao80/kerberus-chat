"""Testes unitários para common/config.py.

Verifica que todas as constantes de configuração existem
e possuem os valores corretos definidos na especificação.
"""

from common.config import (
    AS_HOST,
    AS_PORT,
    TGS_HOST,
    TGS_PORT,
    SVC_HOST,
    SVC_PORT,
    TAMANHO_CHAVE,
    LIFETIME_TICKET,
    JANELA_AUTH,
)


class TestConstantesAS:
    """Constantes do Authentication Server."""

    def test_as_host_e_localhost(self):
        """AS deve escutar em localhost para fins didáticos."""
        assert AS_HOST == "127.0.0.1"

    def test_as_porta_correta(self):
        """AS deve usar a porta 5450."""
        assert AS_PORT == 5450


class TestConstantesTGS:
    """Constantes do Ticket Granting Server."""

    def test_tgs_host_e_localhost(self):
        """TGS deve escutar em localhost."""
        assert TGS_HOST == "127.0.0.1"

    def test_tgs_porta_correta(self):
        """TGS deve usar a porta 5451."""
        assert TGS_PORT == 5451


class TestConstantesServico:
    """Constantes do Serviço Protegido."""

    def test_svc_host_e_localhost(self):
        """Serviço deve escutar em localhost."""
        assert SVC_HOST == "127.0.0.1"

    def test_svc_porta_correta(self):
        """Serviço deve usar a porta 5452."""
        assert SVC_PORT == 5452


class TestConstantesCriptografia:
    """Constantes relacionadas a chaves e tempos."""

    def test_tamanho_chave_e_16_bytes(self):
        """AES-128 requer chaves de 16 bytes (128 bits)."""
        assert TAMANHO_CHAVE == 16

    def test_lifetime_ticket_e_480_minutos(self):
        """Ticket deve durar 8 horas (480 minutos)."""
        assert LIFETIME_TICKET == 480

    def test_janela_auth_e_300_segundos(self):
        """Janela de autenticação deve ser 5 minutos (300 segundos)."""
        assert JANELA_AUTH == 300
