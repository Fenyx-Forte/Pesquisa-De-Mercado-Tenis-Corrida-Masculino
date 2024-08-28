from dash import page_container
from dash_bootstrap_components import Col, Container, Row, Stack, icons, themes

from dashboard.componentes import cabecalho, minha_sidebar


def minhas_meta_tags() -> list[dict[str, str]]:
    meta_tags = [
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        },
        {
            "http-equiv": "Content-Language",
            "content": "pt-BR",
        },
        {
            "name": "author",
            "content": "Fenyx Forte",
        },
        {
            "name": "application-name",
            "content": "Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        },
        {
            "name": "keywords",
            "content": "webscraping dashboard dados",
        },
        {
            "name": "google",
            "content": "notranslate",
        },
        {
            "name": "robots",
            "content": "index, follow",
        },
        {
            "name": "googlebot",
            "content": "index, follow",
        },
    ]

    return meta_tags


def configuracoes_app() -> dict:
    configuracoes = {
        "external_stylesheets": [
            themes.LUMEN,
            icons.FONT_AWESOME,
        ],
        "update_title": None,
        "assets_folder": "../assets/",
        "use_pages": True,
        "pages_folder": "./dashboard/paginas",
        "suppress_callback_exceptions": True,
        "meta_tags": minhas_meta_tags(),
    }

    return configuracoes


def layout_app() -> Container:
    layout = Container(
        Row(
            [
                Col(
                    minha_sidebar.sidebar(),
                    width="auto",
                ),
                Col(
                    Stack(
                        [
                            cabecalho.cabecalho(),
                            page_container,
                        ],
                    ),
                    width=True,
                ),
            ],
        ),
        fluid=True,
    )

    return layout
