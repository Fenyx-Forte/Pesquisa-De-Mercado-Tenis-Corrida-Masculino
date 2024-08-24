def dag_format_pt_br() -> str:
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
