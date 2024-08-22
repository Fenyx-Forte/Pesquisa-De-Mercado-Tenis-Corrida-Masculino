import dash
from dash import html

dash.register_page(__name__, name="Not Found 404", title="Not Found 404")


def layout(**kwargs) -> html.Div:
    conteudo = html.H1("Page not found! Error 404", className="pagina")

    return conteudo
