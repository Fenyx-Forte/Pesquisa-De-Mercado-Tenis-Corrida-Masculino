import datetime


def fuso_horario_brasilia() -> datetime.timezone:
    return datetime.timezone(datetime.timedelta(hours=-3), "BRT")


def data_agora(timezone: datetime.timezone) -> datetime.datetime:
    return datetime.datetime.now(timezone)


def data_agora_string(timezone) -> str:
    return data_agora(timezone).strftime("%d/%m/%Y %H:%M")


def data_agora_brasilia_str() -> str:
    return data_agora_string(fuso_horario_brasilia())


def data_agora_brasilia() -> datetime.datetime:
    return data_agora(fuso_horario_brasilia())
