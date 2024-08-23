from dash import html, register_page
from modulos.uteis import meu_tempo

register_page(__name__, path="/", name="Home", title="Home")


layout = html.Div(
    [
        html.H1("This is our Home page"),
        html.Div("This is our Home page content."),
        html.Div(f"{meu_tempo.data_agora_string()}"),
    ],
    className="pagina",
)
