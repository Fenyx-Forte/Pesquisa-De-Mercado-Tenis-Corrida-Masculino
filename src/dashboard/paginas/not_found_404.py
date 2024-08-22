import dash
from dash import html

dash.register_page(__name__, name="Not Found 404", title="Not Found 404")


def layout(**kwargs) -> html.Div:
    content_style = {
        "marginLeft": "16rem",
        "marginRight": "2rem",
        "padding": "2rem 1rem",
    }

    conteudo = html.H1("Page not found! Error 404", style=content_style)

    return conteudo
