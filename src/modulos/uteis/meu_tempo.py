from datetime import datetime, timedelta, timezone


def formatacao_tempo_completo() -> str:
    return "%Y-%m-%d %H:%M:%S"


def fuso_horario_brasilia() -> timezone:
    return timezone(timedelta(hours=-3), "BRT")


def data_agora() -> datetime:
    return datetime.now(fuso_horario_brasilia())


def data_agora_string() -> str:
    return data_agora().strftime(formatacao_tempo_completo())


def data_agora_simplificada() -> str:
    return data_agora().strftime("%Y-%m-%d")


def data_agora_simplificada_com_underline() -> str:
    return data_agora().strftime("%Y_%m_%d")
