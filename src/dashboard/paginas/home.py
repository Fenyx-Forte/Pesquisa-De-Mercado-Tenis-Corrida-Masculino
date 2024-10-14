from dash import html, register_page
from dash_bootstrap_components import (
    Col,
    Row,
)

from dashboard.uteis import componentes_pagina

register_page(
    __name__,
    path="/",
    name="Home",
    title="Home",
    description="Página Home",
    image_url="https://analise-de-dados-mercadolivre.onrender.com/assets/images/imagem_link.jpg",
)


def id_pagina() -> str:
    return "home"


def titulo_pagina() -> str:
    return "Home"


def coluna() -> html.Div:
    conteudo = html.Div("Conteúdo Home")

    return conteudo


def colunas() -> Row:
    conteudo = Row(
        [
            Col(
                coluna(),
                xs=12,
                class_name="coluna_hoje",
            ),
        ],
        class_name="linha_colunas",
    )

    return conteudo


layout = html.Div(
    [
        componentes_pagina.div_titulo(titulo_pagina()),
        html.Div("Conteúdo Página Home"),
    ],
    className="pagina",
    id=id_pagina(),
)
