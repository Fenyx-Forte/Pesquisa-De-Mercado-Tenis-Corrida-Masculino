"""Módulo para carregar o arquivo de configuração ".env" do projeto."""

from dotenv import load_dotenv


def carregar_env() -> None:
    """Carrega o arquivo de configuração ".env" do projeto."""
    load_dotenv("../.env")
