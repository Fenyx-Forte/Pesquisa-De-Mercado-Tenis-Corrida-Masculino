from dotenv import load_dotenv


def carregar_env() -> None:
    load_dotenv("../.env")
