"""Formatações usadas no dashboard."""


def dag_format_pt_br() -> str:
    """Gera uma função para formatação de números em português (Brasil).

    Returns:
        str: Configuração da localização da linguagem.
    """
    return """
    d3.formatLocale(
        {
            "decimal": ",",
            "thousands": ".",
            "grouping": [3],
            "currency": ["R$", ""]
        }
    )
    """
