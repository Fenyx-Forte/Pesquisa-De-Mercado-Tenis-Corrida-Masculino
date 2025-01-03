"""Traduções usadas no dashboard."""


def dag_locale_pt_br() -> dict[str, str]:
    """Gera um dicionário com as configurações de localização para o português (Brasil).

    Returns:
        dict[str, str]: Dicionário contendo as configurações de localização.
    """
    return {
        # Number Filter & Text Filter
        "filterOoo": "Filtrar...",
        "equals": "Igual a",
        "notEqual": "Diferente de",
        "blank": "Vazio",
        "notBlank": "Não está vazio",
        # Number Filter
        "lessThan": "Menor que",
        "greaterThan": "Maior que",
        "lessThanOrEqual": "Menor ou igual a",
        "greaterThanOrEqual": "Maior ou igual a",
        "inRange": "Entre",
        "inRangeStart": "De",
        "inRangeEnd": "Até",
        # Text Filter
        "contains": "Contém",
        "notContains": "Não contém",
        "startsWith": "Começa com",
        "endsWith": "Termina com",
        # Date Filter
        "dateFormatOoo": "dd-mm-yyyy",
        "before": "Antes",
        "after": "Depois",
        # Filter Conditions
        "andCondition": "E",
        "orCondition": "OU",
        # Data types
        "true": "Verdadeiro",
        "false": "Falso",
    }
