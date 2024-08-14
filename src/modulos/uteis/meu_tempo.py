import datetime


def fuso_horario_brasilia() -> datetime.timezone:
    return datetime.timezone(datetime.timedelta(hours=-3), "BRT")


def data_agora() -> datetime.datetime:
    return datetime.datetime.now(fuso_horario_brasilia)


def data_agora_string() -> str:
    return data_agora().strftime("%d/%m/%Y %H:%M")
