"""Módulo de funções úteis para determinar a data e hora atuais."""

from datetime import datetime, timedelta, timezone


def formatacao_tempo_completo() -> str:
    """Formata a data e hora atual como string."""
    return "%Y-%m-%d %H:%M:%S"


def fuso_horario_brasilia() -> timezone:
    """Retorna o fuso horário brasileiro."""
    return timezone(timedelta(hours=-3), "BRT")


def data_agora() -> datetime:
    """Retorna a data e hora atual."""
    return datetime.now(fuso_horario_brasilia())


def data_agora_string() -> str:
    """Retorna a data e hora atual como string."""
    return data_agora().strftime(formatacao_tempo_completo())


def data_agora_simplificada() -> str:
    """Retorna a data e hora atual como string simplificada."""
    return data_agora().strftime("%Y-%m-%d")


def data_agora_simplificada_com_underline() -> str:
    """Retorna a data e hora atual como string simplificada com underline."""
    return data_agora().strftime("%Y_%m_%d")
