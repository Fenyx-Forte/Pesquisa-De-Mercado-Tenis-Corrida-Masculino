from dash import page_container
from dash_bootstrap_components import Col, Container, Row, Stack, icons, themes

from dashboard.componentes import cabecalho, minha_sidebar


def template_html_padrao() -> str:
    template = """
    <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <link rel="icon" type="image/png" href="/assets/favicon.ico">
                <title>{%title%}</title>
                {%css%}
                <link rel="stylesheet" href="/assets/css/styles.css">
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
    """

    return template


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
        "assets_folder": "../assets",
        "assets_url_path": "/assets",
        "use_pages": True,
        "pages_folder": "./dashboard/paginas",
        "suppress_callback_exceptions": True,
        "index_string": template_html_padrao(),
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
                    class_name="meu-conteudo",
                ),
            ],
        ),
        fluid=True,
        class_name="meu-conteiner",
    )

    return layout
